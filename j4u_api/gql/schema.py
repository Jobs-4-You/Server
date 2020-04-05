import graphene

import j4u_api.gql.mutations as mutations
import j4u_api.gql.resolvers as resolvers
import j4u_api.gql.types as types


class Query(graphene.ObjectType):
    all_users = graphene.List(types.User, resolver=resolvers.resolve_all_users)
    all_groups = graphene.List(types.Group, resolver=resolvers.resolve_all_groups)
    me = graphene.Field(types.User, resolver=resolvers.resolve_me)
    get_signup_link = graphene.Field(
        types.SignupUrl,
        group_id=graphene.Int(required=True),
        expire_at=graphene.DateTime(required=True),
        resolver=resolvers.resolve_get_signup_link,
    )
    all_surveys = graphene.List(
        types.SurveyMeta, resolver=resolvers.resolve_all_surveys
    )


class Mutation(graphene.ObjectType):
    auth = mutations.Auth.Field()
    create_user = mutations.CreateUser.Field()
    verify_user = mutations.VerifyUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
