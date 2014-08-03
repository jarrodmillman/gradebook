#!/usr/bin/env python
# switch to only updating individuals grades (then use the runner)

from gradebook import grades, student_grades, save_grades, student_repos 
from gradebook.utils import cd, log

def main():
    log.info('#'*80)
    log.info('Updating student copy of their grades')
    log.info('#'*80)
    for student in grades['students'].values():
        login = student['login']
        status = student['status']
        if status in ['enrolled', 'audit']:
            del student['SID']
            with cd(student_repos+login):
               log.info('Updating student record of grades ...')
               save_grades(student, student_grades)

