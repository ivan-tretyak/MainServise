"""
Routes and views for the flask application.
"""

from os import error

from werkzeug.exceptions import BadRequest
from MainServise import *
from flask import jsonify, request
import requests

from MainServise.utils import *
from MainServise.validate import validate_json


@app.route('/classification', methods=["POST"])
def classification():
    """Main client route"""

    #validate client header and getting data
    if request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers.get('Accept', None) == 'application/vnd.api+json':
        try:
            data = request.json
            validate_json(data)
        except BadRequest:
            return create_error_response(400, "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)")

        #read urls txt
        urls =  read_file_txt("urls.txt")
        for url in urls:
            header = {"Content-Type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}
            r = requests.post(url, headers=header, json=data)
        return jsonify(r.json())

    elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.mimetype_params != {}:
        return create_error_response(415, 'Mimetype parametres is not empty.')
    elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers.get('Accept', None) != 'application/vnd.api+json':
        return create_error_response(415, 'Header \'Accept\' is not \'application/vnd.api+json\'')
    else:
        return create_error_response(415, "Unknown access error")

app.register_error_handler(404, resource_not_exists)
app.register_error_handler(500, server_error)
app.register_error_handler(405, method_is_not_allowed)
app.register_error_handler(400, handle_invalid_usage)
app.register_error_handler(validate.InvalidApiUsage, handle_invalid_usage)