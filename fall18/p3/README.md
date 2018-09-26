# Project 3

This project will focus on conditional statments and loops, to start download these files
For those using pycharm, it may be easier to make the new project before downloading the files so you can save the files to the new directory created

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/main.py)
* [project.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/project.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/test.py)
* [area.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/hurricane.csv)

A reminder: only make changes to the main.py file as that is the only one that you will be turning in

after getting all the files into the same directory try running 

```
python test.py
```

you should see 
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

The Order in which you should implement the functions are as follows

## Step 1.
implement the first three functions in the main.py file.

These should be:

1. testGetNumRecords()
2. testGetName(row)
3. testGetWindSpeed(row)

* Reminder: quite a few things in computer science are indexed by 0, this means that the 1st row of the dataset would actually be located at the 0th index. Remember to do this small conversion
* These three functions are simple shells which will just test your ability to use the functions provided in the project.py file
* the first function has been made into a shell using pass to demonstrate how to design function shells in this manner


## Step 2.
Implement the search hurricane function

this might be your first time attemping to implement a while loop.
As a recap there are 3 important elements to remember when designing a loop

1. The stopping condition 
2. Code to be implemented on Every Loop
3. An increment/decrement 

 a small framework to help you design a while loop has been givin in main.py, this should help to demonstrate which element goes where

For this function you will be given the name of a hurricane as a parameter and it is your goal to return true if the hurricane is in the database, and false if it is not




## Step 3. 

Implement the searchHurricaneByLocation(lat, long) function

* this function should be similar to what you did in the searchHurricane function
* Just remember you have two values that need to match to one hurricane now
* Instead of returning true or false, you need to return the name of the hurricane at that location

## Step 4.

Implement the countHurricane(oceanName) function

* For this function you will still be looping over all the values in the dataset
* However now we aren't looking for one item, but rather looking for a whole lot of items
* loop through the dataset and count each time you find an item that its from the ocean indicated by oceanName
* this function should take in the name of the ocean you are searching for as oceanName, and it should return the count of how many times it was found


## Step 5.

Implement Max/Min WindSpeed() functions
* For this function you will need to loop through all the WindSpeed values in the dataset and determine the largest and smallest values
* your function should take in no parameters and return the largest/smallest value respectively 

## Step 6.

* Solve the problems in main using the functions that you have already created in the previous steps
* This step just involves calling the functions that you designed in order to answer some questions that we provided.
* It is important that you use your functions to solve these problems, so make sure that each of your solutions calls atleast one of the functions that you created




