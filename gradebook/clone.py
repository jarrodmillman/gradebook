""" Clone student or project repos
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import

from argparse import ArgumentParser

from gradebook.utils import cd, get_grades, log, sh, gb_home

argparser = ArgumentParser(
    description='Clone student or project repos.'
)
argparser.add_argument('directory')
argparser.add_argument('config')

def main():
    args = argparser.parse_args()
    directory = "/".join([gb_home, args.directory])
    config = "/".join([gb_home, args.config])
    clone(directory, config)

def clone(directory, info):
    grades = get_grades(info)

    with cd(directory, create=True):
        for student in grades:
            login = student['login']
            repo = student['url']
            sh(['echo', 'git', 'clone', repo, login])

#proj_dir = gb_home+'/repos/projects'
#proj_info = "/home/stat133/src/grader/data/projects.json"
#
#if __name__ == "__main__":
#    clone(proj_dir, proj_info)
