import json
from html.parser import HTMLParser


class Validator(HTMLParser):
    def error(self, message):
        raise ValueError(message)


def validate_html(html: str):
    parser = Validator()
    parser.feed(html)


def validate_json(obj):
    json.dumps(obj)
