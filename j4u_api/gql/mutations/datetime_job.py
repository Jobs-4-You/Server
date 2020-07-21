from datetime import timezone

import graphene
from dateutil.parser import parse

from j4u_api.database import db_session
from j4u_api.database.enums import RoleEnum
from j4u_api.database.models import DatetimeJob as DatetimeJobModel
from j4u_api.gql.input_types import DatetimeJobInput
from j4u_api.gql.types import DatetimeJob
from j4u_api.qualtrics import qual_client
from j4u_api.utils.auth import roles_required


class CreateDatetimeJob(graphene.Mutation):
    class Arguments:
        datetime_job = DatetimeJobInput(required=True)

    datetime_job = graphene.Field(DatetimeJob)

    @roles_required([RoleEnum.ADMIN])
    def mutate(root, info, datetime_job):
        params = datetime_job["params"]

        mlist = qual_client.get_j4u_mailinglist()
        mlist_id = mlist["id"]
        distrib = qual_client.create_distribution(
            params["surveyId"],
            mlist_id,
            parse(params["surveyEnd"]),
            datetime_job["name"],
        )
        distrib_id = distrib["id"]
        params["distribId"] = distrib_id

        datetime_job["execution_date"] = (
            datetime_job["execution_date"]
            .replace(tzinfo=timezone.utc)
            .astimezone(tz=None)
        )

        new_datetime_job = DatetimeJobModel(**datetime_job)

        db_session.add(new_datetime_job)
        db_session.commit()
        return CreateDatetimeJob(datetime_job=new_datetime_job)


class DeleteDatetimeJob(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @roles_required([RoleEnum.ADMIN])
    def mutate(root, info, id):
        DatetimeJobModel.query.filter_by(id=id).delete()
        db_session.commit()

        return DeleteDatetimeJob(ok=True)
