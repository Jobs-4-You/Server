import json
from datetime import datetime

import graphene
from dateutil.parser import parse
from elasticsearch_dsl import Document, Q, Search
from flask import request

from j4u_api.config import config
from j4u_api.database import db_session
from j4u_api.database.connection import db_session
from j4u_api.database.models import Activity as ActivityModel
from j4u_api.gql.input_types import ActivityInput
from j4u_api.gql.types import Activity as ActivityType
from j4u_api.utils.auth import jwt_auth_required


def default(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime):
        return str(obj)
    raise TypeError("Not sure how to serialize %s" % (obj,))


def enrich(event, user):
    event["timestamp"] = datetime.now()
    event["ip"] = request.remote_addr
    event["user_agent"] = request.headers.get("User-Agent")
    event["user_id"] = user.id
    return event


class CreateActivity(graphene.Mutation):
    class Arguments:
        activity = ActivityInput(required=True)

    activity = graphene.Field(ActivityType)

    @jwt_auth_required
    def mutate(root, info, activity):
        activity = enrich(activity, info.context.user)

        res = ActivityModel(**activity)

        db_session.add(res)
        db_session.commit()

        return CreateActivity(activity=res)
