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