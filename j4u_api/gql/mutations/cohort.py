import graphene

from j4u_api.database import db_session
from j4u_api.database.enums import RoleEnum
from j4u_api.database.models import Cohort as CohortModel
from j4u_api.gql.input_types import CohortInput
from j4u_api.gql.types import Cohort
from j4u_api.utils.auth import roles_required


class CreateCohort(graphene.Mutation):
    class Arguments:
        cohort_data = CohortInput(required=True)

    cohort = graphene.Field(Cohort)

    @roles_required([RoleEnum.ADMIN])
    def mutate(root, info, cohort_data):
        cohort = CohortModel(**cohort_data)

        db_session.add(cohort)
        db_session.commit()
        return CreateCohort(cohort=cohort)


class UpdateCohort(graphene.Mutation):
    class Arguments:
        cohort_id = graphene.ID(required=True)
        cohort_data = CohortInput(required=True)

    cohort = graphene.Field(Cohort)

    @roles_required([RoleEnum.ADMIN])
    def mutate(root, info, cohort_id, cohort_data):
        cohort = CohortModel.query.get(cohort_id)
        print(cohort)
        for k, v in cohort_data.items():
            setattr(cohort, k, v)

        db_session.add(cohort)
        db_session.commit()

        print(cohort)
        print(cohort.name)
        return UpdateCohort(cohort=cohort)
