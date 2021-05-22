import ndjson
from pprint import pprint
import os

def join_to_main_path(filename) -> str:
    path = os.path.join('./data', filename)
    return path

def read_file(filename):
    data = None
    with open(join_to_main_path(filename)) as f:
        data = ndjson.load(f)
    return data

data = read_file('example_no_subdata.ndjson')
pprint(data, indent=3)