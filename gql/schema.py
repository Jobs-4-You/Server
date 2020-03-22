import graphene
import flask
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql import GraphQLError
from database.models import User as UserModel,  Feature as FeatureModel
from config import config
from .errors import UserNotFound, InvalidPassword
from lib.auth import get_token, get_user, jwt_auth_required, roles_required
from database.enums import RoleEnum
from .mutations import Auth


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("pwd_hash", "fixedOldJobValue", "fixedAlphaBeta")


class Features(SQLAlchemyObjectType):
    class Meta:
        model = FeatureModel


def resolve_all_users(parent, info, user_id):
    query = User.get_query(info)  # SQLAlchemy query
    return query.all()


@jwt_auth_required
def resolve_me(parent, info):
    return get_user()


class Query(graphene.ObjectType):
    all_users = graphene.List(User, resolver=resolve_all_users)
    me = graphene.Field(User, resolver=resolve_me)


class Mutation(graphene.ObjectType):
    auth = Auth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
