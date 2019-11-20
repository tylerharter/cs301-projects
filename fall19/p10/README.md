# Project 10: Geography, and the World Wide Web

## Clarifications/Corrections

* None yet!

## Introduction

For your final CS 301 project, you're going to analyze the whole
world!

Specifically, you're going to study various statistics for 174
countries, answering questions such as: *what is the correlation
between a country's literacy rate and GDP?*

To start, download `test.py` and `expected.html`.  You'll also need to
download `lint.py` (see linter documentation under "Testing" below).
Do not download any data files manually (you must write Python code to
download these automatically).  You'll do all your work in a
`main.ipynb`.

# Data

For this project, you'll be using one large JSON file with statistics
about 174 countries adapted from
[here](https://www.kaggle.com/fernandol/countries-of-the-world).
and you will also extract data from a snapshot of
[this page](http://techslides.com/list-of-countries-and-capitals)

First check these resources:
* https://raw.githubusercontent.com/tylerharter/caraza-harter-com/master/tyler/cs301/fall19/data/countries.json
* http://techslides.com/list-of-countries-and-capitals

Some of the columns require a little extra explanation:
* area: measured in square miles
* coastline: ratio of coast to area
* birth-rate: births per 1000 people per year
* death-rate: deaths per 1000 people per year
* infant-mortality: per 1000 births
* literacy: (out of 100%)
* phones: number of phone per 1000 people

# Testing

For answers involving a DataFrame, `test.py` compares your tables to
those in `expected.html`, so take a moment to open that file in your
browser.

`test.py` doesn't care if you have extra rows or columns, and it
doesn't care about the order of the rows or columns.  However, you
must have the correct values at each index/column location shown in
`expected.html`.

For P10, `test.py` is pickier than it has been. In addition to
checking for incorrect answers, it will also check for a few common
kinds of bad coding style. You should look for linting messages at the bottom 
of the output, for example:

```
Linting Summary:
  Warning Messages:
    cell: 1, line: 4 - Redefining built-in 'id'
    cell: 1, line: 3 - Reimport 'numpy' (imported line 2)
    cell: 1, line: 5 - Unnecessary pass statement
    cell: 1, line: 2 - Unused import numpy 
```

In this case, `test.py` will deduct 1 point per linter message because of 
bad style, and at most deduct 10 points. For more information about the linter 
as well as how to run the full linter to see all of the automatically generated 
advice and feedback, please check out the [linting README](../../linter).


## The Stages

* [Stage 1](stage1.md): scrape some data files and answer some geography questions
* Stage 2: query a DB and generate some plots (not released yet!)
