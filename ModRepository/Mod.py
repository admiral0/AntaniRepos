__author__ = 'admiral0'
import os.path as path
import re
from .Exceptions import JsonNotValid, ModDoesNotExist, ModJsonDoesNotExist
from .ModRepositoryManager import mod_file_name, read_json


def validate_version(ver):
    assert type(ver) is str
    if not re.match(r'^[a-zA-Z_0-9\.\-()]+$', ver):
        return ['Version ' + ver + ' must match ^[a-zA-Z_0-9\.\-()]+$']
    return []


def validate_minecraft(mver, vv):
    if not type(mver) is list:
        return ['Minecraft version must be an array for version ' + vv]

    for mv in mver:
        if not re.match(r'^\d+\.\d+(\.\d+)?$', mv):
            return ['Minecraft version ' + mv + ' does not match ^\d+\.\d+(\.\d+)?$ pattern in version ' + vv]
    return []


def validate_versions(d, m):
    if not type(d) is dict:
        return ['Versions is not a dict!']
    error = []
    for ver in d.keys():
        for err in validate_version(ver):
            error.append(err)
        try:
            if not path.isfile(path.join(m.mod_dir, d[ver]['file'])):
                error.append('File ' + d[ver]['file'] + ' has not been found in mod folder:' + m.mod_dir)
        except KeyError:
            error.append('Key \'file\' is missing in version ' + ver)
        try:
            for err in validate_minecraft(d[ver]['minecraft'], ver):
                error.append(err)
        except KeyError:
            error.append('Key \'minecraft\' is missing in version ' + ver)
        if 'type' in d[ver]:
            if d[ver]['type'] not in ['universal', 'client', 'server']:
                error.append('Type for ver ' + ver + 'must be one of universal, client or server')
    return error


class Mod:
    _elements = {
        'author': {
            'type': str,
            'required': True,
            'validate': lambda val, m: [] if 0 < len(val) < 255 else ['Length of author must be between 0 and 255']
        },
        'description': {
            'type': str,
            'required': False,
            'validate': lambda val, m: [] if 0 == len(val) else ['Do not leave description empty!'],
        },
        'name': {
            'type': str,
            'required': True,
            'validate': lambda val, m: [] if 0 < len(val) < 255 else ['Length of the name must be between 0 and 255']

        },
        'url': {
            'type': str,
            'required': True,
            'validate': lambda val, m: [] if re.match(r'^https?:.*$', val) else ['Must be a link']
        },
        'versions': {
            'type': dict,
            'required': True,
            'validate': lambda val, m: validate_versions(val, m)
        }
    }

    def __init__(self, mod_path):
        if not path.isdir(mod_path):
            raise ModDoesNotExist(mod_path)
        self.mod_dir = mod_path
        self.json_path = path.join(mod_path, mod_file_name)
        if not path.isfile(self.json_path):
            raise ModJsonDoesNotExist(self.json_path)
        self.data = read_json(self.json_path)
        self.validate()
        self.slug = path.basename(mod_path)

    def validate(self):
        assert type(self.data) is dict
        errors = []
        for key in self._elements.keys():
            ck = self._elements[key]
            if key in self.data.keys():
                if type(self.data[key]) is ck['type']:
                    for err in ck['validate'](self.data[key], self):
                        assert type(err) is str
                        errors.append(err)
                else:
                    errors.append('Key ' + key + ' should be of type ' + str(ck['type']) + ' instead of '
                                  + str(type(self.data[key])))
            else:
                if ck['required']:
                    errors.append('Key ' + key + 'is required.')
        if len(errors) > 0:
            raise JsonNotValid(self.json_path, errors)

