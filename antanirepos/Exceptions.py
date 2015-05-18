__author__ = 'admiral0'


class RepositoryDirectoryDoesNotExist(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'The mod repository does not exist. Missing directory:' + self.path


class RepositoryDoesNotHaveMetaJson(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path + ' doesn\'t exist.'


class JsonNotValid(Exception):
    def __init__(self, file, errors):
        assert type(errors) is list
        self.errors = errors
        self.file = file

    def __str__(self):
        err = 'Cannot parse ' + self.file + ". Reasons:\n"
        for error in self.errors:
            err += "\t" + error + "\n"
        return err


class ModDoesNotExist(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'Mod directory doesn\'t exist:' + self.path


class ModJsonDoesNotExist(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'Mod.json doesn\'t exist:' + self.path


class ModDoesNotExistInRepo(Exception):
    def __init__(self, mod):
        self.name = mod

    def __str__(self):
        return 'Mod ' + self.name + ' has not been found in mod repository.'


class ModVersionDoesNotExistInRepo(Exception):
    def __init__(self, mod, ver):
        self.name = mod
        self.ver = ver

    def __str__(self):
        return 'Version ' + self.ver + ' of mod ' + self.name + ' has not been found in mod repository.'


class BranchDoesNotExist(Exception):
    def __init__(self, br):
        self.name = br

    def __str__(self):
        return 'Branch ' + self.name + ' has not been found in pack repository.'


class TagDoesNotExist(Exception):
    def __init__(self, br):
        self.name = br

    def __str__(self):
        return 'Branch ' + self.name + ' has not been found in pack repository.'


class RefHasErrors(Exception):
    def __init__(self, ref, exceptions):
        self.name = ref
        self.exc = exceptions

    def __str__(self):
        str_exc = self.name + ' has exceptions:'
        for e in self.exc:
            str_exc += str_exc(e)
        return str_exc