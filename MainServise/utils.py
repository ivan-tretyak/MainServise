from typing import List
import json

from MainServise.marshmallowSchemas.admin.url import *


def read_json_file() -> List:
    with open('url.json') as f:
        jsons = json.load(f)
    return jsons


def add_new_link_to_url(jsons, url: URL, key):
    jsons['links'][key] = url.data.link
    jsons['data'][key] = {}
    jsons['data'][key]['type'] = url.data.type
    jsons['data'][key]['language'] = url.data.language
    jsons['data'][key]['keywords_group'] = url.data.keywords_group
    return jsons


def save_json(path, jsons):
    with open(path, 'w') as outfile:
        json.dump(jsons, outfile)
