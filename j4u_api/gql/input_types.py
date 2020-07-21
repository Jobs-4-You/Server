import graphene

from j4u_api.gql.enums import CiviliteEnum


class UserInput(graphene.InputObjectType):
    civilite = CiviliteEnum(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    birth_date = graphene.Date(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    phone = graphene.String(required=True)


class UIConfigInput(graphene.InputObjectType):
    search = graphene.Boolean(required=True)
    recommendations = graphene.Boolean(required=True)
    alpha_fixed = graphene.Boolean(required=True)
    beta_fixed = graphene.Boolean(required=True)


class GroupInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    baseline_id = graphene.ID(required=True)
    cruiser_id = graphene.ID(required=True)
    ui_config = UIConfigInput(required=True)


class EventInput(graphene.InputObjectType):
    type = graphene.String(required=True)
    payload = graphene.JSONString()


class DatetimeJobInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    action = graphene.String(required=True)
    params = graphene.JSONString(required=True)
    execution_date = graphene.DateTime(required=True)
