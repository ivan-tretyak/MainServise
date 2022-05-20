import base64
from re import I

class InvalidApiUsage(Exception):
    """Exception class for validate JSON data."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

def validate_json(json):
    if json.get('data') is None:
        raise InvalidApiUsage("No field 'data'.")
    elif type(json['data']) != dict:
        raise InvalidApiUsage("Field 'data' is not subscriptable.")
    elif json['data'].get('type') is None:
        raise InvalidApiUsage("Object 'data' has not field type.")
    elif json['data']['type'] != 'image':
        raise InvalidApiUsage("Unknown data type.")
    elif json['data'].get('src') is None:
        raise InvalidApiUsage("Object 'data' has not field src.")
    elif type(json['data']['src']) != str:
        raise InvalidApiUsage("Field 'src' in object data is not string.")
    elif json['data'].get('decode') is None:
        raise InvalidApiUsage("Object 'data' has not decode field")

    elif type(json['data']['decode']) != str:
        raise InvalidApiUsage("Unknown decode type.")
    elif type(json['data']['src']) == str:
        try:
           valid = base64.b64encode(base64.b64decode(json['data']['src'])).decode(json['data']['decode']) == json['data']['src']
        except LookupError:
            raise InvalidApiUsage(f"Unknown encoding: {json['data']['decode']}.")
        except:
            valid = False
        if not valid:
            raise InvalidApiUsage("Data source is incorrect base64 string.")

def validate_json_urls(json):
    if json.get('data') is None:
        raise InvalidApiUsage("No field 'data'.")
    elif json.get('links') is None:
        raise InvalidApiUsage("No field 'links'.")
    
    elif json.get('data').get('type') is None:
        raise InvalidApiUsage("No subfield 'type' in 'data'.")
    elif json.get('data').get('language') is None:
        raise InvalidApiUsage("No subfield 'language' in 'data'.")
    elif json.get('data').get('headers') is None:
        raise InvalidApiUsage("No subfield 'headers' in 'data'.")
    elif json.get('data').get('keywords_group') is None:
        raise InvalidApiUsage("No subfield 'keywords_group' in 'data'.")
    
    elif type(json.get('data').get('type')) != str:
        raise InvalidApiUsage("Unknown type of field 'type'.")
    elif type(json.get('data').get('language')) != str:
        raise InvalidApiUsage("Unknown type of field 'language'.")
    elif type(json.get('data').get('headers')) != dict:
        raise InvalidApiUsage("Field headers is not subscriptable.")
    elif type(json.get('data').get('keywords_group')) != str:
        raise InvalidApiUsage("Unknown type of field 'keywords_group'.")
    elif type(json.get('links')) != str:
        raise InvalidApiUsage("Unknown type of field 'links'.")
    
    elif json.get('data').get('headers') != {'Accept': 'application/vnd.api+json', 'Content-Type': 'application/vnd.api+json'}:
        raise InvalidApiUsage("Unknown headers")

    elif type(json.get('data')) != dict:
        raise InvalidApiUsage("Field data is not subscriptable.")


def validate_headers(request):
    if request.headers.get('Content-Type', None) == 'application/vnd.api+json' and request.headers.get('Accept', None) == 'application/vnd.api+json':
        pass
    elif request.headers.get('Content-Type', None) == 'application/vnd.api+json' and request.mimetype_params != {}:
        raise InvalidApiUsage('Mimetype parametres is not empty.', 415)
    elif request.headers.get('Content-Type', None) == 'application/vnd.api+json' and request.headers.get('Accept', None) != 'application/vnd.api+json':
        raise InvalidApiUsage('Header \'Accept\' is not \'application/vnd.api+json\'', 415)
    else:
        raise InvalidApiUsage("Unknown access error", 415)