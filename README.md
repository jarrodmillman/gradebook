gradebook
=========

Tools for grading

Important facts about the system:

* It relies heavily on Git. So whoever is using this system will need
  to understand how Git works and ideal should already be using Git
  regularly for their own work.  It also requires that teaching Git
  to your students is part of the course (and needs to be started
  before the students get to far into the course).
* There is one private class repo that only instructors see.
* Every student has their own private repo (e.g., using GitHub's educational
  student accounts).
* The instructor also needs a private assignments repo (e.g., using GitHub's
  educational account for organizations).
* For each assignment (e.g., homework 1) their must be a script (e.g., hw1.py)
  in the repos/instructor/assignments repo.
* It isn't ready for primetime, but I am **gradually** improving it.

You will need to have a keychain set up so they don't need to
type in their username and password for each repository they want to
push to.  You will also need to set up a GPG key so you can make
signed tags on the repos.  You will also want to make sure it is
in your keychain as well.

## Installation

The first time you install:

    pip install

To update (after a `git pull` for instance):

    make install 

## Getting started

You may wish to look through these example repos before reading further:

1. https://github.com/jarrodmillman/example-class
2. https://github.com/jarrodmillman/example-assignments

## Creating a class repo

Here is what a bare minimum private class repo should look like initially:

```
    .
    ├── .git
    ├── .gitignore
    ├── .log.conf
    ├── data
    │   └── grades.json
    └── log
        └── README.md
```

You can initially start your repo using the files in the `example-class`
repo.

Next you will need to populate `data/grades.json` with something like:

```
{
    "instructor": {
        "assignments": {
            "login": "assignments", 
            "url": "git@github.com:jarrodmillman/example-assignments.git", 
            "type": "instructor"
        }
    }, 
    "projects": {
        "jarrodmillman": {
            "login": "jarrodmillman", 
            "team": [
                "jarrodmillman"
            ], 
            "url": "git@github.com:jarrodmillman/example-project.git", 
            "type": "projects"
        }
    }, 
    "students": {
        "student1": {
            "login": "student1", 
            "status": "enrolled", 
            "url": "git@github.com:jarrodmillman/example-student.git", 
            "type": "students"
        }
    }
}
```

You will need to make changes to the above to reflect the actual information
for your class.

For more details about how you might populate all the student repo information,
please see [data/README.md](https://github.com/jarrodmillman/example-class/blob/master/data/README.md)

## Environment Variable

At this point, you will need to set an environment variable with the path to your
class repository on your local filesystem.

    export GB_HOME=<working directory for class records>

Once you've set `GB_HOME` and populated `data/grades.json`, you
can use `gb-clone students` and `gb-clone instructor` to create
the `repos/students/...` and repos/instructor/...` directories
and clone the corresponding repos into those directories.

```
    .
    ├── data
    ├── log 
    └── repos
        ├── instructor
        │   └── assignments
        │       ├── hw1
        │       │   ├── ex1-data.csv
        │       │   ├── ex1.r
        │       │   └── ex1-sol.r
        │       └── hw1.py
        └── students
            └── student1
                ├── .git
                ├── .gitignore
                └── README.md
```



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
