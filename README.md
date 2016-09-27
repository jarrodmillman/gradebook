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
* For each assignment (e.g., homework 1) their must be a script (e.g., `hw1.py`)
  in the `repos/instructor/assignments` repo.
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
3. https://github.com/jarrodmillman/example-student

You will most likely want to keep all of the above repos private.

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
        "teamname": {
            "login": "teamname", 
            "team": [
                "github_user1", "github_user2", "github_user3"
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

If you are using GitHub, you may find this useful:
  https://github.com/education/teachers_pet

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

## Creating a student repo

Each private student (or project) repo needs a copy of their individual record
from the class record.  This file should be named `grades.json`.

For example, if this

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
        "teamname": {
            "login": "teamname",
            "team": [
                "github_user1", "github_user2", "github_user3"
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

is the class record, then the student record would be

```
{
    "login": "student1",
    "status": "enrolled",
    "url": "git@github.com:jarrodmillman/example-student.git",
    "type": "students"
}
```

## Creating an assignments repo

For each assignment, create a subdirectory and a corresponding Python at the
top-level of the assignment repository.
The subdirectories contain the assignment (e.g.,
instructions, date, the file students were to complete, solutions) and
the corresponding Python file is the grading script, which is loaded
and run by gradebook's `load_plugin` function.

For example, in
  https://github.com/jarrodmillman/example-assignments/tree/master/hw1
you will find four exercise files (e.g, `ex1.r`), four solution files
(e.g., `ex1_sol.r`), and test data (e.g., `ex1-tests.rda`).  The
students are given the exercise files and test data.
They then fill-in the exercise file.  Here is a summary of a typical
student workflow:
  http://www.jarrodmillman.com/stat133-summer2014/workflow.html

Let's look at one of the exercise files for `hw1`:
  https://github.com/jarrodmillman/example-assignments/blob/master/hw1/ex1.r
At the top of the file, we load a unit test library (I would use
`testthat` now) and some test data.  The file then consists of
instructions in comments and some function stubs.  Here is some
information about R functions (including unit testing) that we gave
the students:
  http://www.jarrodmillman.com/stat133-summer2014/notes3.html

Once the assignments were submitted, we would grade them using:
  https://github.com/jarrodmillman/example-assignments/blob/master/hw1.py
The first 14 lines are mostly boilerplate code.  The assignment
specific part begins on line 16:

    part_names = ['ex1', 'ex2', 'ex3', 'ex4']
    possible = [6, 8, 8, 8]

Each item in `part_name` corresponds to an assignment file (e.g.,
'ex1' corresponds to `hw1/ex1.r` as well as a grading function `ex1`
in `hw1.py`) and the corresponding item in the `possible` list
indicates the total number of possible points for that part of the
assignment.  The remainder of the file contains one function for each
part of the assignment.  For example, the function `ex1` on line 22
scores the first part of the assignment.  If you look at the function
body, you will see that it first attempts to source the submitted
code.  Next it makes sure any generated graphics are saved to a file
(i.e., `R('graphics.off()')` on line 30).  Then it loads the test
data.  Finally, it runs some tests and increments the score when the
tests pass.  For example, on line 33 you will see:

    score += check("R('all.equal(outlier.cutoff.t, outlierCutoff(ex1.test))')[0]", True, 2, g)

The `check` function checks whether the student's submitted
`outlierCutoff` function returns the expected result.  If so, `score`
is incremented by 2 (i.e., the third argument to the check function).
The last argument is the global namespace (i.e., dictionary), which is
where the `check` function finds the objects (e.g., the
`outlierCutoff` function) sourced from the student assignment.

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
