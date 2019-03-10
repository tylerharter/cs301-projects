# Project 8

## Description

Having worked our way through soccer and hurricanes, we are now going to work on the IMDB Movies Dataset. A very exciting fortnight lies ahead where we find out some cool facts about our favorite movies, actors and directors.

Find the required files at the following links: 

- [project.py](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/project.py)
- [test.py](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/test.py)
- [small_mapping.csv](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/small_mapping.csv)
- [small_movies.csv](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/small_movies.csv)
- [mapping.csv](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/mapping.csv)
- [movies.csv](https://github.com/tylerharter/cs301-projects/blob/P8/spring19/p8/movies.csv)

You will be working mainly with *movies.csv* and *mapping.csv*. The *small_movies.csv* and *small_mapping.csv* have been provided to help you debug any errors you may face while implementing Step 1.

*small_movies.csv* and *movies.csv* have 6 columns -

```movie_id, year, rating, directors, actors, genres```

Here are a few rows from movies.csv: 
```
tt1931435,2013,5.6,nm0951698,nm0000134,"Comedy,Drama,Romance"
tt0242252,2001,6.1,nm0796124,"nm0048932,nm0000596,nm0004778","Drama,History,Romance"
tt0066811,1971,6.0,nm0125111,"nm0000621,nm0283499,nm0604702,nm0185281","Comedy,Family"
```

*small_mapping.csv* and *mapping.csv* have 2 columns - id, name

Here are a few rows from mapping.csv:

```
nm0000001,Fred Astaire
nm0000004,John Belushi
nm0000007,Humphrey Bogart
tt0110997,The River Wild
```

Essentially, each of those weird alphanumeric sequence is a unique identifier for either an actor or a director or a movie title. 

Create a *main.ipynb* file with function definitions as required to solve the following problems, while using the *mapping.csv* and *movies.csv* files. You can use *small_movies.csv* and *small_mapping.csv* as toy-datasets only for self verification purposes and not for submission purposes.

Before we move ahead with the problems, you should familiarize yourself with the utility functions provided to you in the ```project.py``` file.

## Utility functions provided: 

- ```print_dict(dictionary)``` : This prints out any dictionary that you provide as an argument to this function in a nice, compact fashion. If any question expects you to return a dictionary as an answer, make sure you use this function to print it. 
Usage: 
```python
>>> import project
>>> sample_dictionary = {"dogs":"pet","cat":"pet","tiger":"wild"}
>>> project.print_dict(sample_dictionary)
{
  "cat": "pet",
  "dogs": "pet",
  "tiger": "wild"
}

```
- ```dictionary_sort(dictionary, reverse = True)```: This function sorts a dictionary based on its values in descending order. If you need to sort the dictionary in ascending order, set the ```reverse``` argument of the function to ```False```. 
Usage: 

```python
>>> sample_dictionary = {"UW Madison": 1848, "UW Green Bay" : 1965, "UW Milwaukee" : 1956, "UW Eau Claire": 1916}
>>> ordered_dictionary = project.dictionary_sort(sample_dictionary)
>>> ordered_dictionary_reverse = project.dictionary_sort(sample_dictionary, reverse = False)
>>> project.print_dict(ordered_dictionary)
[
  [
    "UW Green Bay",
    1965
  ],
  [
    "UW Milwaukee",
    1956
  ],
  [
    "UW Eau Claire",
    1916
  ],
  [
    "UW Madison",
    1848
  ]
]
>>> project.print_dict(ordered_dictionary_reverse)
[
  [
    "UW Madison",
    1848
  ],
  [
    "UW Eau Claire",
    1916
  ],
  [
    "UW Milwaukee",
    1956
  ],
  [
    "UW Green Bay",
    1965
  ]
]
```

Notice that this function returns a list of tuples sorted on the foundational year of each of these institutions.

## 1. Week 1
### Step 1: A mapping function

Define a function that builds a dictionary where the keys are the IDs(remember the weird alphanumeric strings?) and the values are the corresponding names. Inputs to this function should be the mapping file. Upon calling the function, one should find something like this:

```python
mapping1 = get_mapping("small_mapping.csv")
print_dict(mapping1)

{
  "nm0000131": "John Cusack",
  "nm0000154": "Mel Gibson",
  "nm0000163": "Dustin Hoffman",
  "nm0000418": "Danny Glover",
  "nm0000432": "Gene Hackman",
  "nm0000997": "Gary Busey",
  "nm0001149": "Richard Donner",
  "nm0001219": "Gary Fleder",
  "nm0752751": "Mitchell Ryan",
  "tt0093409": "Lethal Weapon",
  "tt0313542": "Runaway Jury"
}
```
While solving for the project, don't use the toy dataset.

#### Question 1

Find out the corresponding value for the key **nm0000233** while using the newly built dictionary.

#### Question 2

Build a dictionary uses the names as keys and the IDs as corresponding values. Use this dictionary to find out the ID for **John Cusack**.


### Step 3: List of dictionaries

Build a function that takes ```movies.csv``` as an input argument and returns a list of dictionaries where each dictionary represents a movie as follows:

```python
{ 
    "title": "movie-id",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": ["director-id1", "director-id2", ...],
    "actors": ["actor-id1", "actor-id2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```
Note that the values for keys ```directors, actors``` and ```genres``` is always a list, even if it has only one element.

#### Question 3
Using this list of dictionaries that stores relevant details about each movie, find out the list of actors for the 100th movie in the list.

#### Question 4
Using the same list, find out the list of genres associated with the 235th movie in the list.


### Step 4: Using both files

Note that for the keys ```actors, directors ```and ```movie titles```, we are only able to store the IDs for the corresponding names. Build a function that replaces these IDs with their corresponding names. Input arguments to this function should be both the mapping and movies files. Each dictionary in the list should look something like:

```python
{ 
    "title": "the movie name",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": ["director-name1", "director-name2", ...],
    "actors": ["actor-name1", "actor-name2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```
Notice the difference between the previous one and this. This list of dictionaries is extremely vital for almost all of the following questions.

#### Question 5
Using this list of dictionaries that stores relevant details about each movie, find out the list of actors for the 100th movie in the list.

#### Question 6
Using the same list, find out the movie title for the 235th movie in the list.


### Step 5: Basic Statistics
Using the dictionary developed above, build a function to develop the four following lists:

List Type     | List contents
------------- | -------------
actors_list   | List of all unique actors
directors_list| List of all unique movie directors
movies_list   | List of all movie titles
genres_list   | List of all unique genres

Note that an actor or a director can appear in more than one movie, but the list should contain only one instance. The same reasoning applies to genres as well. 


#### Question 7
Return the entire list of genres found out using the above function.

#### Question 8
Return the last 5 movie titles from the movies_list found out using the function above.


#### Question 9
**Stats Function** : Build a function that takes in all the lists you created above as input arguments and returns a dictionary of stats that should have the following structure:


key          |	value 
-------------|---------------------------------------------------------
num_movies	 |The total number of distinct movie titles in the dataset
num_actors	 |The total number of distinct actor names in the dataset
num_directors|The total number of distinct director names in the dataset
num_genres	 |The total number of distinct genres in the dataset



## Week2

Over the span of this portion, we will be using the list of movie dictionaires we created in Step 4 of Week 1 to derive some interesting insights from the dataset provided.

<!--
### Step 1 : Career Activity of Actors and Directors
Build a function that takes in the following inputs:
  - List of movie dictionaries built in Step 4 of week1
  - use case: String variable that can be "actors" or "directors" depending on use case
  - start : List start index used to slice the sorted list
  - end: List end index used to slice the sorted list
The function should return a list of tuples that that indicate the number of movies that each actor(or director, depending on use case). has been involved in. If you run the function with appropriate parameters, it should return something like:
```python
>>>career_span(movie_dict, "directors", 0, 10)
>>>[('John Ford', 21),
 ('Henry Hathaway', 19),
 ('George B. Seitz', 15),
 ('Robert N. Bradbury', 13),
 ('Budd Boetticher', 12),
 ('George Marshall', 12),
 ('Charles Chaplin', 11),
 ('Stanley Kubrick', 11),
 ('Edwin L. Marin', 11),
 ('George Sherman', 11)]
 ```
>**Hint:** Build a function that iterates over all the movies in the list of dictionaries and keeps a simple count of the number of instances where a director appears. Sort this dictionary using the ```dictionary_sort()``` function provided.
#### Question 10
Return the list top 5 actors who have appeared on the maximum number of movies, while using the function built above.
#### Question 11
Return the list top 5 directors who have directed the maximum number of movies, while using the function built above.
#### Question 12
By using proper ```start``` and ```end``` parameters, return the 6th highest to 12th highest actors in terms of the number of movies they have acted in.

-->

### Step 1 : Movies per year

Build a function that takes in the following inputs:

  - List of movie dictionaries built in Step 4 of week1
  - year as integer
  
 The function should return the number of movies made in a specific year as an integer.
 
 #### Question 10
 Return the number of movies made in the year 2000
 
 #### Question 11
 Return the number of movies made in the year 1940
 
 #### Question 12
 Return the year from the decade beginning 1990 in which the maximum movies were made. 




### Step 2 : Career Span of Actors and Directors

Build a function that takes in the following inputs:

  - List of movie dictionaries built in Step 4 of week1
  - use case: String variable that can be "actors" or "directors" depending on use case
  - start : List start index used to slice the sorted list
  - end: List end index used to slice the sorted list

The function should return a list of tuples that that indicate the career span of each actor(or director, depending on use case). If you run the function with appropriate parameters, it should return something like:

```python
>>>career_span(movie_dict, "actors", 0, 10)
>>>[('Mickey Rooney', 75),
 ('Anthony Quinn', 61),
 ('George Burns', 60),
 ('Dean Stockwell', 53),
 ('Glenn Ford', 52),
 ('James Caan', 52),
 ('Robert Mitchum', 51),
 ('Kurt Russell', 50),
 ('Robert De Niro', 49),
 ('Marlon Brando', 49)]
 ```
The output shown above simply means that Mickey Romney has acted for 75 years, Anthony Quinn for 61 years and so on.

#### Question 13
Return the list top 5 actors who have had the longest career spans, while using the function built above.


#### Question 14
Return the list top 5 directors who have had the longest career spans, while using the function built above.


#### Question 15
By using proper ```start``` and ```end``` parameters, return the 9th highest to 15th highest directors in terms of their career spans.


### Step 3: Genre Specific Movies

Build a function that takes in the following inputs:

  - List of movie dictionaries built in Step 4 of week1
  - Genre Category as a string
 
The function should return a list of all the movies that is associated with that genre. 

> *Hint*: While iterating through the movie list, keep updating a dictionary whose key values are all the genres and corresponding value is a list of all the movies associated with it. Upon completion, you can use the second argument for the function as a key value to retrieve the associated movie list.


Upon running the function with appropriate parameters, one should get an output similar to this:
```python
>>>genre_list(movie_dict, "Horror")
>>>['Hide and Seek',
 'Enemy from Space',
 'Night Train',
 'Haunted Gold',
 "Soul's Midnight",
 'Creeper',
 'Repossessed',
 'The Night Walker',
 'The Changeling',
 'Garden of the Dead',
 'The Quatermass Xperiment',
 'Solstice',
 'John Dies at the End',
 'I Spit on Your
 ...
 ...
 ]
 ```
 
 
#### Question 16
Return the list of all movies associated with the genre "Action".


#### Question 17

Return the list of all movies associated with the genre "Thriller".

 
### Step 4: Best Years of Movie


Build a function that takes in the following inputs:

  - List of movie dictionaries built in Step 4 of week 1
  - start : List start index used to slice the sorted list
  - end: List end index used to slice the sorted list
  
The function should return a list of tuples that are sorted on the basis of the average rating of all movies released in a specific year. 

If you run the function with appropriate parameters, the output should look something like:
```python
>>>year_ratings(movie_dict,0,10)
>>>[(1921, 8.3),
 (1925, 8.2),
 (1919, 7.5),
 (1923, 7.3),
 (1962, 7.17),
 (1964, 7.16),
 (1928, 7.0),
 (1957, 6.91),
 (1947, 6.91),
 (1940, 6.9)]
 ```
 
You can use the ```dictionary_sort()``` function.
Note: The average rating can be calculated as the ratio of sum of ratings of all movies released in a year and the number of movies released in that specific year.
 

 
#### Question 18
Return the top 5 years of movie based on average rating

#### Question 19
Return the worst 5 years of movie based on average rating

#### Question 20
Return the top 7th to 15th years of movie based on average rating
 
