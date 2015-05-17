__author__ = 'admiral0'
import os.path as path
from os import walk
import json
import re
from .Exceptions import JsonNotValid, RepositoryDirectoryDoesNotExist, RepositoryDoesNotHaveMetaJson

mod_file_name = 'mod.json'


def read_json(file):
    try:
        with open(file) as meta_data:
            data = json.load(meta_data)
            return data
    except ValueError:
        raise JsonNotValid(file, ['Cannot parse. Is it a valid JSON file?'])


class ModRepository:
    _metaname = 'meta.json'

    def __init__(self, repopath):
        if not path.isdir(repopath):
            raise RepositoryDirectoryDoesNotExist(repopath)
        if not path.isfile(path.join(repopath, self._metaname)):
            raise RepositoryDoesNotHaveMetaJson(path.join(repopath, self._metaname))
        self.repo = repopath
        self.metadata = read_json(path.join(repopath, self._metaname))
        self.validate()

    def validate(self):
        errors = []
        if 'authors' not in self.metadata:
            errors.append('Does not contain authors property')
        else:
            if not type(self.metadata['authors']) is list:
                errors.append('authors is not a list')
            else:
                for author in self.metadata['authors']:
                    if not type(author) is str:
                        errors.append(str(author) + ' is not a string')
                    else:
                        if not re.match(r'^.+?@.+?\..+?$', author):
                            errors.append(author + ' must be an email')
        if len(errors) > 0:
            raise JsonNotValid(path.join(self.repo, self._metaname), errors)

    def list_mods(self):
        mods = {}
        for (mod_path, dirs, files) in walk(self.repo):
            if mod_file_name in files:
                mods[path.basename(mod_path)] = mod_path
        return mods
