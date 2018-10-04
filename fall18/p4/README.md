# Project 4

This project will primarily focus on providing further practice with
**conditional statments** and **loops**. You will also get some
experience accepting user input, and checking whether such inputs are
sane.  To start, download the test.py file to your project
directory.

* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/test.py)

**Note:** This project does not provide you a project.py (you won't be
needing it) or a main.py to start from (you can start from
scratch). You should hand in **main.py** file when you are done.

Your program will grade students and provide basic statistics when
requested.  Hence, no data file is necessary, because all data is
typed by the user.

# Overview

Below is an example of how a user might interact with your program
(parts typed by the user are in bold).

<pre>
ty-mac:p4$ <b>python main.py</b>
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>80</b>
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>70</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>a</b>
80.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$ 
</pre>

Your program should keep taking input until the user indicates they
want to exit.  There are five valid things the user may type, and here
is what your program should do in each case:

* **any number between 0 and 100**: the program should treat the number as a percent, and print a corresponding letter grade (between A and F)
* **q**: print "done" and quit running
* **c**: print the number of scores entered so far
* **a**: print the average score entered so far
* **r**: clear the statistics so that the number of scores entered is considered 0 and the average is reset

The user may also enter tricky input, including (but not limited to)
upper case commands (which should be accepted) and numbers over 100
(which should be rejected).

# Getting Started

There are a lot of tests this time (200 of them!), and many of them
are fairly complicated, so it's probably easier to start writing your
main.py directly and testing it yourself manually before you try
running our tests.  If you focus on writing a correct program, you
won't need to worry about looking at each of the 200 tests.

Your program will need to keep asking the user for input in a loop.
To get started, you could write a simple program that just echoes
input by writting the following in your new main.py file:

```python
while True:
    val = input("enter something: ")
    print(val)
```

Try running it:

<pre>
ty-mac:p4$ python main.py
enter something: <b>3</b>
3
enter something: <b>howdy</b>
howdy
enter something: <b>how do i exit?</b>
how do i exit?
enter something:   C-c C-cTraceback (most recent call last):
  File "main.py", line 2, in <module>
      val = input("enter something: ")
      KeyboardInterrupt
ty-mac:p4$ 
</pre>

The program contains an infinite loop, and the only way to stop it is
to kill it, by hitting control-C on your keyboard.

# Directions

The order in which you should implement the functions are as follows:

## Step 1
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

## Step 2
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

## Step 3
Implement the `searchHurricaneByLocation(latitude, longitude)` function.
* The purpose of this function is to find if a hurricane is present in the
dataset, given it's `latitude` and `longitude` as input.
* This function should be similar to what you did in the `searchHurricane()`
function.
* Just remember that you have two values (i.e., `latitude` and `longitude`) that
need to match to one hurricane now.
* Instead of returning `True` or `False`, you need to return the name of the
hurricane at that location.
* If there are no hurricanes with the given `latitude` and `longitude`, then
this function should return `None`.  `None` is special value in python
which represents the absence of something. For example, in this case, `None`
signifies that there is no hurricane with the given `latitude` and `longitude`.

## Step 4
Implement the `countHurricane(oceanName)` function.
* The purpose of this function is to compute and return the number of
hurricanes that occured in a particular ocean (e.g., Pacific), given the
ocean name as input.
* For this function, you will still be looping over all the values in the dataset.
* Loop through the dataset and increment a `counter` each time you find a hurricane that is from the ocean indicated by `oceanName`.
* This function should take in the name of the ocean you are searching for as `oceanName`, and it should return the count of how many times this `oceanName` was found in the dataset of hurricanes.
* If there are no hurricanes with the given `oceanName`, then this function should return 0 (zero).

## Step 5
Implement `maxWindSpeedHurricane()` function.
* The purpose of this function is to find and return the maximum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the largest value.
* Your function should take no parameters and should return the largest wind speed value.

## Step 6
Implement `minWindSpeedHurricane()` function.
* The purpose of this function is to find and return the minimum wind speed
among all the hurricanes in the dataset.
* For this function, you will need to loop through all the wind speed values in the dataset and determine the smallest value.
* Your function should take no parameters and should return the smallest wind speed value.

## Step 7
* Solve the problems 5 - 10 in main using the functions that you have already created in the previous steps.
* This step just involves **calling** the functions that you have already defined in order to answer some questions that we have asked.
* It is important that you use your functions to solve these problems. Make sure that each of your solution calls at least one of the functions that you created.

### Good luck with your hurricanes project! :)

