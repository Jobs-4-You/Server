import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models import User as UserModel, Feature as FeatureModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("pwd_hash", "fixedOldJobValue", "fixedAlphaBeta")


class Feature(SQLAlchemyObjectType):
    class Meta:
        model = FeatureModel


class SignupUrl(graphene.ObjectType):
    url = graphene.String(required=True)
    token = graphene.String(required=True)
