import graphene
from .types import *
from .mutations import *
from .resolvers import *
from .enums import GroupEnum


class Query(graphene.ObjectType):
    all_users = graphene.List(User, resolver=resolve_all_users)
    me = graphene.Field(User, resolver=resolve_me)
    get_signup_link = graphene.Field(
        SignupUrl,
        group=GroupEnum(required=True),
        expire_at=graphene.DateTime(required=True),
        resolver=resolve_get_signup_link,
    )


class Mutation(graphene.ObjectType):
    auth = Auth.Field()
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
