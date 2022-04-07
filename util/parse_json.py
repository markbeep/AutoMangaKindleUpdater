import json
import requests


def parse_json(fp):
    with open(fp, "r") as f:
        return json.load(f)


STATIC_URL = "https://markc.su/api/automangadownloader.json"


def fetch_json():
    js = requests.get(STATIC_URL).text
    return json.loads(js)
