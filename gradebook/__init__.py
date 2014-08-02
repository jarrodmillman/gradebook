import os
import sys
import json

try:
   gb_home = os.environ["GB_HOME"]
except KeyError:
   print "Please set the environment variable GB_HOME"
   sys.exit(1)

student_repos = gb_home+'/133'
instructor_home = gb_home + '/133/instructor'
class_grades = gb_home + '/data/grades.json'
class_log = gb_home+'/log/grade.log'
student_grades = 'grades.json'
config_file = gb_home+'/data/config.json'

def get_grades(filename=class_grades):
    try:
        with open(filename) as infile:
            grades = json.load(infile)
    except:
        print("Trouble loading " + filename)
        sys.exit(1)

    return grades


def save_grades(content, filename):
    with open(filename, 'w') as outfile:
        json.dump(content, outfile, sort_keys=True, indent=4)


grades = get_grades()


