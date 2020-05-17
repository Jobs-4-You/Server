import humps
from elasticsearch_dsl import Q, Search

import j4u_api.database.models as models
import j4u_api.gql.types as types
from j4u_api.config import config
from j4u_api.database.connection import db_session
from j4u_api.database.enums import RoleEnum
from j4u_api.job_room import job_room_client
from j4u_api.qualtrics import qual_client
from j4u_api.recommendations import recom_engine
from j4u_api.utils.auth import jwt_auth_required, roles_required
from j4u_api.utils.func import pick_rename
from j4u_api.utils.token import create_signup_token


@roles_required([RoleEnum.ADMIN])
def resolve_all_users(parent, info):
    query = models.User.query
    return query.all()


@roles_required([RoleEnum.ADMIN])
def resolve_all_groups(parent, info):
    query = models.Group.query.order_by(models.Group.name)
    return query.all()


@jwt_auth_required
def resolve_me(parent, info):
    return info.context.user


@roles_required([RoleEnum.ADMIN])
def resolve_get_signup_link(parent, info, group_id, expire_at):
    signup_token = create_signup_token(group_id, expire_at)
    url = f"{config.APP_URL}/?signup&token={signup_token}"
    return types.SignupUrl(url=url, token=signup_token)


def resolve_all_surveys(parent, info):
    res = []
    data = qual_client.list_surveys()
    data = humps.decamelize(data)
    for d in data:
        sm = types.SurveyMeta(**d)
        res.append(sm)
    return res


def resolve_job_search_hints(parent, info, query, limit=5):
    # qs = [Q("fuzzy", title=q) for q in query.split()]
    # query = qs.pop()
    # for q in qs:
    #    query = query | q
    query = query.lower()
    qq = " AND ".join([f"({x}*)" for x in query.split()])
    print(qq)

    query = Q("query_string", query=qq, fields=["title"])

    s = Search(index="jobs").query(query)[:limit]
    from j4u_api.utils.print import pretty_print

    response = s.execute()
    res = []
    for hit in response:
        meta = hit.meta
        hit.id = meta.id
        res.append(hit)
    return res


def resolve_positions(parent, info, profession_codes, page):
    total_count, positions = job_room_client.search(profession_codes, page)

    paths = [
        # Genral
        ("id", "jobAdvertisement.id"),
        ("job_quantity", "jobAdvertisement.jobContent.numberOfJobs"),
        ("external_url", "jobAdvertisement.jobContent.externalUrl"),
        # Company
        ("company.name", "jobAdvertisement.jobContent.company.name"),
        ("company.city", "jobAdvertisement.jobContent.company.city"),
        ("company.street", "jobAdvertisement.jobContent.company.street"),
        ("company.postal_code", "jobAdvertisement.jobContent.company.postalCode"),
        ("company.house_number", "jobAdvertisement.jobContent.company.houseNumber"),
        ("company.country_code", "jobAdvertisement.jobContent.company.countryIsoCode"),
        # Employment
        ("employment.start_date", "jobAdvertisement.jobContent.employment.startDate"),
        ("employment.end_date", "jobAdvertisement.jobContent.employment.endDate"),
        ("employment.short", "jobAdvertisement.jobContent.employment.shortEmployment"),
        (
            "employment.immediately",
            "jobAdvertisement.jobContent.employment.immediately",
        ),
        ("employment.permanent", "jobAdvertisement.jobContent.employment.permanent"),
        (
            "employment.workload_perc_min",
            "jobAdvertisement.jobContent.employment.workloadPercentageMin",
        ),
        (
            "employment.workload_perc_max",
            "jobAdvertisement.jobContent.employment.workloadPercentageMax",
        ),
        # Location
        ("location.city", "jobAdvertisement.jobContent.location.city"),
        (
            "location.country_code",
            "jobAdvertisement.jobContent.location.countryIdoCode",
        ),
        ("location.canton_code", "jobAdvertisement.jobContent.location.cantonCode"),
        # Contact
        ("contact.salutation", "jobAdvertisement.jobContent.publicContact.salutation"),
        ("contact.first_name", "jobAdvertisement.jobContent.publicContact.firstName"),
        ("contact.last_name", "jobAdvertisement.jobContent.publicContact.lastName"),
        ("contact.phone", "jobAdvertisement.jobContent.publicContact.phone"),
        ("contact.email", "jobAdvertisement.jobContent.publicContact.email"),
    ]

    processed_positions = []
    for position in positions:
        p = pick_rename(position, paths)

        desc_paths = [
            ("language_code", "languageIsoCode"),
            ("title", "title"),
            ("description", "description"),
        ]

        p["descriptions"] = []
        descs = position["jobAdvertisement"]["jobContent"]["jobDescriptions"]
        if type(descs) is list:
            for desc in descs:
                processed_desc = pick_rename(desc, desc_paths)
                p["descriptions"].append(processed_desc)

        processed_positions.append(p)

    res = {
        "total_count": total_count,
        "positions": processed_positions,
    }

    return res


@jwt_auth_required
def resolve_recommendations(parent, info, old_job_isco08, old_job_title, alpha, beta):
    user = info.context.user
    features = [(x.feature_config.engine_name, x.value) for x in user.features]
    features = sorted(features, key=lambda x: x[0])
    _, features = zip(*features)
    vars = list(features) + [alpha, old_job_isco08, beta]
    recoms = recom_engine.recom(*vars)
    res = {}
    res["var_list"] = recoms["var_list"]
    res["importances"] = recoms["importances"]
    res_list = list(
        zip(
            recoms["isco08_list"],
            recoms["avam_list"],
            recoms["bfs_list"],
            recoms["job_title_list"],
        )
    )
    res_list = [
        dict(
            [
                ("isco08", isco08),
                ("avam", avam),
                ("bfs", bfs),
                ("job_title", job_title.title()),
            ]
        )
        for isco08, avam, bfs, job_title in res_list
    ]

    user.alpha = alpha
    user.beta = beta
    user.old_job_isco08 = old_job_isco08
    user.old_job_title = old_job_title
    db_session.add(user)
    db_session.commit()

    res["results"] = sorted(res_list, key=lambda x: x["job_title"])

    return res
