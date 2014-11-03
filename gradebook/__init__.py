from collections import OrderedDict
import os
import sys
import json


try:
   gb_home = os.environ["GB_HOME"]
except KeyError:
   raise RuntimeError("Please set the environment variable GB_HOME")

repo_dir = os.path.join(gb_home, 'repos')
data_dir = os.path.join(gb_home, 'data')
log_dir = os.path.join(gb_home, 'log')
grade_file = 'grades.json'

instructor_home = os.path.join(repo_dir, 'instructor', 'assignments')

student_grades = grade_file
class_grades = os.path.join(data_dir, grade_file)
config_file = os.path.join(data_dir, 'config.json')
csv_file = os.path.join(data_home, 'grades.csv')

class_log = os.path.join(log_dir, 'grade.log')


def get_grades(filename=class_grades):
    try:
        with open(filename) as infile:
            grades = json.load(infile, object_pairs_hook=OrderedDict)
    except:
        print("Trouble loading " + filename)
        sys.exit(1)

    return grades


def save_grades(content, filename):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile, indent=4)


grades = get_grades()
