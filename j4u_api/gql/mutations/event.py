import json
from datetime import datetime

import graphene
from dateutil.parser import parse
from elasticsearch_dsl import Document, Q, Search
from flask import request

from j4u_api.config import config
from j4u_api.elastic_db import Event as EventModel
from j4u_api.gql.input_types import EventInput
from j4u_api.gql.types import Event as EventType
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


def create_session_time(event):
    id = f'{event["timestamp"]}:{event["user_id"]}:{event["ip"]}'
    payload = {"start": event["timestamp"], "end": event["timestamp"]}
    event["type"] = "SESSION_TIME"
    x = EventModel(meta={"id": id}, **event, payload=payload)
    x.save()
    return x


def update_session_time(last, event):
    e = EventModel.get(id=last.meta.id)
    e.payload["end"] = event["timestamp"]
    e.timestamp = last.timestamp
    a = e.save()
    return e


def create_event(event):
    id = f'{event["timestamp"]}:{event["user_id"]}:{event["ip"]}'
    x = EventModel(meta={"id": id}, **event)
    x.save()
    return x


def handle_session_time(event):
    query = (
        Q("match", user_id=event["user_id"])
        & Q("match", ip=event["ip"])
        & Q("match", type="SESSION_TIME")
    )
    s = EventModel.search().query(query).sort({"timestamp": {"order": "desc"}})
    res = s.execute()
    if len(res) == 0:
        return create_session_time(event)
    else:
        last = res[0]
        seconds_diff = (event["timestamp"] - parse(last.payload["end"])).total_seconds()
        if seconds_diff <= int(config.HEARTBEAT_MAX_INTERVAL):
            return update_session_time(last, event)
        else:
            return create_session_time(event)


class CreateEvent(graphene.Mutation):
    class Arguments:
        event = EventInput(required=True)

    event = graphene.Field(EventType)

    @jwt_auth_required
    def mutate(root, info, event):
        event = enrich(event, info.context.user)
        res = None
        if event["type"] == "HEARTBEAT":
            res = handle_session_time(event)
        else:
            res = create_event(event)
        res.id = res.meta.id
        res.payload = json.dumps(res.payload.to_dict(), default=default)
        return CreateEvent(event=res)
