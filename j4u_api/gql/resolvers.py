import humps

import j4u_api.gql.types as types
from j4u_api.config import config
from j4u_api.database.enums import RoleEnum
from j4u_api.qualtrics import qual_client
from j4u_api.utils.auth import jwt_auth_required, roles_required
from j4u_api.utils.token import create_signup_token


@roles_required([RoleEnum.ADMIN])
def resolve_all_users(parent, info):
    query = types.User.get_query(info)  # SQLAlchemy query
    return query.all()


@roles_required([RoleEnum.ADMIN])
def resolve_all_groups(parent, info):
    query = types.Group.get_query(info)  # SQLAlchemy query
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
    print(res)
    return res
