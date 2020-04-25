
import graphene

from j4u_api.database import db_session
from j4u_api.database.enums import RoleEnum
from j4u_api.database.models import Group as GroupModel
from j4u_api.gql.input_types import GroupInput
from j4u_api.gql.types import Group
from j4u_api.utils.auth import roles_required


class UpdateGroupConfig(graphene.Mutation):
    class Arguments:
        group_id = graphene.ID(required=True)
        group_data = GroupInput(required=True)

    group = graphene.Field(Group)

    @roles_required([RoleEnum.ADMIN])
    def mutate(root, info, group_id, group_data):
        group = GroupModel.query.get(group_id)
        print(group)
        for k, v in group_data.items():
            setattr(group, k, v)

        db_session.add(group)
        db_session.commit()
        group = GroupModel.query.get(group_id)
        print(group_data)
        print(group)
        return UpdateGroupConfig(group=group)
