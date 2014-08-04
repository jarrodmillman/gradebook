from collections import OrderedDict
import os
import sys
import json


try:
   gb_home = os.environ["GB_HOME"]
except KeyError:
   print "Please set the environment variable GB_HOME"
   sys.exit(1)

repo_dir = gb_home + '/repos/'
data_dir = gb_home + '/data/'
log_dir = gb_home + '/log/'
grade_file = 'grades.json'

instructor_home = repo_dir + 'students/instructor/'

student_grades = grade_file
class_grades = data_dir + grade_file
config_file = data_dir + 'config.json'

class_log = log_dir + 'grade.log'


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
