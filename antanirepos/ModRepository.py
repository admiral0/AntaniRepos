__author__ = 'admiral0'
import os.path as path
from os import walk
from .Common import read_json, mod_file_name
import re
from .Exceptions import JsonNotValid, RepositoryDirectoryDoesNotExist, RepositoryDoesNotHaveMetaJson, ModDoesNotExistInRepo
from .Mod import Mod


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


class ModManager(ModRepository):
    mods = {}

    def __init__(self, repopath):
        super().__init__(repopath)
        self.mods_lazy = self.list_mods()

    def get_mod(self, name):
        if name not in self.mods.keys():
            if name in self.mods_lazy.keys():
                self.mods[name] = Mod(self.mods_lazy[name])
            else:
                raise ModDoesNotExistInRepo(name)
        return self.mods[name]
