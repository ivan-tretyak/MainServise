from marshmallow import Schema, validate, ValidationError, fields, pre_load


class Headers(Schema):
    ContentType = fields.Str(validate=validate.OneOf(['application/vnd.api+json', 'application/json']), required=True)
    Accept = fields.Str(validate=validate.OneOf(['application/vnd.api+json', 'application/json']), required=True)

    @pre_load
    def test(self, data: dict, **kwargs):
        new_data = {"ContentType": data["Content-Type"],
                    "Accept": data["Accept"]}
        return new_data


if __name__ == "__main__":
    headers = Headers()
    try:
        headers.load({"Content-Type": "applicationss/json", "Accept": "application/json"})
    except ValidationError as err:
        print(err.messages)

