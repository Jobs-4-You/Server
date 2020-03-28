import jwt
import graphene
from database import db_session
from database.models import User as UserModel
from gql.input_types import UserInput
from gql.types import User
from gql.errors.token_errors import *
from utils.token import extract_from_token, create_auth_token
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
        db_session.add(new_user)
        db_session.commit()

        verification_token = create_auth_token(new_user.id)
        verification_url = f"{config.APP_URL}/verify?token={verification_token}"

        send_mail(
            to=[new_user.email],
            subject="J4U verification du compte",
            template="verification",
            link=verification_url,
        )

        from utils.print import pretty_print

        user_dict = new_user.to_dict()
        pretty_print(user_dict)
        del user_dict["password_hash"]
        return CreateUser(user=User(**user_dict))


class VerifyUser(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    verified = graphene.Boolean()

    def mutate(root, info, token):
        try:
            user_id = extract_from_token(token)["user_id"]
        except jwt.DecodeError:
            raise InvalidVerificationLink().error
        except jwt.ExpiredSignatureError:
            raise ExpiredVerificationLink().error

        user = UserModel.query.filter(UserModel.id == user_id).first()
        user.verified = True
        db_session.add(user)
        db_session.commit()

        return VerifyUser(verified=True)
