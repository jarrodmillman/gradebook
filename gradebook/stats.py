#!/usr/bin/env python

import sys
from collections import OrderedDict, Counter

from numpy import array
import pandas as pd

from gradebook import config_file, get_grades, grades

def main():
    argv = sys.argv[1:]
    print argv
    narg = len(argv)
    
    if narg == 0:
        total = 0
        assignments = get_grades(config_file)
        
        #for assignment in [a for x in assignments for a in assignments[x]]
        for reading in assignments['readings']:
            total += get_scores(reading)
        for homework in assignments['homeworks']:
            total += get_scores(homework)
    
    else:
        lab = argv[0]
        total = get_scores(lab)
    
    print '*'*80
    print total
    print '*'*80
    print pd.Series(total).describe()
    print '*'*80
    stem_and_leaf(total)

def stem_and_leaf(x):
    d = OrderedDict((((str(v)[:-1],' ')[v<10], Counter()) for v in sorted(x)))
    for s in ((str(v),' '+str(v))[v<10] for v in x):
        d[s[:-1]][s[-1]] += 1
    m=max(len(s) for s in d)
    for k in d:
        print('%s%s | %s'%(' '*(m-len(k)),k,' '.join(sorted(d[k].elements()))))

def get_scores(lab):
    total = []
    for student in grades['students'].values():
        status = student.get('status', 'enrolled')
        #if status in ['enrolled', 'audit'] and lab in student['grades']:
        if status in ['enrolled'] and lab in student['grades']:
            total += [student['grades'][lab]['earned']]
    return array(total)
