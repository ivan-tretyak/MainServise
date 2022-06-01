from marshmallow import Schema, validate, ValidationError, fields, pre_load


class Headers(Schema):
    ContentType = fields.Str(validate=validate.OneOf(['application/vnd.api+json', 'application/json']), required=True)
    Accept = fields.Str(validate=validate.OneOf(['application/vnd.api+json', 'application/json']), required=True)

    @pre_load
    def test(self, data: dict, **kwargs):
        new_data = {}
        try:
            new_data["ContentType"] = data["Content-Type"]
        except KeyError:
            raise ValidationError("Miss http-headers Content-Type")
        try:
            new_data["Accept"] = data["Accept"]
        except KeyError:
            raise ValidationError("Miss http-headers Accept")
        return new_data

def validate_headers(get_headers: dict) -> None:
    schema = Headers()
    try:
        headers = schema.load(get_headers)
        return None
    except ValidationError as err:
        return err.messages


if __name__ == "__main__":
    headers = Headers()
    try:
        headers.load({"Contessnt-Type": "application/json", "Accepst": "application/json"})
    except ValidationError as err:
        print(err.messages)

