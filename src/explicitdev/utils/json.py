import json


def pretty_dump(path, data, indent=2):
    with path.open(mode='w') as file:
        json.dump(data, file, indent=indent)
