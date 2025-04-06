import json


def json_default(o):
    if hasattr(o, '__dict__'):
        return o.__dict__
    return str(o)

def to_json_recursive(o):
    return json.dumps(o, default=json_default)