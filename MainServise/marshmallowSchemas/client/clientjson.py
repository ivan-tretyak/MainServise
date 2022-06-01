import base64
import typing
from dataclasses import dataclass
from PIL import Image
from io import BytesIO


from marshmallow import Schema, validate, ValidationError, fields, pre_load, post_load


@dataclass
class UserJSONDATA:
    type: str
    decode: str
    src: str


@dataclass
class UserJSON:
    data: UserJSONDATA


class ImageBase64(fields.Field):
    def _serialize(self, value: str, attr: str, obj: typing.Any, **kwargs):
        return value

    def _deserialize(self, value: str, attr: str, data, **kwargs):
        try:
            im = Image.open(BytesIO(base64.b64decode(value))).convert('RGB')
            im.save('test.jpg', format='JPEG')
            buffered = BytesIO()
            im.save(buffered, format='JPEG')
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except LookupError:
            raise ValidationError("Invalid decoding method.")
        except:
            raise ValidationError("Incorrect base64 string.")


class Data(Schema):
    type = fields.Str(validate=validate.OneOf(['image', 'Image']))
    src = ImageBase64(required=True)
    decode = fields.Str(validate=validate.OneOf(['utf-8']))

    @post_load
    def make_UserDataJSON(self, data, **kwargs):
        return UserJSONDATA(**data)


class JSON(Schema):
    data = fields.Nested(Data())

    @post_load
    def make_UserJSON(self, data, **kwargs):
        return UserJSON(**data)

def validate_user_json(json: dict) -> UserJSON:
    schema = JSON()
    try:
        user_json = schema.load(json)
    except ValidationError as err:
        return err.messages
    return user_json

if __name__ == "__main__":
    result = validate_user_json({'data':{'type':'image', 'decode':'utf-8', 'src':'test'}})
    print(result)
