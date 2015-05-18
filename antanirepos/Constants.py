__author__ = 'admiral0'

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
