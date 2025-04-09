import json
import socket


def json_default(o):
    if hasattr(o, '__dict__'):
        return o.__dict__
    return str(o)

def to_json_recursive(o):
    return json.dumps(o, default=json_default)

def check_internet_connection() -> bool:
    remote_server = "www.google.com"
    port = 80
    status = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.5)
    try:
        sock.connect((remote_server, port))
        status = True
    except socket.error:
        status = False
    finally:
        sock.close()
        return status