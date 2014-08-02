""" Run commands in student or project repos
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import

from argparse import ArgumentParser

from gradebook import grades, student_repos
from gradebook.utils import cd, log, sh

argparser = ArgumentParser(
    description='Clone student or project repos.'
)
argparser.add_argument('command', nargs='+',
                       help='command to run in repos')


def main():
    args = argparser.parse_args()

    log.info('#'*80)
    log.info(vars(args))
    log.info('#'*80)
#    grades = get_grades()
    for student in grades:
        login = student['login']
        status = student['status']
        if status in ['enrolled', 'audit']:
            run(args.command, '/'.join([student_repos, login])) 

def run(command, directory):
    with cd(directory):
       sh(command)


#proj_dir = gb_home+'/repos/projects'
#proj_info = "/home/stat133/src/grader/data/projects.json"
#
#if __name__ == "__main__":
#    clone(proj_dir, proj_info)
