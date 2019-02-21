# Project 5

Hurricanes often count among the worst natural disasters, both in terms of
monetary costs and, more importantly, human life.  Data Science can
help us better understand these storms.  For example, take a quick
look at this FiveThirtyEight analysis by Maggie Koerth-Baker:
[Why We're Stuck With An Inadequate Hurricane Rating System](https://fivethirtyeight.com/features/why-were-stuck-with-an-inadequate-hurricane-rating-system/).

For this project, you'll be analyzing data in the `hurricanes.csv`
file.  We generated this data file by writing a Python program to
extract stats from this page:
https://en.wikipedia.org/wiki/List_of_United_States_hurricanes.  By
the end of this semester, we'll teach you to extract data from
websites like Wikipedia for yourself.

This project will focus on **conditional statements** and
**loops**. To start, download `project.py`, `test.py` and
`hurricanes.csv`.  You'll test as usual by running `python test.py` to
test a `main.ipynb` file (or `python test.py other.ipynb` to test a
notebook with a different name).

We won't explain how to use the `project` module here (the code in the
`project.py` file).  The lab this week is designed to teach you how it
works, so be sure to do the lab from home (if you missed it) before
starting the project.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

# Important Note

Often, we'll often organize data by assigning numbers (called indexes)
to different parts of the data (e.g., rows or columns in a table). In
Computer Science, indexing typically starts with the number 0 (zero).
i.e., when you have a list of things, you'll start counting them from
0 (zero) instead of 1 (one). To understand this better, open the file
hurricanes.csv and take a look at it. You can open it in any
spreadsheet program (like Microsoft Excel or LibraOffice Sheets) or in
a basic text editor like idle or notepad. If you open it in a
spreadsheet program or view in on github
(https://github.com/tylerharter/cs301-projects/blob/master/spring19/p5/hurricanes.csv)
you will see row numbers - but notice the row numbers start at 1. Row
numbers are not the same as the index numbers!

In this file, the
first row is the header (like the column names in a table).
The remaining rows in this file are the data we are interested in.
It is important to note that:
* Hurricane 'Baker' is at index 0
* Hurricane 'Camille' is at index 1
* Hurricane 'Eloise' is at index 2
* etc.

## Questions and Functions

For the first four, you don't have to define
any functions of your own. Instead you should just make use of the
functions provided in the file *project.py* by calling the corresponding
function that you need to solve a particular problem.
### Q1: How many records are in the dataset?
### Q2: What is the name of the hurricane at index 0?
### Q3: What is the name of the hurricane at index 3?
### Q4: What is the name of the hurricane at index 19?

### Q5: Was there a hurricane named Waldo?

To answer this, you'll need to implement (i.e, define) the `searchHurricane(name)` function.

```python
# TODO: finish this function
def searchHurricane(name):
    # create an index variable, starting at 0

    while False: # stopping condition, this will currently not loop, fix it
        pass # this is a placeholder for an empty loop, so delete it

        # use the project.getName function to check if the hurricane
        # at the current index is the one we're looking for and if so
        # return True

        # increment your index
    return None  # fix this
```

This might be your first time attempting to implement a `while` loop.
As a recap, there are 3 important elements to remember when designing a loop:

1. The stopping condition.
2. Code to run on every iteration of the loop.
3. An increment/decrement statement.

A small framework to help you design a while loop has been given in main.py for this function.
This should help you to determine which element goes where in the loop.
* The purpose of this function is to find if a hurricane exists with a given
`name` (which is provided as the input to the function).
* This function takes the `name` of a hurricane as a parameter
and it's goal is to return `True` if the hurricane is in the dataset, and
`False` if it is not.
* You may have to use the helpers functions provided in *project.py*
to implement this function and the functions below.

### Q6: Was there a hurricane named 'Tyler'?

### Q7: Was there a hurricane named 'Caroline'?
You can see how having a function can help you quickly answer the same type of question multiple times with different input!

### Q8: How many hurricanes came from the Pacific?

To answer this, you'll need to implement the `countHurricane(oceanName)` function.
* The purpose of this function is to compute and return the number of
hurricanes that occurred in a particular ocean (e.g., Pacific), given the
ocean name as input.
* For this function, you will still be looping over all the values in the dataset.
* Loop through the dataset and increment a `counter` each time you find a hurricane that is from the ocean indicated by `oceanName`.
* This function should take in the name of the ocean you are searching for as `oceanName`, and it should return the count of how many times this `oceanName` was found in the dataset of hurricanes.
* If there are no hurricanes with the given `oceanName`, then this function should return 0 (zero).

### Q9: How many hurricanes came from the Atlantic?

### Q10: How many more hurricanes were in the Atlantic ocean than the Pacific ocean?

### Q11: What is the highest wind speed of all the hurricanes in the data set?

To answer this, you'll need to implement `maxWindSpeedHurricane()` function.
* The purpose of this function is to find and return the maximum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the largest value.
* Your function should take no parameters and should return the largest wind speed value.

You might notice the result is not what you expect! Remember, this dataset is drawn from data on hurricanes in their first 24 hours, before they get very powerful.

### Q12: What is the lowest wind speed of all the hurricanes in the data set?
To answer this, you'll need to implement  `minWindSpeedHurricane()` function.
* The purpose of this function is to find and return the minimum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the smallest value.
* Your function should take no parameters and should return the smallest wind speed value.


### Q13: What is the difference between the max wind speed and min wind speed of the dataset?


### Good luck with your hurricanes project! :)
