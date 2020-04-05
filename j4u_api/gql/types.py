import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from database.models import Feature as FeatureModel
from database.models import Group as GroupModel
from database.models import User as UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password_hash",)


class Feature(SQLAlchemyObjectType):
    class Meta:
        model = FeatureModel


class Group(SQLAlchemyObjectType):
    class Meta:
        model = GroupModel


class SignupUrl(graphene.ObjectType):
    url = graphene.String(required=True)
    token = graphene.String(required=True)


class SurveyMeta(graphene.ObjectType):
    id = graphene.ID(required=True)
    creation_date = graphene.DateTime(required=True)
    last_modified = graphene.DateTime(required=True)
    is_active = graphene.Boolean(required=True)
    name = graphene.String(required=True)
    owner_id = graphene.ID(required=True)
