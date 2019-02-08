import json
from os.path import join, split


def get_file_from_test_resource(filename):
    return join(split(__file__)[0], "resources", filename)


def read_json_from_file(filename):
    with open(get_file_from_test_resource(filename)) as json_file:
         return json.loads(json_file.read())
