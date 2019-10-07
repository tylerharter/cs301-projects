# Project 5: Hurricane Study

## Corrections/Clarifications

* none yet

## Overview

Hurricanes often count among the worst natural disasters, both in terms of
monetary costs and, more importantly, human life.  Data Science can
help us better understand these storms.  For example, take a quick
look at this FiveThirtyEight analysis by Maggie Koerth-Baker:
[Why We're Stuck With An Inadequate Hurricane Rating System](https://fivethirtyeight.com/features/why-were-stuck-with-an-inadequate-hurricane-rating-system/)
(you should all read FiveThirtyEight, btw!).

For this project, you'll be analyzing data in the `hurricanes.csv`
file.  We generated this data file by writing a Python program to
extract stats from this page:
https://en.wikipedia.org/wiki/List_of_United_States_hurricanes.  By
the end of this semester, we'll teach you to extract data from
websites like Wikipedia for yourself.

This project will focus on **loops** and **strings**. To start,
download `project.py`, `test.py` and `hurricanes.csv`.  You'll do your
work in Jupyter Notebooks this week, producing a `main.ipynb` file.
You'll test as usual by running `python test.py` to test a
`main.ipynb` file (or `python test.py other.ipynb` to test a notebook
with a different name).  You may not use any extra modules that you
need to install with pip (only the standard modules that come with
Python, such as `math`).

We won't explain how to use the `project` module here (the code in the
`project.py` file).  The lab this week is designed to teach you how it
works.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Questions and Functions

For the first three questions, you don't have to define
any functions of your own. Instead you should just make use of the
functions provided in the file `project.py` by calling the corresponding
function that you need to solve a particular problem.

### Q1: How many records are in the dataset?

### Q2: What is the name of the hurricane at index 10?

### Q3: How many deaths were caused by the hurricane at the last index?

### Q4:Is there a hurricane named Bob?

To get full credit on this one, you are required to use a `break` to
finish your loop early if Bob is found. Output `True` if Bob is found and
`False` if the hurricane is not found.

Hint: here's a loop that prints every hurricane name.  Consider
adapting the code?

```python
for i in range(project.count()):
    print(project.get_name(i))
```

### Q5: How many hurricanes named Florence are in the dataset?

Write your code such that it counts all the variants (e.g., "Florence",
"FLORENCE", "fLoReNce", etc.).

### Q6: What is the fastest MPH achieved by a hurricane in the dataset?

### Q7: What is the name of that fastest hurricane?

### Q8: How much damage (in dollars) was done by the hurricane Dolphin?

Be careful! In the data, the number was formatted with a suffix, but
you'll need to do some processing to convert it to this: `13500000`.

While not required, you may wish to write a general function that
handles "K", "M", and "B" suffixes (it will be handy later).

### Q9: How many total deaths are represented in the dataset?

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return index of deadliest hurricane over the given date range
def deadliest_in_range(year1, year2):
    worst_idx = None
    for i in range(project.count()):
        if ????:  # TODO: check if year is in range
            if worst_idx == None or ????:  # TODO: it is worse than previous?
                # TODO: finish this code!
    return worst_idx
```

Hint: You can copy the `get_month`, `get_day`, and `get_year`
functions you created in lab to your project notebook if you like.

### Q10: What was the deadliest hurricane between 2010 and 2019 (inclusive)?

For this and the following, count a hurricane as being in the year it
was formed (not dissipated).

### Q11: What was the deadliest hurricane of the 20th century (1901 to 2000, inclusive)?

### Q12: In what year did the most deadly hurricane in the dataset form?

### Q13: How much damage (in dollars) was done by the deadliest hurricane of the 20th century?

### Q14: What were the total damages across all hurricanes in the dataset, in dollars?

Remember that "K" stands for thousand, "M" stands for million, and "B"
stands for billion!  These may appear in the dataset, but the answer
you compute (`864230464997`) should not use them.

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return number of huricanes formed in month mm
def hurricanes_in_month(mm):
    num_of_hurricanes = 0
    for i in range(project.count()):
        pass # TODO: finish this code!
    return num_of_hurricanes
```

### Q15: How many hurricanes were formed in the month of July?

### Q16: How many hurricanes were formed in the month of December?

### Q17: How many hurricanes were formed in the month of January?

### Q18: How many hurricanes were formed in the month of May?

## Challenge Questions

### Q19: Which month experienced the formation of the most number of hurricanes?

Answer with a number (e.g., 1 for Jan, etc.).

### Q20: How many years experienced the formation of at least four hurricanes?

### Good luck with your hurricanes project! :)
