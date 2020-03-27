import graphene
from gql.enums import CiviliteEnum


class UserInput(graphene.InputObjectType):
    civilite = CiviliteEnum(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    birth_date = graphene.Date(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    phone = graphene.String(required=True)
