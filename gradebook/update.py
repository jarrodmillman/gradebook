#!/usr/bin/env python

from gradebook.utils import cd, get_grades, save_grades, log

def main():
    log.info('#'*80)
    log.info('Updating student copy of their grades')
    log.info('#'*80)
    grades = get_grades()
    for student in grades:
        login = student['login']
        status = student['status']
        if status in ['enrolled', 'audit']:
            del student['SID']
            with cd('133/'+login):
               log.info('Updating student record of grades ...')
               save_grades(student, 'grades.json')

#grades = get_grades()
if __name__ == '__main__':
    main()

