# Project 3

The City of Madison has many [different
agencies](https://www.cityofmadison.com/agencies) providing a variety
of services.  In this project, you'll analyze real spending data from
2015 to 2018 for five of the largest agencies: police, fire, streets,
library, and parks.  You'll get practice calling functions from a
`project` module, which we'll provide, and practice writing your own
functions.

Start by downloading `project.py`, `test.py` and `madison.csv`.
Double check that these files don't get renamed by your browser (by
running `ls` in the terminal from your `p3` project directory).
You'll do all your work in a new `main.ipynb` notebook that you'll
create and handin when you're done.  You'll test as usual by running
`python test.py`.

We won't explain how to use the `project` module here (the code in the
`project.py` file).  The lab this week is designed to teach you how it
works, so be sure to do the lab from home (if you missed it) before
starting the project.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Dataset

The data looks like this:

agency_id|agency|2015|2016|2017|2018
------|------|------|------|------|------
11|police|68.06346877|71.32575615000002|73.24794765999998|77.87553504
22|fire|49.73757877|51.96834048|53.14405332|55.215007260000014
33|library|16.96543425|18.12552139|19.13634773|19.845065799999997
44|parks|18.371421039999998|19.159243279999995|19.316837019999994|19.7607100000000
55|streets|25.368879940000006|28.2286218|26.655754419999994|27.798933740000003

The dataset is in the `madison.csv` file.  We'll learn about CSV files
later in the semester.  For now, you should know this about them:
* it's easy to create them by exporting from Excel
* it's easy to use them in Python programs
* we'll give you a `project` module to help you access them until we teach you more

All the numbers in the dataset are in millions of dollars.  Answer
questions in millions of dollars unless we specify otherwise.

## Requirements

You may not hardcode agency IDs in your code.  For example, if we ask
how much was spent on streets in 2015, you could obtain the answer
with this code: `get_spending(get_id("streets"), 2015)`.  If you don't
use `get_id` and instead use `get_spending(55, 2015)`, we'll deduct
points.

For some of the questions, we'll ask you to write (then use) a
function to compute the answer.  If you compute the answer without
creating the function we ask you to, we'll manually deduct points from
the `test.py` score when recording your final grade, even if the way
you did it produced the correct answer.

## Questions and Functions

###Q1: What is the agency ID of the library agency?

How: use `project.get_id("library")`

###Q2: How much did the agency with ID 44 spend in 2018?

It is OK to hardcode `44` in this case since we asked directly about
agency 44 (instead of about "parks").

###Q3: How much did "streets" spend in 2017?

Hint: instead of repeatedly calling `project.get_id("streets")` (or
similar) for each function, you may wish to make these calls once at
the beginning of your notebook and save the results in variables,
something like this:

```
streets_id = project.get_id("streets")
police_id = project.get_id("police")
fire_id = project.get_id("fire")
...
```

###Function 1: `year_max(year)`

This function will compute the maximum spending of any one agency in a
given year.  We'll give this one to you directly (you'll have to do
the subsequent functions yourself).  Copy/paste this into a cell in
your notebook:

```
def year_max(year):
    # grab the spending by each agency in the given year
    police_spending = project.get_spending(project.get_id("police"), year)
    fire_spending = project.get_spending(project.get_id("fire"), year)
    library_spending = project.get_spending(project.get_id("library"), year)
    parks_spending = project.get_spending(project.get_id("parks"), year)
    streets_spending = project.get_spending(project.get_id("streets"), year)

    # use builtin max function to get the largest of the five values
    return max(police_spending, fire_spending, library_spending, parks_spending, streets_spending)
```

###Q4: What was the most spent by a single agency in 2015?

Use `year_max` to answer this.

###Q5: What was the most spent by a single agency in 2018?

###Function 2: `agency_min(agency)`

We'll help you start this one, but you need to fill in the rest
yourself.

```
def agency_min(agency):
    agency_id = project.get_id(agency)
    y15 = project.get_spending(agency_id, 2015)
    y16 = project.get_spending(agency_id, 2016)
    # grab the other years

    # use the min function (similar to the max function)
    # to get the minimum across the four years, and return
    # that value
```

This function will compute the minimum the given agency ever spent
over the course of a year.

###Q4: What was the least the police ever spent in a year?

Use your `agency_min` function.

###Q5: What was the least that fire ever spent in a year?

###Q6: What was the least that library ever spent in a year?

function 3: average spent by agency?
function 4: change_per_year?
function 5: extrapolate
function 6: extrapolate_error