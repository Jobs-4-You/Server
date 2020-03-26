import graphene
from database.models import User as UserModel
from utils.auth import get_token
from gql.errors import UserNotFound, InvalidPassword


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(root, info, email, password):
        user = UserModel.query.filter(UserModel.email == email).first()
        if user is None:
            raise UserNotFound(email).error
        if not user.check_password(password):
            raise InvalidPassword(email).error

        access_token = get_token(user.id)
        return Auth(access_token=access_token, refresh_token="")
