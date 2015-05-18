__author__ = 'admiral0'

from . import *
from .Exceptions import JsonNotValid
import argparse
import os.path as path


def is_mod_repo(x):
    if path.isdir(x):
        return x
    raise argparse.ArgumentTypeError(x + ' is not a Directory')


def validate(args):
    try:
        repo = ModRepository(args.mod_repo)
        for m in repo.list_mods().values():
            try:
                Mod(m)
            except JsonNotValid as e:
                print(str(e))
    except JsonNotValid as e:
        print(str(e))


def list_mods(args):
    repo = ModManager(args.mod_repo)
    for mod in repo.mods.values():
        print(mod.slug + ' ')
        print(','.join(mod.data['versions'].keys()))


actions = {
    'validate': validate,
    'list': list_mods
}

parser = argparse.ArgumentParser(description='TechnicAntani ModRepo Tools')
parser.add_argument('mod_repo', metavar='ModRepoPath', type=is_mod_repo, help='The path to Mod Repo directory',
                    default='.')
parser.add_argument('-a', dest='action', type=str, default='validate', choices=actions.keys(),
                    help='Action to perform')


def init():
    args = parser.parse_args()
    actions[args.action](args)