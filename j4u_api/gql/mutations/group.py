
import graphene

from j4u_api.database import db_session
from j4u_api.database.models import Group as GroupModel
from j4u_api.gql.types import Group


class UpdateGroupSurveys(graphene.Mutation):
    class Arguments:
        group_id = graphene.String(required=True)
        baseline_id = graphene.String()
        cruiser_id = graphene.String()

    group = graphene.Field(Group, required=True)

    def mutate(root, info, group_id, baseline_id, cruiser_id):
        group = GroupModel.query.filter(Group.id == group_id)

        if baseline_id:
            group.baseline_id = baseline_id
        if cruiser_id:
            group.cruiser_id = cruiser_id

        db_session.add(group)
        db_session.commit()
        group = GroupModel.query.filter(Group.id == group_id)

        return UpdateGroupSurveys(group=group)
