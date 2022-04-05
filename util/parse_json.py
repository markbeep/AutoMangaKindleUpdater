import json


def parse_json(fp):
    with open(fp, "r") as f:
        return json.load(f)