#!/usr/bin/env python
""" Score an assignment
"""
# vim: ft=python
from __future__ import division, print_function, absolute_import


import os, sys
from argparse import ArgumentParser
import json 
import logging as log
import traceback
from subprocess import check_output
from rpy2.robjects import r as R


argparser = ArgumentParser(
    description='Score an assignment.'
)
argparser.add_argument('assignment')
argparser.add_argument(
    '-r', '--record', action='store_true',
    help='record score in gradebook'
)
argparser.add_argument(
    '-f', '--finish', action='store_true',
    help="only score students if they haven't been already"
)
argparser.add_argument(
    '-l', '--list', action='store_true',
    help="list parts"
)
argparser.add_argument(
    '-p', '--parts', nargs='+',
    help="only score these parts"
)

def main():
    args = argparser.parse_args()
    assignment = args.assignment

    if student['status'] != 'enrolled':
        return None

    if args.finish:
        for d in grades:
            if d['login']==student['login'] and assignment in d['grades']:
                return None

    logfile = instructor_home+"/../"+login+"/"+assignment+"/score.log"
    start_log(logfile)
    global_vars = {}
#    local_vars = {}

    filename = instructor_home+"/"+assignment+".py"
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, global_vars)

    part_names = global_vars['part_names']
    possible = global_vars['possible']

    # list
    if args.list:
        print(' '.join(part_names))
        return None

    # set up skelton for scores
    if args.parts:
        if set(args.parts).issubset(part_names):
            parts = init_parts(part_names, possible, args.parts)
        else:
            print("ERROR:  {} is not a subset of {}.".format(args.parts,part_names))
            return None
    else:
        parts = init_parts(part_names, possible)

    for func_name in parts:
        parts[func_name]['earned'] = global_vars[func_name](assignment) # + argument list

    if args.record:
        save_grades(assignment, parts)
    else:
        print('='*17)
        print('(not recording) score: ' + str(get_score(parts)))
        print('Out of: ' + str(get_possible(parts)))
        print('='*17)
        print(parts)

    return None

def start_log(logfile):
    log.basicConfig(filename=logfile,
                    filemode='w',
                    level=log.INFO)
    return None

def init_parts(names, possible, parts=None):
    if parts:
        p = { part: {'earned': 0, 'possible': points}
               for (part, points) in zip(names, possible) if part in parts}
    else:
        p = { part: {'earned': 0, 'possible': points}
               for (part, points) in zip(names, possible)}
    return p

def get_grades(filename):
    try:
        with open(filename) as infile:
            grades = json.load(infile)
    except:
        print("Trouble loading " + filename)
        sys.exit(1)

    return grades

def save_grades(assignment, parts, verbose=True):
    for d in grades:
        if d['login']==student['login']:
            penalty = 0
            note = ''
            commit = check_output(['git', 'log', '-1', '--format="%H"']).strip()[1:-1]
            score = get_score(parts)
            possible =  get_possible(parts)
            if assignment in d['grades']:
                old = d['grades'][assignment]
                if 'penalty' in old:
                    penalty = old['penalty']
                if 'note' in old:
                    note = old['note']
                if 'possible' in old:
                    possible = old['possible']
                score = max(score - penalty, old['earned'])
                for k,v in old['parts'].iteritems():
                    parts[k] = parts.get(k, v)
            d['grades'][assignment] = {'earned': score,
                                'parts': parts,
                                'possible': possible,
                                'penalty': penalty,
                                'hash': commit,
                                'note': note }
    with open(class_grades, 'w') as outfile:
        json.dump(grades, outfile, sort_keys = True, indent = 4)
    if verbose:
        print(student['login'] + ' got ' + str(score))
        log.info("You got a %s out of %s.", str(score), str(possible))

def get_score(parts):
    return sum([parts[p]["earned"] for p in parts])

def get_possible(parts):
    return sum([parts[p]["possible"] for p in parts])

def run(command, g):
    log.info('Executed '+command)
    try:
        exec(command, g)
    except:
        log.exception('Got exception on main handler')
        log.exception(traceback.format_exc())

def correct(command, answer, points):
    log.info('(%s points) %s is %s', points, command, answer)

def wrong(command, answer, result, points):
    log.error('(%s points) Checking %s', points, command)
    log.error('... Expecting: %s', answer)
    log.error('... But got:   %s', result)

def check(command, answer, points, g):
    g['os'] = os
    try:
        result = eval(command, g)
    except:
        wrong(command, answer, 'Traceback error', points)
        log.exception('Got exception:')
        log.exception(traceback.format_exc())
        return 0
    if result == answer:
        correct(command, answer, points)
        return points
    else:
        wrong(command, answer, result, points)
        return 0

def query(question, points):
    """Ask a yes/no question via raw_input() and return their answer.
    Modified from ActiveState 577058-query-yesno

    "question" is a string that is presented to the user.

    The "answer" return value is one of "True" or "False".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,   "n":False}
    prompt = " [y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in valid:
            if valid[choice]:
                correct(question, choice, points)
                return points
            else:
                wrong(question, "False", choice, points)
                return 0
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

try:  
   gb_home = os.environ["GB_HOME"]
except KeyError: 
   print("Please set the environment variable GB_HOME")
   sys.exit(1)

instructor_home = gb_home + '/133/instructor'
class_grades = gb_home + '/data/grades.json' 
student_grades = 'grades.json'

grades = get_grades(class_grades)
student = get_grades(student_grades)
login = student['login']


try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

if __name__ == '__main__':
    main()
