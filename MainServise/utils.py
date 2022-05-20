import flask
from flask import jsonify
import json

from sympy import im

from MainServise import validate
from MainServise import json as my_json


def create_response(status_code, message={}):
    response = flask.make_response(jsonify(message), status_code)
    response.headers['Content-Type'] = 'application/vnd.api+json'
    return response


def create_error_response(status_code, error):
    return create_response(status_code, {'error': str(error)})


def resource_not_exists(e):
    print(e)
    """Returns a handled exception for a 404 error."""
    return create_error_response(404, e)


def server_error(e):
    """Returns a handled exception for a 500 error."""
    return create_error_response(500, e)


def method_is_not_allowed(e):
    """Returns a handled exception for a 405 error."""
    return create_error_response(405, e)


def handle_invalid_usage(error: validate.InvalidApiUsage):
    """Returns handled exception for error 400."""
    return create_error_response(400, error.message)

from typing import Dict, List


def read_file_txt(path: str) -> List[str]:
    lines: List[str] = []
    with open(path) as f:
        for line in f:
            lines.append(line.replace('\n', ''))
    return lines

def read_json_file(path: str) -> List[my_json.URL]:
    with open(path) as f:
        jsons = json.load(f)
    return my_json.build_URL(jsons)
