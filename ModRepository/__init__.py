__author__ = 'admiral0'

from .ModRepositoryManager import ModRepository
from .Mod import Mod


class ModManager(ModRepository):
    mods = {}

    def __init__(self, repopath):
        super().__init__(repopath)
        mods = self.list_mods()
        for mod_name in mods.keys():
            self.mods[mod_name] = Mod(mods[mod_name])

    def get_mod(self, name):
        return self.mods[name]