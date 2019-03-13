# Stage 1: Data Plubming

A lot of data science work involves *plumbing*, the process of getting
data into a useful format.  Data plumbing is the focus of stage 1
(stage 2 is the fun part).

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

The following questions pertain to `small_mapping.csv` and
`small_movies.csv`, unless otherwise specified.

---

## Question 1: what is returned by your `get_mapping("small_mapping.csv")` function?

In addition to displaying the result in the `Out [N]` area, keep the
result in a variable for use in subsequent questions.

## Question 2: what is the value associated with the key "tt0313542"?

Use the dictionary returned earlier. Do not call `get_mapping` a
second time (that would be inneficient).

## Question 3: what are the values in the mapping associated with keys beginning with "tt"?

Answer with a Python list.

## Question 4: which keys in the mapping map to people with a first name of "Gary"?

Answer with a Python list.

---

Build a function that takes a path to a movies CSV (e.g.,
"small_movies.csv" or "movies.csv") as an parameter and returns a list
of dictionaries where each dictionary represents a movie as follows:

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

---

## Question 5:

Using this list of dictionaries that stores relevant details about
each movie, find out the list of actors for the 100th movie in the
list.

#### Question 6: 
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
