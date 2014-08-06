from __future__ import print_function
import os

from gradebook import (
    get_grades,
    save_grades,
    grades,
    student_grades
)

def main():
    repo = get_grades(student_grades)
    login = repo['login']
    directory = os.getcwd().split('/')[-2]
    #directory = repo['type']

    record = grades[directory][login]
    if 'SID' in record:
        del record['SID']
    save_grades(record, student_grades)

