import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='AntaniRepos',
    version='1.0',
    author='Radu Andries',
    author_email='admiral0@tuxfamily.org',
    description=("A library to manage and modify repositories for "
                 "https://github.com/admiral0/TechnicAntani"),
    license='BSD',
    keywords='minecraft technicantani technicplatform repositories git',
    url='https://github.com/admiral0/AntaniRepos',
    packages=[
        'ModRepository',
        'PackRepository'
    ],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        "pygit2=0.22.0",
    ],
    entry_points={
        "console_scripts": [
            'antanimods = ModRepository.Util:init'
        ]
    }
)