__author__ = 'admiral0'

from .Exceptions import JsonNotValid as JsonError
import json

mod_file_name = 'mod.json'

minecraft_version_regex = r'^\d+\.\d+(\.\d+)?$'
url_regex = r'^https?:.*$'


def validate(entities, json, obj):
    assert type(entities) is dict
    assert type(json) is dict
    errors = []
    for key in entities.keys():
        ck = entities[key]
        if key in json.keys():
            if type(json[key]) is ck['type']:
                for err in ck['validate'](json[key], obj):
                    assert type(err) is str
                    errors.append(err)
            else:
                errors.append('Key ' + key + ' should be of type ' + str(ck['type']) + ' instead of '
                              + str(type(json[key])))
        else:
            if ck['required']:
                errors.append('Key ' + key + ' is required.')
    return errors


def read_json(file):
    try:
        with open(file) as meta_data:
            data = json.load(meta_data)
            return data
    except ValueError:
        raise JsonError(file, ['Cannot parse. Is it a valid JSON file?'])