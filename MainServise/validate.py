import base64


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
