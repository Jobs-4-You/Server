import jwt
import graphene
import flask
from datetime import datetime, timedelta
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql import GraphQLError
from mysql_db.models import User as UserModel, Features as FeaturesModel
from config import config
from .errors import UserNotFound, InvalidPassword


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("pwd_hash", "fixedOldJobValue", "fixedAlphaBeta")


class Features(SQLAlchemyObjectType):
    class Meta:
        model = FeaturesModel


def get_token(user_id, exp_time=3600):
    exp = datetime.utcnow() + timedelta(seconds=exp_time)
    return jwt.encode(
        {"user_id": user_id, "exp": exp}, config.JWT_KEY, algorithm="HS256"
    ).decode()


def extract_token(token):
    return jwt.decode(token, config.JWT_KEY, algorithm="HS256")


def get_identity():
    return flask.g.user_id


def jwt_auth_required(func):
    def inner1(*args, **kwargs):
        token = args[1].context.headers.get("accessToken")
        user_id = extract_token(token)["user_id"]
        flask.g.user_id = user_id
        return func(*args, **kwargs)

    return inner1


def resolve_all_users(parent, info, user_id):
    query = User.get_query(info)  # SQLAlchemy query
    return query.all()


@jwt_auth_required
def resolve_me(parent, info):
    user_id = get_identity()
    return UserModel.query.filter(UserModel.id == user_id).first()


class Query(graphene.ObjectType):
    all_users = graphene.List(User, resolver=resolve_all_users)
    me = graphene.Field(User, resolver=resolve_me)


class Auth(graphene.Mutation):
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
        return Auth(access_token=token, refresh_token="")


class Mutation(graphene.ObjectType):
    auth = Auth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
