# Final Project

For your final CS 301 project, you're going to analyze the whole
world!

Specifically, you're going to study various statistics for 175
countries, answering questions such as: *what is the correlation
between a country's literacy rate and GDP?*

To start, download the files given below into your project directory.

* [expected.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p10/expected.json)
* [expected.html](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p10/expected.html)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p10/test.py)



# General Directions

The final project is due on December 12, but we're breaking it into
three stages.  We'll be releasing one stage each week.  You can set
your own work schedule (e.g., it would be a bad idea to try this, but
you could complete all three stages on December 11 if you like).  We
recommend trying to complete one stage each week so you don't leave
too much work until the end.

You'll be doing all your work in a notebook, and when you're done,
you'll turn in a `main.ipynb` file.  We recommend you start by
reviewing the
[reading](https://tyler.caraza-harter.com/cs301/fall18/materials/readings/lec-26/pandas-intro.html)
where we first introduced notebooks.

As usual, you can work with one partner.  Please include the usual
comments
([directions](https://tyler.caraza-harter.com/cs301/fall18/projects.html))
in the first cell of your notebook.

# Data

For this project, you'll be using one large JSON file with statistics
about 175 countries, and 175 small JSON files, each with details about
one country's capital.  The data was adapted from
[here](http://techslides.com/list-of-countries-and-capitals) and
[here](https://www.kaggle.com/fernandol/countries-of-the-world).

You should start by looking at these two web resources:

* [https://tyler.caraza-harter.com/cs301/fall18/data/countries.json](https://tyler.caraza-harter.com/cs301/fall18/data/countries.json)
* [https://tyler.caraza-harter.com/cs301/fall18/data/capitals.txt](https://tyler.caraza-harter.com/cs301/fall18/data/capitals.txt)

The second file contains links to smaller files that you will need to
automatically download for your analysis.

Some of the columns require a little extra explanation:
* area: measured in square miles
* coastline: ratio of coast to area
* birth-rate: births per 1000 people per year
* death-rate: deaths per 1000 people per year
* infant-mortality: per 1000 births
* literacy: (out of 100%)
* phones: number of phone per 1000 people

# Testing

If your notebook is named main, run the following to test your
notebook (be sure to save it first, or you might accidentally test an
old version of your code): `python test.py main.ipynb`.

Tests will run everything in order, so if you get a different result,
you may want to try clicking "Restart and Run All" from the "Kernel"
menu in your notebook before running the tests.

You will need to download test.py, expected.json, and expected.html in
order to run the tests.

# Stages

* [Stage 1: Web Scraping](stage1.md)
* [Stage 2: Database Querying](stage2.md)
* Stage 3: Plotting (not posted yet)
