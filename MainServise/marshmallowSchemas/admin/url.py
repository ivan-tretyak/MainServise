from dataclasses import dataclass
from marshmallow import Schema, fields, validate, ValidationError, pre_load, post_load

@dataclass
class URLData:
    type: str
    language: str
    keywords_group: str
    link: str


@dataclass
class URL:
    data: URLData


class URLDataSchema(Schema):
    type = fields.Str(required=True)
    language = fields.Str(required=True)
    keywords_group = fields.Str(required=True)
    link = fields.Url(required=True)

    @post_load
    def make_URLData(self, data, **kwargs):
        return URLData(**data)


class URLSchema(Schema):
    data = fields.Nested(URLDataSchema())

    @post_load
    def make_Url(self, data, **kwargs):
        return URL(**data)


if __name__ == "__main__":
    import json

    new_count = {'data': {'keywords_group': 'group photo',
                          'language': 'en-US',
                          'link': 'https://imageclassificationtretyak.herokuapp.com',
                          'type': 'group photo'}}
    urlsch = URLSchema()
    with open('url.json') as f:
        jsons = json.load(f)
    print(jsons)
    url = urlsch.load(new_count)
    jsons['links'][url.data.keywords_group] = url.data.link
    jsons['data'][url.data.keywords_group] = {}
    jsons['data'][url.data.keywords_group]['type'] = url.data.type
    jsons['data'][url.data.keywords_group]['language'] = url.data.language
    jsons['data'][url.data.keywords_group]['keywords_group'] = url.data.keywords_group
    print(jsons)

