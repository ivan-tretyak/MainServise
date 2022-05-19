import flask
from flask import jsonify

import MainServise


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


def handle_invalid_usage(error: MainServise.):
    """Returns handled exception for error 400."""
    return create_error_response(400, error.message)