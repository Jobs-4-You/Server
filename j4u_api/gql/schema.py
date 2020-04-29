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
    job_search_hints = graphene.Field(
        graphene.List(types.JobSearchHint),
        query=graphene.String(required=True),
        limit=graphene.Int(),
        resolver=resolvers.resolve_job_search_hints,
    )
    positions = graphene.Field(
        types.PostionsResult,
        profession_codes=graphene.List(graphene.Int, required=True),
        page=graphene.Int(required=True),
        resolver=resolvers.resolve_positions,
    )
    recommendations = graphene.Field(
        types.RecommendationResult,
        old_job_isco08=graphene.Int(required=True),
        alpha=graphene.Float(required=True),
        beta=graphene.Float(required=True),
        resolver=resolvers.resolve_recommendations,
    )


class Mutation(graphene.ObjectType):
    auth = mutations.Auth.Field()
    create_user = mutations.CreateUser.Field()
    verify_user = mutations.VerifyUser.Field()
    update_group_config = mutations.UpdateGroupConfig.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)