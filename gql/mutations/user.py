import jwt
import graphene
from database.models import User as UserModel
from gql.input_types import UserInput
from gql.types import User
from gql.errors import InvalidSignupLink, ExpiredSignupLink
from utils.token import extract_from_token
from utils.mail import send_mail
from config import config


class CreateUser(graphene.Mutation):
    class Arguments:
        user = UserInput(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate(root, info, user, token):
        try:
            group = extract_from_token(token)["group"]
        except jwt.DecodeError:
            raise InvalidSignupLink().error
        except jwt.ExpiredSignatureError:
            raise ExpiredSignupLink().error

        new_user = UserModel(**user, group=group)
        print(new_user)
        send_mail(
            to=[new_user.email],
            subject="J4U verification du compte",
            template="verification",
            link=f"{config.APP_URL}/verify",
        )

        return CreateUser(user=None)
