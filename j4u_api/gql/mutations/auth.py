import graphene

from j4u_api.database.models import User as UserModel
from j4u_api.errors.auth_errors import InvalidPassword, UserNotFound
from j4u_api.utils.token import create_auth_token


class Auth(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(root, info, email, password):
        user = UserModel.query.filter(UserModel.email == email).first()
        if user is None:
            raise UserNotFound(email)
        if not user.check_password(password):
            raise InvalidPassword(email)

        access_token = create_auth_token(user.id)
        return Auth(access_token=access_token, refresh_token="refresh")
