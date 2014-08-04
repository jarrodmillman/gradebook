""" Clone student or project repos
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import

import os
from argparse import ArgumentParser

from gradebook import grades, repo_dir
from gradebook.utils import cd, log, sh

argparser = ArgumentParser(
    description='Clone student or project repos.'
)
argparser.add_argument('directory', choices=('students', 'projects', 'instructor'))

def main():
    args = argparser.parse_args()
    clone(args.directory)

def clone(t):
    directory = os.path.join(repo_dir, t)
    with cd(directory, create=True):
        for repo in grades[t].values():
            login = repo['login']
            url = repo['url']
            sh(['git', 'clone', url, login])
