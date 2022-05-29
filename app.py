"""
Routes and views for the flask application.
"""

from flask import Flask, abort

from MainServise.marshmallowSchemas.admin.url import URLSchema

app = Flask(__name__)

from werkzeug.exceptions import BadRequest
from flask import jsonify, request
import requests

from MainServise import utils
from MainServise.marshmallowSchemas.client.clientjson import *
from MainServise.marshmallowSchemas.client.headers import *
import os

@app.errorhandler(400)
def incorrect_api_usage(e):
    return jsonify({'error': e}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error':  'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/classification', methods=["POST"])
def classification():
    headersSchema = Headers()
    userJSON = JSON()
    ansa = {'data':{}}
    try:
        headersSchema.load(request.headers)
        user_json = validate_user_json(request.json)
        if type(user_json) != UserJSON:
            return incorrect_api_usage(user_json)
        urls = utils.read_json_file()
        data, links = urls['data'], urls['links']
        header = {'Content-Type':'application/json', 'Accept':'application/json'}
        for link in links:
            url = links[link]
            print(type(request.json))
            ans = requests.post(url, headers=header, json=request.json)
            print(ans.json())
            ansa['data'][link] = ans.json()
        return ansa

    except ValidationError as err:
        abort(400, descritpiton=err.messages)
    except BadRequest:
        return jsonify({'error': "JSON wasn't send."}), 400


@app.route('/url', methods=['GET'])
def url():
    print(os.path.exists('url.json'))
    print(os.getcwd())
    return jsonify(utils.read_json_file())

def exist_url(keywords_group, request):
    try:
        jsons = utils.read_json_file()
        ans = {'data': {}}
        ans['data']['link'] = jsons['links'][keywords_group]
        ans['data']['type'] = jsons['data'][keywords_group]['type']
        ans['data']['keywords_group'] = jsons['data'][keywords_group]['keywords_group']
        ans['data']['language'] = jsons['data'][keywords_group]['language']
        return jsonify(ans)
    except KeyError:
        abort(404)
    except:
        abort(500)


def update_url(keywords_group, request):
    try:
        urlsch = URLSchema()
        jsons = request.json
        url = urlsch.load(jsons)
        jsons = utils.read_json_file()
        jsons = utils.add_new_link_to_url(jsons, url, keywords_group)
        utils.save_json('url.json', jsons)
        return jsonify(utils.read_json_file())
    except ValidationError as err:
        return incorrect_api_usage(err.messages)
    except KeyError:
        abort(404)
    except:
        abort(500)


@app.route('/url/<keywords_group>', methods=['GET', 'PATCH'])
def urlsnew(keywords_group):
    methods = {"GET": exist_url, 'PATCH': update_url}
    return methods[request.method](keywords_group, request)

if __name__ == "__main__":
    app.run()