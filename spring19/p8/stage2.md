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
 