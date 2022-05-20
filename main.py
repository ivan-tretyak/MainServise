"""
Routes and views for the flask application.
"""

from flask import Flask, abort
app = Flask(__name__)

from os import error

from werkzeug.exceptions import BadRequest
from MainServise import *
from flask import jsonify, request
import requests

from MainServise.utils import *
from MainServise.validate import validate_headers, validate_json, validate_json_urls
from MainServise.json import build_URL_from_client, to_dict, build_URL


@app.route('/classification', methods=["POST"])
def classification():
    """Main client route"""

    #validate client header and getting data
    validate_headers(request)
    try:
        data = request.json
        validate_json(data)
    except BadRequest:
        return create_error_response(400, "Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)")
    data_send = {'data':{}}
    #read urls txt
    urls =  read_json_file("urls.json")
    for url in urls:
        r = requests.post(url.link, headers=url.headers, json=data)
        if r.status_code == 200:
            data_send['data'][url.keywords_group] = r.json()['data']
        else:
            data_send['data'][url.keywords_group] = r.json()['error']
    return jsonify(data_send)

    

@app.route('/urls', methods=["GET"])
def urls():
    urls = read_json_file("urls.json")
    if request.method == "GET":
        return jsonify(to_dict(urls))


@app.route('/urls/<keywords_group>', methods=["GET", "PATCH"])
def get_urls_by_keywords_group(keywords_group):
    urls = read_json_file("urls.json")
    if request.method == "GET":
        for url in urls:
            if url.keywords_group == keywords_group:
                return jsonify(url.to_dict())
        abort(404)
    if request.method == "PATCH":
        validate_headers(request)
        validate_json_urls(request.json)
        for i in range(len(urls)):
            if urls[i].keywords_group == keywords_group:
                urls[i] = build_URL_from_client(request.json)
                new_json = to_dict(urls)
                with open('urls.json', 'w') as f:
                    json.dump(new_json, f)
        urls.append(build_URL_from_client(request.json))
        new_json = to_dict(urls)
        with open('urls.json', 'w') as f:
            json.dump(new_json, f)
        return jsonify(to_dict(read_json_file("urls.json")))

app.register_error_handler(404, resource_not_exists)
app.register_error_handler(500, server_error)
app.register_error_handler(405, method_is_not_allowed)
app.register_error_handler(400, handle_invalid_usage)
app.register_error_handler(validate.InvalidApiUsage, handle_invalid_usage)

if __name__ == "__main__":
    app.run()