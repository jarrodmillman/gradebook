""" Run commands in student or project repos
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import

from argparse import ArgumentParser

from gradebook.utils import cd, get_grades, log, sh, gb_home

argparser = ArgumentParser(
    description='Clone student or project repos.'
)
argparser.add_argument('command', nargs='+',
                       help='command to run in repos'))
argparser.add_argument(
    '-u', '--user', action='store_true',
    help='only run for this user'
)


def main():
    args = argparser.parse_args()

    log.info('#'*80)
    log.info(' '.join(args))
    log.info('#'*80)

def run(command, directory):
    with cd(directory):
       sh(command)


#proj_dir = gb_home+'/repos/projects'
#proj_info = "/home/stat133/src/grader/data/projects.json"
#
#if __name__ == "__main__":
#    clone(proj_dir, proj_info)
