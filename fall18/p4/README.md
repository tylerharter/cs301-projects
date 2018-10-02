# Project 4

The project focuses on the IMDB movies dataset that contains a list of movies along with information like cast, director, rating, genre, plot description etc. You can open the IMDB-Movie-Data file in Excel or some other software to get an idea of what the dataset contains.

We will be working with **strings**, **loops**, **conditionals** and **command line arguments** in this project.

To start, download the 4 files given below into your project directory.

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p4/main.py)
* [project.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p4/project.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p4/test.py)
* [IMDB-Movie-Data.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p4/IMDB-Movie-Data.csv)

**A reminder:** You should make your changes ONLY to the **main.py** file.
DO NOT EDIT ANY OTHER FILES.

After downloading all the files into the same directory try running the command below:

```
python test.py
```

and you should see the following: 
```
To be filled

```

# Introduction to Command Line inputs

Important Note :  In this project we will be working on using commandline arguments to pass inputs to your program. Command-line arguments are specified while running the program file on the commandline. For example consider the following:

```python
python main.py upper "Steven Spielberg"
``` 

The above will pass the two arguments `upper` and `"Steven Spielberg"` to main.py via the command line and are called commandline arguments. We have written code inside the main.py file provided to you to read these arguments and provide to you for use in defining the functions for this project. The commandline arguments are called command1 and command2. There are a number of options that can be passed as command1 and command2 and they are described in the directions given below.


# Directions

It is recommended to follow the order mentioned below to complete this project:

## Step 1:

Read through the function we have provided in the main.py file and understand what it does. 
Try calling the function with different inputs to see changes in the output. To do this run the main.py file on commandline as follows:

```python
python main.py upper "Steven Spielberg"
STEVEN SPIELBERG
```

Look at the `main(command1, command2)` in main.py. The `if` statement compares command1 with `upper` and calls `convertCase` function on command2 to get the output. 

Now, write a similar `if` block for the `lower` command. Use the `convertCase` function we have provided, but be careful! You may need to change some of the arguments in the function call.
Try running the below command and check if your code is working as expected. 

```python
python main.py lower "Steven Spielberg"
steven spielberg
```

Make sure you understand how this works as you will need to code something similar for other functions in this project. 

**For each of the functions you define below, you will need to write similar if statements in `main(command1, command2)`, corresponding to their command line arguments**


## Step 2:

Now its time to write your first function for the project. 
This function must be called `reverseString(original_string)` and it should return the string that is obtained by reversing the input argument string original_string.

Example outputs from the function when its run from python terminal are given below:

```python
python main.py reverse "Apocalypse"
espylacopA
```

```python
python main.py reverse "Python Programming"
gnimmargorP nohtyP
```


For this function think about how you can use for loops and string indexing to reverse the string.

The function should be called if the command1 equals the word "reverse" followed by the string you want to reverse. 
Write an `if` block in `main(command1, command2)` to call reverseString(original_string) function when the first command line argument is "reverse".




## Step 3:

Our next function checks whether a string is a Palindrome or not. 

**A palindrome is a string which reads the same way even when its reversed**. For example 'SPACECAPS' and 'BOB' are palindromes. 

The function you are going to code is called `checkPalindrome(original_string)`. 
The function should be called when the `main.py` is run with commandline arguments "palindrome" followed by a string. For example:

```python
python main.py palindrome "Spacecaps"
True
```

```python
python main.py palindrome "Programming"
False
```
Write an `if` block in `main(command1, command2)` to call `checkPalindrome(original_string)` when the first command line argument is "palindrome".

**Important to keep in mind:**
1. Note that in output above, the case difference in the individual letters is to be ignored while deciding whether a string is Palindrome or not. For example, both "Elle" and "elle" are palindromes. For this,you might need to convert your original string to lowercase before checking for palindrome. You can use the convertCase function for this.
2. If you look closely, definition of palindrome requires the string to equal its reversed version. That should give you a hint that you can use the function you coded in step 2 to help you out in this function.


## Step 4:

Now that you have a correctly working palindrome function, we can finally focus on our dataset. 

Write a function called `findPalindromeMovie()`. 


For this function you need to search for a movie name that qualifies as a Palindrome in the dataset. 
It turns out that there is only one movie in the dataset that qualifies as a palindrome. **Hint:** Use the function you have defined above!

The function should be called when the main.py is run with the commandline argument "find_palin".
Write an `if` block in `main(command1, command2)` to call `findPalindromeMovie()` when the first command line argument is "find_palin".

For example:

```python
python main.py find_palin
```
(We have not shown the expected output of the above command! You should get an output ) 

**Here, note that there is only one command line argument necessary, as the function `findPalindromeMovie`does not have any input arguments**


## Step 5:

The next function is quite exciting as you get to create cool passwords from ordinary strings. This function is called `encodeString(original_String)` and it should replace all 'A' and a' with '@', all 'O' and 'o' with '0' and all 'I' and 'i' with '!' in the string and return the modified string.

Remember that strings are immutable in python and you should not attempt to modify the passed in string in place.

The function must be called when the main.py is run with the commandline arguments "encode" followed by the original string.
Write an `if` block in `main(command1, command2)` to call `encodeString()` when the first command line argument is "encode".

Some sample outputs of the function:
```python
python main.py encode "BALLOONS"
B@LL00NS
```

```python
python main.py encode "password incorrect"
p@ssw0rd !nc0rrect
```

## Step 6:

Let's explore our IMBD movies dataset! Open the `IMDB-Movie-Data.csv` file and have a look at the dataset. 
We have the following information about each movie: Title,Genre,Director,Cast,Year,Runtime,Rating,Revenue. 
Note that each movie also has an index, starting from 0. 

Like with previous projects, we have provided you with a function to help extract information from this dataset. 

Using the `getNumRecords()` function, you can get the total number of records in the dataset.
```python
>>> import project
>>> print(project.getNumRecords())
998
``` 
The `getMovieData(field, movie, index)` is a very versatile function, you can use it to get the following information about a movie: Index, Title, Genre, Director, Cast, Year, Runtime, Rating, Revenue. You should pass these as string arguments, corresponding to `field`.

**You need to provide EITHER the movie name OR the index value to this function**
 

The use of these functions is shown below:

(Passing the movie name as an argument)
```python
>>> import project
>>> print(project.getMovieData('Director',movie='Suicide Squad'))
David Ayer
>>> print(project.getMovieData('Cast',movie='Rogue One'))
Felicity Jones, Diego Luna, Alan Tudyk, Donnie Yen
``` 

(Passing the index as an argument)
```python
>>> import project
>>> print(project.getMovieData('Title',index=21))
Manchester by the Sea
>>> print(project.getMovieData('Director',index=33))
Tim Miller
```


Now, write a function to count the number of movies by a given director.

This function is called `countMoviesByDirector(director_name)` and it should return a number, equal to the number of movies in the dataset directed by `director_name`.

**Hint:** Remember how you worked with the Hurricanes dataset and found the number of hurricanes in a given ocean!

The function must be called when the main.py is run with the commandline arguments "count_by_director" followed by the name of the director. 
Write an `if` block in `main(command1, command2)` to call `countMoviesByDirector(director_name)` when the first command line argument is "count_by_director".

Some sample outputs of the function:
```python
python main.py count_by_director "Christopher Nolan"
5
```


## Step 7:

Lets try to see how many movies in the dataset have sequels. 

Write the `findNumSequels()` function. Find all movies in dataset which have a sequel called the name of the first movie followed by a 2. For example, "Cars" and "Cars 2" are both in the dataset. We want to find how many such **pairs** are in the dataset.  

**Hint**: You may need to use nested loops for this task (loop inside a loop!).

The function must be called when the main.py is run with the commandline arguments "num_sequels". 
Write an `if` block in `main(command1, command2)` to call `findNumSequels()` when the first command line argument is "num_sequels". (Notice that command2 is not necessary here)

```python
python main.py num_sequels
```
The correct output of the above is not shown!


## Step 8:

Lets find the main actor in a given movie!

Write the `mainActor(movie)` function. Find the main actor in a given movie (The main actor is considered to be the actor listed first in the cast). For example, the main actor in 'Guardians of the Galaxy' is Chris Pratt as their cast reads: Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana.

**Hint**: Find the index of the first comma in the cast and slice the string. 

The function must be called when the main.py is run with the commandline arguments "main_actor". 
Write an `if` block in `main(command1, command2)` to call `mainActor(movie)` when the first command line argument is "main_actor" followed by the name of the movie. 

```python
python main.py main_actor "Guardians of the Galaxy"
Chris Pratt
```

## Step 9:

Lets find how many movies in the dataset a given actor is in! 

Write a function to count the number of movies a given actor has acted in. 

This function is called `countMoviesByActor(actor_name)` and it should return a number, equal to the number of movies in the dataset directed by `actor_name`.

**Hint:** Get the cast for each movie in the dataset and use the string `find()` function you have studied to check if the actor is listed among the cast, and increment a counter accordingly. 

The function must be called when the main.py is run with the commandline arguments "count_by_actor" followed by the name of the actor. 
Write an `if` block in `main(command1, command2)` to call `countMoviesByActor(actor_name)` when the first command line argument is "count_by_actor".

Some sample outputs of the function:
```python
python main.py count_by_actor "Nicole Kidman"
6
```


## Step 10:

Write a function to find the highest budget of all movies released in a given year in the dataset. 

This function is called `findHighestRevenue(year)`. 

**IMPORTANT POINT TO NOTE:**
The budgets given in the dataset are *dirty*, meaning that they are not all uniformly formatted. Open up the dataset and note that sometimes budget is just a number, while other data entries have a number followed by an 'M'. For example, 'Guardians of the Galaxy' has a budget of "333.13" while 'Prometheus' has a budget of "126.46M". 

The `getMovieData` function will return the budget as a string. You will need to perform some *data cleanup* on your own for this task! 
You need to check whether the budget is a number or whether it has an 'M' after it. If so, you will need to slice the string before converting to float. 

The function must be called when the main.py is run with the commandline arguments "highest_rev" followed by the year. 
Write an `if` block in `main(command1, command2)` to call `findHighestRevenue(year)` when the first command line argument is "highest_rev".

Some sample outputs of the function:
```python
python main.py highest_rev 2016
Rogue One
```

```python
python main.py highest_rev 2014
American Sniper
```




### Good luck! :)
