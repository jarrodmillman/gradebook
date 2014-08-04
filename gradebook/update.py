from gradebook import (
    get_grades,
    save_grades,
    grades,
    student_grades
)

def main():
    repo = get_grades(student_grades)
    login = repo['login']
    directory = repo['type']

    record = grades[directory][login]
    del record['SID']
    save_grades(record, student_grades)

