# Draft!  Don't start this stage yet, because it is still being revised.

# Stage 2: Bucketing and Summarizing

In stage 1, you took data in a cumbersome form (everything was a
string and the data contained IDs instead of names) and converted it
to something more useful, namely lists of movie dictionaries.  In this
stage, you'll be doing analysis on data in that more useful form.
Much of your analysis will take the form of categorizing (aka
bucketing) movies, then computing simple stats over each bucket.  Some
movies will belong to multiple buckets (for example, a movie with
multiple genres, in the case that we're categorizing by genre).

You'll need to re-download `test.py` to begin this stage.  Note that
some questions involve creating plots.  Our tests can only detect the
whether a plot has been created, not whether the plot matches our
requirements, so double check for yourself that the plots look correct
to avoid deductions during code review.

## Implementing the `bucketize` Function

Implement the following function:

```python
def bucketize(movie_list, movie_key):
    # TODO: return dict of lists of movie dicts
```

The `movie_list` parameter accepts a list of dictionaries, such as
those in the `movies` or `small` variables from stage 1.  To refresh
your memory, `small` should look like this:

```
[{'title': 'Runaway Jury',
  'year': 2003,
  'rating': 7.1,
  'directors': ['Gary Fleder'],
  'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'Lethal Weapon',
  'year': 1987,
  'rating': 7.6,
  'directors': ['Richard Donner'],
  'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
  'genres': ['Action', 'Crime', 'Thriller']}]
```

The `movie_key` parameter should refer to some key that exists in
every dictionary in `movie_list`.  For example, for the above
dictionaries, `movie_key` might contain "title", "year", "actors",
etc.

The result returned by the `bucketize` should be a dictionary of
lists.  The **keys** of the result dictionary should be the values of
the `movie_list` dictionaries that are looked up by `movie_key`.  For
example, if `movies_list` refers to the `small` data shown above and
`movie_key` is "year", then the keys in the returned dictionary will
be 2003 and 1987 because `movies_list[0][movie_key]` is 2003 and
`movies_list[1][movie_key]` is 1987.

The **values** of the returned dictionary will be lists of movie
dictionaries from `movies_list`.  For example, suppose the following
call is made:

```python
buckets = bucketize(small, "year")
```

In this case, `bucktes[2003]` will be a list of movie dicts for the
movies made in 2003 (in this case, just *Runaway Jury*).  Concretely,
`buckets` should be the following:

```python
{2003: [{'title': 'Runaway Jury',
   'year': 2003,
   'rating': 7.1,
   'directors': ['Gary Fleder'],
   'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
   'genres': ['Crime', 'Drama', 'Thriller']}],
 1987: [{'title': 'Lethal Weapon',
   'year': 1987,
   'rating': 7.6,
   'directors': ['Richard Donner'],
   'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
   'genres': ['Action', 'Crime', 'Thriller']}]}
```

**Special Case:** if `m[movie_key]` for a movie `m` in `movie_list` is
a list, then `m` should end up in multiple lists in the returned
dictionary.  For example, suppose this code is run:

```python
buckets = bucketize(small, "genres")
```

In this case, `buckets["Crime"]`, `buckets["Drama"]`, and
`buckets["Thriller"]` will all contain the movie dict for *Runaway
Jury*, because that movie has three categories and therefore belongs
in multiple categories.

The first couple questions just involve testing your `bucketize`
function, which should work with any list of dicts (even those not
technically describing movies).  To get some test data, paste the
following cell:

```python
test_movies = [
{"title": "A", "year": 2018, "style": "short", "genres": ["g1"]},
{"title": "B", "year": 2018, "style": "long",  "genres": ["g2"]},
{"title": "C", "year": 2019, "style": "short", "genres": ["g3"]},
{"title": "D", "year": 2019, "style": "long", "genres": ["g1", "g2", "g3"]},
]
```

#### Question 21: what is `bucketize(test_movies, "year")`?

Expected answer:

```
{2018: [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
  {'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']}],
 2019: [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
  {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]}
```

Note that the *A* and *B* dictionaries are in the 2018 bucket and *C*
and *D* are in the 2019 bucket.

#### Question 22: what is `bucketize(test_movies, "style")`?

Expected answer:

```
{'short': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
  {'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']}],
 'long': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
  {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]}
```

#### Question 23: what is `bucketize(test_movies, "genres")`?

Expected answer:

```
{'g1': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
  {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
 'g2': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
  {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
 'g3': [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
  {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]}
```

This one is tricky!  Notice how movie *D* shows up in all three
buckets because we're bucketizing by genre, and *D* is falls under all
three genre categories.

#### Question 24: what is `bucketize(small, "genres")`?

Remember that `small` is where we stored the value returned by
`get_movies` in stage 1 when we loaded data from the
"small_movies.csv" file.

Expected answer:

```
{'Crime': [{'title': 'Runaway Jury',
   'year': 2003,
   'rating': 7.1,
   'directors': ['Gary Fleder'],
   'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
   'genres': ['Crime', 'Drama', 'Thriller']},
  {'title': 'Lethal Weapon',
   'year': 1987,
   'rating': 7.6,
   'directors': ['Richard Donner'],
   'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
   'genres': ['Action', 'Crime', 'Thriller']}],
 'Drama': [{'title': 'Runaway Jury',
   'year': 2003,
   'rating': 7.1,
   'directors': ['Gary Fleder'],
   'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
   'genres': ['Crime', 'Drama', 'Thriller']}],
 'Thriller': [{'title': 'Runaway Jury',
   'year': 2003,
   'rating': 7.1,
   'directors': ['Gary Fleder'],
   'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
   'genres': ['Crime', 'Drama', 'Thriller']},
  {'title': 'Lethal Weapon',
   'year': 1987,
   'rating': 7.6,
   'directors': ['Richard Donner'],
   'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
   'genres': ['Action', 'Crime', 'Thriller']}],
 'Action': [{'title': 'Lethal Weapon',
   'year': 1987,
   'rating': 7.6,
   'directors': ['Richard Donner'],
   'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
   'genres': ['Action', 'Crime', 'Thriller']}]}
```

#### Question 25: how many different unique actors appear in the `small` dataset?

Hint: `bucketize(small, "actors")` bucketizes movies based on actors,
so the number of buckets will correspond to the number of unique
actors.  In other words, `len(bucketize(small, "actors"))` is the
number of unique actors.

#### Question 26: how many unique genres appear in the full dataset?

**Note:** for this and all remaining questions, answer with respect to
the full dataset referenced by the `movies` variable (we'll ask
nothing more regarding `small` or `test_movies`).**

#### Question 27: how many movies are there of each genre?

Answer with a dictionary where each key is a genre and each value is
how many movies have that genre, like this:

```
{'Comedy': 485,
 'Drama': 1094,
 'Romance': 352,
 'History': 73,
 'Family': 85,
 'Mystery': 121,
 'Thriller': 250,
 'Action': 299,
 'Crime': 357,
 'Adventure': 283,
 'Western': 226,
 'Music': 38,
 'Animation': 45,
 'Sport': 48,
 'Fantasy': 59,
 'War': 99,
 'Sci-Fi': 69,
 'Horror': 85}
```

Hint: many of these questions can be reframed as questions about buckets.  For example:
* how many buckets are there?
* how many items are there in each bucket?

#### Question 28: how many movies are there of each genre? (plot your answer)

Yes, this is the same as q27, but now you must answer with a plot
rather than a dictionary.  Your plot should look like this:

<img src="genre_count.png" width="400">

Note for plot-based, the tests are only checking that a plot exists.
If a plot is not correct, your reviewer will manually deduct points.

#### Question 29: how many movies are there of each genre, prior to 2000? (plot your answer)

#### Question 30: how many movies are there of each genre, in or after 2000? (plot your answer)

Take a moment to compare the this and the previous plots.  What can
you infer?  What genres have grown in popularity?  Which ones have
fallen out of favor in recent years?

#### Question 31: how many movies have there been per year, since (and including) 2000? (plot your answer)

Hint: if you've written a general function to help with the previous
questions and you've kept the relevant data in a variable, you can
answer this with one simple line of code.

#### Question 32: what are the directing career spans of the directors who have directed for at least 30 years?

The span is the difference in years between year of the first movie
they directed and the last one they directed.  Answer with a
dictionary mapping name to years worked.  It should look like this:

```
{'Howard Hawks': 42,
 'Charles Chaplin': 34,
 'Henry Hathaway': 36,
 'Stanley Kubrick': 46,
 'Taylor Hackford': 32,
 'Cecil B. DeMille': 30,
 'Lee H. Katzin': 30,
 'Richard Fleischer': 32,
 'Sidney Lumet': 33,
 'George Sherman': 33,
 'John Huston': 30,
 'Robert Siodmak': 30,
 'Eldar Ryazanov': 31,
 'Martin Ritt': 32}
```

#### Question 33: what are the acting career spans of the actors who have acted for at least 40 years?

#### Question 34: who are the 10 directors with the longest careers?

Answer with a list of dictionaries, such that each dictionary specifies a name and span, like this:

```
[{'name': 'Mickey Rooney', 'span': 75},
 {'name': 'Anthony Quinn', 'span': 61},
 {'name': 'George Burns', 'span': 60},
 {'name': 'Dean Stockwell', 'span': 53},
 {'name': 'Glenn Ford', 'span': 52},
 {'name': 'James Caan', 'span': 52},
 {'name': 'Robert Mitchum', 'span': 51},
 {'name': 'Kurt Russell', 'span': 50},
 {'name': 'Robert De Niro', 'span': 49},
 {'name': 'Marlon Brando', 'span': 49}]
```

This is a little tricky, so we'll sketch out a part of a function for
you to complete that will help you find the answer:

```python
def row_ranking(row):
    return row["span"]

def top_n_span(buckets, n):
    # TODO: spans should be a dictionary mapping name to career span
    spans = ????
    rows = []
    for name in spans:
        span = ????
        rows.append({"name": name, "span": span})

    # we want to sort the rows so that those with the biggest spans
    # are first.  Notice that we aren't calling row_ranking, but rather
    # passing a reference to this function to the sort method.  The sort
    # method uses this function to determine how to rank the rows.
    # 
    # we do a reverse sort because we want the biggest spans first,
    # not last
    rows.sort(key=row_ranking, reverse=True)

    # TODO: return a slice of the rows
```

#### Question 35: who are the 10 directors with the longest careers?

Answer with the same format as above.

TODO
- counting buckets
- counting values in buckets (+plots)
- counting values in buckets with filter (+plots)
- year spread per actor/director
- median rating per year with > 10 movies
- best 5 years for movies

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
 