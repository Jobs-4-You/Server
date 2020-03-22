import graphene

class UserInput(graphene.InputObjectType):
    civilite = graphene.String(required=True)
    first_name = graphene.String(required=True)
    first_name = graphene.String(required=True)
    birth_date = graphene.Date(required=True)
    token = graphene.Date(required=True)