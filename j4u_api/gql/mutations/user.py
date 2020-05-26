import graphene
import jwt
from sqlalchemy.exc import SQLAlchemyError

import j4u_api.errors.token_errors as token_errors
from j4u_api.config import config
from j4u_api.database import db_session
from j4u_api.database.models import Group as GroupModel
from j4u_api.database.models import User as UserModel
from j4u_api.errors.qulatrics_errors import ContactAlreadyExists
from j4u_api.gql.input_types import UserInput
from j4u_api.gql.types import User
from j4u_api.qualtrics import qual_client
from j4u_api.utils.errors import parse_db_error
from j4u_api.utils.mail import send_mail
from j4u_api.utils.token import create_auth_token, extract_from_token


class CreateUser(graphene.Mutation):
    class Arguments:
        user = UserInput(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate(root, info, user, token):
        try:
            group_id = extract_from_token(token)["group_id"]
        except jwt.DecodeError:
            raise token_errors.InvalidSignupLink()
        except jwt.ExpiredSignatureError:
            raise token_errors.ExpiredSignupLink()

        try:
            group = GroupModel.query.filter(GroupModel.id == group_id).first()
            new_user = UserModel(**user, group=group)
            db_session.add(new_user)
            db_session.flush()

            verification_token = create_auth_token(new_user.id, 3600 * 24 * 1)
            verification_url = f"{config.APP_URL}/verify?token={verification_token}"

            send_mail(
                to=[new_user.email],
                subject="J4U verification du compte",
                template="verification",
                link=verification_url,
            )
            qual_client.create_contact(new_user.email)
            db_session.commit()
            return CreateUser(user=new_user)

        except SQLAlchemyError as err:
            error = parse_db_error(err)
            raise error
        except ContactAlreadyExists as err:
            raise err
        except Exception as err:
            raise err


class VerifyUser(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    verified = graphene.Boolean()

    def mutate(root, info, token):
        try:
            user_id = extract_from_token(token)["user_id"]
        except jwt.DecodeError:
            raise token_errors.InvalidVerificationLink()
        except jwt.ExpiredSignatureError:
            raise token_errors.ExpiredVerificationLink()

        user = UserModel.query.filter(UserModel.id == int(user_id)).first()
        user.verified = True
        db_session.add(user)
        db_session.commit()

        return VerifyUser(verified=True)
