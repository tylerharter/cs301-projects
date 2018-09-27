# Project 3

This project will focus on **conditional statments** and **loops**. To start,
download the 4 files given below into your project directory.

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/main.py)
* [project.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/project.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/test.py)
* [hurricanes.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/hurricanes.csv)

**A reminder:** You should make your changes ONLY to the **main.py** file.
DO NOT EDIT ANY OTHER FILES.

After downloading all the files into the same directory try running the command below:

```
python test.py
```

and you should see the following: 
```
Your Python version: Python 3.7.0

Running your program with this command: python3 main.py

RESULTS:
  test_1: expecting True, but got None
  test_2: expecting False, but got None
  test_3: expecting True, but got None
  test_4: expecting False, but got None
  test_5: missing function searchHurricaneByLocation
  test_6: missing function searchHurricaneByLocation
  test_7: missing function countHurricane
  test_8: missing function countHurricane
  test_9: missing function minWindSpeedHurricane
  test_10: missing function maxWindSpeedHurricane
  problem_1: fewer output lines than expected
  problem_2: fewer output lines than expected
  problem_3: fewer output lines than expected
  problem_4: fewer output lines than expected
  problem_5: fewer output lines than expected
  problem_6: fewer output lines than expected
  problem_7: fewer output lines than expected
  problem_8: fewer output lines than expected
  problem_9: fewer output lines than expected
  problem_10: fewer output lines than expected
Score: 0%

```

# Important Note
In Computer Science, indexing starts with the number 0 (zero).
i.e., when you have a list of things, you'll start counting them
from 0 (zero) instead of 1 (one). To understand this better, open
the file hurricanes.csv and take a look at it. In this file, the
first row is the header (like the column names in a table).
The remaining rows in this file are the data we are interested in.
It is important to note that: 
* Hurricane 'HEIDI' is at index 0
* Hurricane 'OLAF' is at index 1
* Hurricane 'TINA' is at index 2

and so on.

Can you tell what is the hurricane at index 10 in this list of hurricanes? 

# Directions

The order in which you should implement the functions are as follows:

## Step 1.
Implement the problems 1 - 4 in the `main()` function within
the file *main.py*. To solve these problems, you don't have to define
any functions of your own. Instead you should just make use of the
functions provided in the file *project.py* by calling the corresponding
function that you need to solve a particular problem. To understand the
functions that are defined in *project.py*, you may open that file and
read the docstring (i.e., the line(s) below the function definition that
documents the purpose of the function). You may also find the purpose
of each function by doing the following on your python console:
```python
>>> import project
>>> project.getNumRecords.__doc__
'This function will return the number of records in the dataset'
>>> 

``` 

## Step 2.
Implement (i.e, define) the `searchHurricane(name)` function.

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

This might be your first time attemping to implement a `while` loop.
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

## Step 3. 
Implement the `searchHurricaneByLocation(latitude, longitude)` function.
* The purpose of this function is to find if a hurricane is present in the
dataset, given it's `latitude` and `longitude` as input.
* This function should be similar to what you did in the `searchHurricane()`
function.
* Just remember that, you have two values (i.e., `latitude` and `longitude`) that
need to match to one hurricane now.
* Instead of returning `True` or `False`, you need to return the name of the
hurricane at that location.
* If there are no hurricanes with the given `latitude` and `longitude`, then
this function should return `None`.  `None` is special value in python
which represents the absence of something. For example, in this case, `None`
signifies that there is no hurricane with the given `latitude` and `longitude`.

## Step 4.
Implement the `countHurricane(oceanName)` function.
* The purpose of this function is to compute and return the number of
hurricanes that occured in a particular ocean (e.g., Pacific), given the
ocean name as input.
* For this function, you will still be looping over all the values in the dataset.
* Loop through the dataset and increment a `counter` each time you find a hurricane that is from the ocean indicated by `oceanName`.
* This function should take in the name of the ocean you are searching for as `oceanName`, and it should return the count of how many times this `oceanName` was found in the dataset of hurricanes.
* If there are no hurricanes with the given `oceanName`, then this function should return 0 (zero).

## Step 5.
Implement `maxWindSpeedHurricane()` function.
* The purpose of this function is to find and return the maximum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the largest value.
* Your function should take no parameters and should return the largest wind speed value.

## Step 6.
Implement `minWindSpeedHurricane()` function.
* The purpose of this function is to find and return the minimum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the smallest value.
* Your function should take no parameters and should return the smallest wind speed value.

## Step 7.
* Solve the problems 5 - 10 in main using the functions that you have already created in the previous steps.
* This step just involves **calling** the functions that you have already defined in order to answer some questions that we have asked.
* It is important that you use your functions to solve these problems. Make sure that each of your solution calls at least one of the functions that you created.

### Good luck with your hurricanes project! :)

