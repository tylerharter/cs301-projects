# Stage 1: Data Plubming

A lot of data science work often involves *plumbing*, the process of
getting messy data into a more useful format.  Data plumbing is the
focus of stage 1.  We'll develop and test three functions that will be
helpful in stage 2:

1. `get_mapping(path)`
2. `get_raw_movies(path)`
3. `get_movies(movies_path, mapping_path)`

---

Start by writing a function that starts like this:

```python
def get_mapping(path):
```

When called, the `path` should refer to one of the mapping files
(e.g., "small_mapping.csv").  The function should return a dictionary
that maps IDs (as keys) to names (as values), based on the file
referenced by `path`.  For example, this code:

```python
mapping = get_mapping("small_mapping.csv")
print_dict(mapping)
```

Should print this:

```
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

Note that the mapping files DO NOT have a CSV header.

The following questions pertain to `small_mapping.csv` unless
otherwise specified.

---

#### Question 1: what is returned by your `get_mapping("small_mapping.csv")` function?

In addition to displaying the result in the `Out [N]` area, keep the
result in a variable for use in subsequent questions.

#### Question 2: what is the value associated with the key "tt0313542"?

Use the dictionary returned earlier. Do not call `get_mapping` a
second time (that would be inneficient).

#### Question 3: what are the values in the mapping associated with keys beginning with "tt"?

Answer with a Python list.

#### Question 4: which keys in the mapping map to people with a first name of "Gary"?

Answer with a Python list.  To get full points, you should write code
that will count somebody named "gary" but will not count somebody
named "Garyyy".

---

Build a function named `get_raw_movies` that takes a path to a movies
CSV (e.g., "small_movies.csv" or "movies.csv") as a parameter and
returns a list of dictionaries where each dictionary represents a
movie as follows:

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

Note that the movie files DO have a CSV header.

Also note that the values for keys ```directors, actors``` and
```genres``` is always a list, even if it has only one element.

---

## Question 5: what does `get_raw_movies("small_movies.csv")` return?

The result should be this:
```
[{'title': 'tt0313542',
  'year': 2003,
  'rating': 7.1,
  'directors': ['nm0001219'],
  'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'tt0093409',
  'year': 1987,
  'rating': 7.6,
  'directors': ['nm0001149'],
  'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
  'genres': ['Action', 'Crime', 'Thriller']}]
```

Also keep value returned by `get_raw_movies` in a variable.  You
should not call the function more often than necessary.

#### Question 6: how many genres did the movie at index 0 have?

Use the data from Q5.

#### Question 7: what is the ID of the last actor listed for the move at index 1?

Use the data from Q5.

---

Note that for the keys `actors`, `directors`, and `title`, we are only
able to store the IDs for the corresponding names. Write a function
named `get_movies(movies_path, mapping_path)` loads data from the
`movies_path` file using `get_movies_raw` and converts the IDs to
names using a mapping based on the `mapping_path` file, which you
should load using your `get_mapping` function.

Each dictionary in the list should look something like this:

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

Notice the difference between the previous one and this (names instead
of IDs). This list of dictionaries is extremely vital for almost all
of the following questions.

We recommend you get the translation from ID to name working for title
before you start trying to translate actors and directors.

After you implement your function (or implement enough of it to answer
some of the below questions), call it and store the result in `movies`
as follows:

```python
small = get_movies("small_movies.csv", "small_mapping.csv")
```

---

#### Question 8: what is `small[0]["title"]`?

Just paste `small[0]["title"]` into a cell and run it.  We're doing
this to check that the structures in `small` (as returned by
`get_movies` above) contain the correct data.

#### Question 9: what is `small[1]["directors"]`?

#### Question 10: what is `small[-1]["actors"]`?

#### Question 11: what is `small`?

The result should look like this:

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

---

If you've gotten this far, your functions must be working pretty well
with the small data.  So let's try the full dataset!

```python
movies = get_movies("movies.csv", "mapping.csv")
```

---

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
