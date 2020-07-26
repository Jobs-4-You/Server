from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

import j4u_api.database.models as models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        exclude_fields = ("password_hash",)


class Feature(SQLAlchemyObjectType):
    class Meta:
        model = models.Feature


class FeatureConfig(SQLAlchemyObjectType):
    class Meta:
        model = models.FeatureConfig


class Group(SQLAlchemyObjectType):
    class Meta:
        model = models.Group


class UICongif(SQLAlchemyObjectType):
    class Meta:
        model = models.UIConfig


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


class JobSearchHint(graphene.ObjectType):
    id = graphene.ID(required=True)
    avam = graphene.Int(required=True)
    bfs = graphene.Int(required=True)
    isco08 = graphene.Int(required=True)
    title = graphene.String(required=True)
    isco_title = graphene.String(required=True)

    def resolve_title(parent, info):
        return parent["title"].title()


class JobRoomCompany(graphene.ObjectType):
    name = graphene.String()
    city = graphene.String()
    street = graphene.String()
    postal_code = graphene.Int()
    house_number = graphene.String()
    country_code = graphene.String()


class JobRoomEmployment(graphene.ObjectType):
    start_date = graphene.Date()
    end_date = graphene.Date()
    short = graphene.String()
    immediately = graphene.Boolean()
    permanent = graphene.Boolean()
    workload_perc_min = graphene.Int()
    workload_perc_max = graphene.Int()

    def resolve_start_date(parent, root):
        start_date = parent["start_date"]
        if start_date is not None:
            return datetime.strptime(start_date, "%Y-%m-%d").date()
        return start_date

    def resolve_end_date(parent, root):
        end_date = parent["end_date"]
        if end_date is not None:
            return datetime.strptime(end_date, "%Y-%m-%d").date()
        return end_date


class JobRoomLocation(graphene.ObjectType):
    city = graphene.String()
    country_code = graphene.String()
    canton_code = graphene.String()


class JobRoomContact(graphene.ObjectType):
    salutation = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()
    email = graphene.String()


class JobRoomDescription(graphene.ObjectType):
    language_code = graphene.String()
    title = graphene.String()
    description = graphene.String()


# TODO better parsing
class JobRoomPosition(graphene.ObjectType):
    id = graphene.ID(required=True)
    job_quantity = graphene.Int()
    external_url = graphene.String()
    language = graphene.String()
    descriptions = graphene.List(JobRoomDescription)
    company = graphene.Field(JobRoomCompany)
    employment = graphene.Field(JobRoomEmployment)
    location = graphene.Field(JobRoomLocation)
    contact = graphene.Field(JobRoomContact)


class PostionsResult(graphene.ObjectType):
    id = graphene.ID(required=True)
    total_count = graphene.Int(required=True)
    positions = graphene.List(JobRoomPosition, required=True)


class IndividuaJobRecommendation(graphene.ObjectType):
    isco08 = graphene.Int(required=True)
    avam = graphene.Int(required=True)
    bfs = graphene.Int(required=True)
    job_title = graphene.String(required=True)


class RecommendationResult(graphene.ObjectType):
    id = graphene.ID(required=True)
    var_list = graphene.List(graphene.Float, required=True)
    importances = graphene.List(graphene.Float, required=True)
    results = graphene.List(IndividuaJobRecommendation, required=True)


class Event(graphene.ObjectType):
    id = graphene.ID(required=True)
    timestamp = graphene.DateTime(required=True)
    user_agent = graphene.String(required=True)
    ip = graphene.String(required=True)
    type = graphene.String(required=True)
    user_id = graphene.Int(required=True)
    user = graphene.Field(User)
    payload = graphene.JSONString()

    def resolve_user(parent, info):
        return models.User.query.get(parent.user_id)


class DatetimeJob(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    state = graphene.String(required=True)
    action = graphene.String(required=True)
    params = graphene.JSONString(required=True)
    creation_date = graphene.DateTime(required=True)
    execution_date = graphene.DateTime(required=True)
    executed_date = graphene.DateTime()
