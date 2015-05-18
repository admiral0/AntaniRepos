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


def pack(args):
    try:
        ModRepository(args.mod_repo)
    except JsonNotValid as e:
        print(str(e))


actions = {
    'mods': validate,
    'ls-mods': list_mods,
    'pack': pack,
    'list-pack': pack
}

parser = argparse.ArgumentParser(description='TechnicAntani ModRepo Tools')

parser.add_argument('action', metavar='action', type=str, default='mods', choices=actions.keys(),
                    help='Action to perform. One of ' + ','.join(actions.keys()))
parser.add_argument('mod_repo', metavar='path', type=is_mod_repo, help='The path to be inspected',
                    default='.')  # , nargs='+')
parser.add_argument('-m', dest='ModPath', type=is_mod_repo, help='Mod Repo parameter. Used in pack actions')


def init():
    args = parser.parse_args()
    actions[args.action](args)