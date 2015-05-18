__author__ = 'admiral0'

from os import path
import re
from .Exceptions import RepositoryDirectoryDoesNotExist
from .Exceptions import JsonNotValid
from .Exceptions import RepositoryDoesNotHaveMetaJson
from .Exceptions import ModDoesNotExistInRepo, ModVersionDoesNotExistInRepo
from .Exceptions import BranchDoesNotExist, TagDoesNotExist
from .ModRepository import read_json
from .ModRepository import ModManager
from .Constants import minecraft_version_regex, url_regex, validate
import pygit2


def validate_mods(x, m):
    errors = []
    for key in x:
        if type(key) is not str:
            errors.append('Key ' + str(key) + ' must be a string in "mods"')
        if type(x[key]) is not str:
            errors.append('Value' + str(x[key]) + ' must be a string in "mods"')


class PackRepository:
    _modpack_file = 'modpack.json'
    _entities = {
        'description': {
            'required': True,
            'type': str,
            'validate': lambda x, m: []
        },
        'forgever': {
            'required': True,
            'type': str,
            'validate':
                lambda x, m: [] if re.match(r'^\d+\.\d+\.\d+\.\d+$', x) else [x + ' is not a valid forge version']
        },
        'mcversion': {
            'required': True,
            'type': str,
            'validate':
                lambda x, m: [] if re.match(minecraft_version_regex, x) else [x + ' is not a valid minecraft version']
        },
        'url': {
            'required': True,
            'type': str,
            'validate':
                lambda x, m: [] if re.match(url_regex, x) else [x + ' is not a valid URL']
        },
        'version': {
            'required': True,
            'type': str,
            'validate':
                lambda x, m: [] if re.match(r'^[0-9\.\-_a-z]+$', x) else [x + ' is not a valid version']
        },
        'mods': {
            'required': True,
            'type': dict,
            'validate': validate_mods
        }
    }

    def __init__(self, repopath, modrepo=None):
        if not path.isdir(repopath):
            raise RepositoryDirectoryDoesNotExist(repopath)
        self.json = path.join(repopath, self._modpack_file)
        if not path.isfile(self.json):
            raise RepositoryDoesNotHaveMetaJson(self.json)
        # TODO Configless and default assets
        self.repo_dir = repopath
        self.data = read_json(self.json)
        self.validate()
        self.modrepo = modrepo
        if modrepo is not None:
            self.validate_semantic()

    def validate(self):
        assert type(self.data) is dict
        err = validate(self._entities, self.data, self)
        if len(err) > 0:
            raise JsonNotValid(self.json, err)

    def validate_semantic(self):
        assert type(self.modrepo) is ModManager
        errors = []
        for name, version in self.data['mods'].items():
            try:
                m = self.modrepo.get_mod(name)
                m.get_version(version)
            except ModDoesNotExistInRepo:
                errors.append('Mod ' + name + ' does not exist in repo')
            except ModVersionDoesNotExistInRepo:
                errors.append('Version ' + version + ' of mod ' + name + ' is not in the repo.')
        if len(errors) > 0:
            raise JsonNotValid(self.json, errors)
