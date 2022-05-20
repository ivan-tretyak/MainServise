from re import U
from typing import Dict, List


class URL:
    def __init__(self, type: str, lang: str, keywords_group: str, headers: Dict[str, str], link: str):
        self.type = type
        self.language = lang
        self.keywords_group = keywords_group
        self.headers = headers
        self.link = link

    def to_dict(self) -> Dict[str, str]:
        dictionary = {"links":{},
                  "data": {}}

        dictionary['links'][self.keywords_group] = self.link
        dictionary['data'][self.keywords_group] = {}
        dictionary['data'][self.keywords_group]['type'] = self.type
        dictionary['data'][self.keywords_group]['language'] = self.language
        dictionary['data'][self.keywords_group]['headers'] = self.headers
        dictionary['data'][self.keywords_group]['keywords_group'] = self.keywords_group
        return dictionary
        

def to_dict(urls: List[URL]) -> Dict[str, str]:
    dictionary = {"links":{},
                  "data": {}}

    for url in urls:
        dictionary['links'][url.keywords_group] = url.link

        dictionary['data'][url.keywords_group] = url.to_dict()['data'][url.keywords_group]
    return dictionary

def build_URL(json: dict):
    links, data = json['links'], json['data']
    urls: List[URL] = []
    for key in links:
        url = URL(data[key]['type'], data[key]['language'],
                data[key]['keywords_group'], data[key]['headers'],
                links[key])

        urls.append(url)
    return urls

def build_URL_from_client(json: dict):
    return URL(json['data']['type'], json['data']['language'],
                json['data']['keywords_group'], json['data']['headers'],
                json['links'])