gradebook
=========

Tools for grading

## Environment Variable

    export GB_HOME=<working directory for class records>

## Installation

    make install 


## Getting started

1. https://github.com/jarrodmillman/example-class
2. https://github.com/jarrodmillman/example-assignments


## Example: scoring hw5

gb-update updates a single student or project repo's individual
section of the entire class' grades.json.  I've been naming the
individual copies grades.json as well.

gb-score <asgn> always generates a score.log in the individual repo's
<asgn> directory.

Grading students is a little freeform and I normally iterate on each
of the steps until I get it right and then move forward.  I typically
run git status at the top-level and also using gb-run in the subrepos
between each step.  Sometimes I have to use git to revert a step and
then try again.  My typical workflow for scoring an assignment (say
hw5) might look something like this (w/ some of the checking in
between each step left out---it started getting long when I actually
wrote things down):

    # Make sure data/grades.json is pristine and up to date
    git status
    
    # Make sure log/grades.log doesn't exist
    ls log/grades.log
    
    # Make sure student's repos are clean and on master
    gb-run git status
    
    # Checkout the assignment
    gb-run git checkout hw5
    
    # Quick look at log file
    vim log/grades.json
    
    # Check student's repos
    gb-run git status
    
    # Score
    gb-run -- gb-score -r hw5
    
    # Check grades
    git diff data/grades.json
    
    # Maybe soft freeze data/grades.json so I can tell if something I do
    changes the grades further
    git add data/grades.json
    
    # Check the stats (you may  need to edit data/config/json, but this will change)
    gb-stats hw5
    
    # May need to individually check specific repos depending on how things look
    # e.g., I may check out which student's got 0s, but I haven't ported
    that functionality for the old system yet
    # gb-grades hw5
    
    # I am happy with scores and ready to finalize everything
    
    # check repos
    gb-run git status
    
    # may need to clean up hw5/Rplots.pdf
    gb-run rm hw5/Rplots.pdf
    
    # add it back if the student has it checked in
    gb-run git checkout hw5/Rplots.pdf
    
    # check repos
    gb-run git status
    
    # go back to master
    gb-run git checkout master
    
    # check repos & maybe quickly look through log
    gb-run git status
    
    # add score.log
    gb-run git add hw5/score.log
    
    # updates their copy of their grades
    gb-run gb-update
    gb-run git add grades.json
    
    # commit student grades
    gb-run -- git commit -m 'Score hw5'
    
    # return scores
    gb-run git pull
    gb-run git push
    
    # check the log
    vim log/grades.json
    
    # if everything good, rename
    mv log/grades.json log/2014-08-04-score-hw5.log
    git add log/2014-08-04-score-hw5.log

Then git commit which should include changes to data/grades.json and
log/2014-08-04-score-hw5.log.  Then

    git pull
    git push

And it is done unless we need to regrade something.
