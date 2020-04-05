import datetime
import json


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    if isinstance(o, datetime.date):
        return o.__str__()


def to_pretty_string(obj):
    return json.dumps(obj, indent=4, sort_keys=True, default=myconverter)


def pretty_print(obj):
    print(to_pretty_string(obj))
