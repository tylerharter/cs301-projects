# Project 3

The City of Madison has many [different
agencies](https://www.cityofmadison.com/agencies) providing a variety
of services.  In this project, you'll analyze real spending data from
2015 to 2018 for five of the largest agencies: police, fire, streets,
library, and parks.  You'll get practice calling functions from a
`project` module, which we'll provide, and practice writing your own
functions.

Start by downloading `test.py` and `madison.csv`.  Double check that
these files don't get renamed by your browser (by running `ls` in the
terminal from your `p3` project directory).  You'll do all your work
in a new `main.ipynb` notebook that you'll create and handin when
you're done.  You'll test as usual by running `python test.py`.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

Requirements...

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

## Questions

