""" Run commands in student or project repos
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import

import os
from argparse import ArgumentParser

from gradebook import grades, repo_dir
from gradebook.utils import cd, log, sh

argparser = ArgumentParser(
    description='Run command in student or project repos.'
)
argparser.add_argument(
    '-p', '--projects', action='store_true',
    help='run on projects (default: students)'
)
argparser.add_argument(
    '-s', '--select', action='store',
    help='only run on the specified section'
)
argparser.add_argument('command', nargs='+',
                       help='command to run in repos')


def main():
    args = argparser.parse_args()

    log.info('#'*80)
    log.info(vars(args))
    log.info('#'*80)
    repos = 'projects' if args.projects else 'students'
    
    for repo in grades[repos].values():
        login = repo['login']
        status = repo.get('status', 'enrolled')
        if args.select:
            try:
                selected = repo['section'] == args.select
            except KeyError:
                print(repo['login'])
        else:
            selected = True
        if selected and status in ['enrolled', 'audit', 'unenrolled']:
            run(args.command, os.path.join(repo_dir, repos, login)) 

def run(command, directory):
    with cd(directory):
        sh(command)

