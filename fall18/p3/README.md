# Project 3

This project will focus on **conditional statments** and **loops**. To start
download the 4 files given below.  For those using pycharm, it may be easier to
make a new project before downloading these files, so that you can save these
files in the new project directory that you created.

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/main.py)
* [project.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/project.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/test.py)
* [hurricanes.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/hurricanes.csv)

**A reminder:** You should make your changes ONLY to the **main.py** file. DO NOT EDIT ANY OTHER FILES.

After getting all the files into the same directory try running

```
python test.py
```

and you should see 
```
Your Python version: Python 3.6.5 :: Anaconda, Inc.

Running your program with this command: python main.py

RESULTS:
  Function test 1 (testGetNumRecords): Got exception unsupported operand type(s) for -: 'NoneType' and 'int' when running test 1
  Function test 2 (testGetName): function testGetName not found
  Function test 3 (testGetWindSpeed): function testGetWindSpeed not found
  Function test 4 (searchHurricane): function searchHurricane not found
  Function test 5 (searchHurricane): function searchHurricane not found
  Function test 6 (searchHurricane): function searchHurricane not found
  Function test 7 (searchHurricane): function searchHurricane not found
  Function test 8 (searchHurricaneByLocation): function searchHurricaneByLocation not found
  Function test 9 (searchHurricaneByLocation): function searchHurricaneByLocation not found
  Function test 10 (countHurricane): function countHurricane not found
  Function test 11 (countHurricane): function countHurricane not found
  Function test 12 (maxWindSpeedHurricane): function maxWindSpeedHurricane not found
  Function test 13 (minWindSpeedHurricane): function minWindSpeedHurricane not found
  Main function print test (Problem 1): expected (529) but found (0)
  Main function print test (Problem 2): expected (BABE) but found (0)
  Main function print test (Problem 3): PASS
  Main function print test (Problem 4): expected (False) but found (0)
  Main function print test (Problem 5): expected (JUNE) but found (0)
  Main function print test (Problem 6): expected (241) but found (0)
  Main function print test (Problem 7): expected (288) but found (0)
  Main function print test (Problem 8): expected (65) but found (0)
Score: 4%
```

# Directions

The order in which you should implement the functions are as follows:

## Step 1.
Implement the problems **1 - n1** in under the main function.

## Step 2.
Implement the `searchHurricane(name)` function.

This might be your first time attemping to implement a while loop.
As a recap, there are 3 important elements to remember when designing a loop:

1. The stopping condition. 
2. Code to run on every iteration of the loop.
3. An increment/decrement statement. 

A small framework to help you design a while loop has been givin in main.py for this function. This is given to demonstrate which element goes where in the loop.

* For this function you will be given the name of a hurricane as a parameter
and it is your goal to return `True` if the hurricane is in the database, and
`False` if it is not.

## Step 3. 
Implement the `searchHurricaneByLocation(latitude, longitude)` function.

* This function should be similar to what you did in the `searchHurricane()`
function.
* Just remember you have two values (i.e., `latitude` and `longitude`) that
need to match to one hurricane now.
* Instead of returning `True` or `False`, you need to return the name of the
hurricane at that location.
* If there are no hurricanes with the given `latitude` and `longitude`, then
this function should return `None`.  `None` is special value in python
which represents the absense of something. For example, in this case, `None`
signifies that there is no hurricane with the given `latitude` and `longitude`.


## Step 4.
Implement the `countHurricane(oceanName)` function.

* For this function you will still be looping over all the values in the dataset.
* Loop through the dataset and count each time you find a hurricane that is from the ocean indicated by oceanName.
* This function should take in the name of the ocean you are searching for as oceanName, and it should return the count of how many times it was found.
* If there are no hurricanes with the given `oceanName`, then this function should return 0 (zero).

## Step 5.
Implement `maxWindSpeed()` and `minWindSpeed()` functions.
* For this function you will need to loop through all the WindSpeed values in the dataset and determine the largest and smallest values.
* Your function should take in no parameters and return the largest/smallest wind speed value respectively.

## Step 6.
* Solve the problems **n1 - n2** in main using the functions that you have already created in the previous steps.
* This step just involves calling the functions that you designed in order to answer some questions that we have provided.
* It is important that you use your functions to solve these problems, so make sure that each of your solutions calls atleast one of the functions that you created.

