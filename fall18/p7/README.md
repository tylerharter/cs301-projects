# Project 7

For this assignment, we will be using the IMDB Movie dataset again.

Download the files using the links below

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/main.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/test.py)
* [expected.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/expected.json)
* [small\_mapping.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/small_mapping.csv)
* [small\_movies.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/small_movies.csv)
* [movies.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/movies.csv)
* [mapping.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p7/mapping.csv)

You will be working mainly with movies.csv and mapping.csv.  
The small\_movies.csv and small\_mapping.csv have been provieded to help you debug any errors you may face while implementing Step 1.

`small_movies.csv` and `movies.csv` have 6 columns -   

`movie_id`, `release_year`, `rating`, `directors`, `actors`, `genres`

Here are a few rows from `movies.csv`

```
tt1931435,2013,5.6,nm0951698,nm0000134,"Comedy,Drama,Romance"
tt0242252,2001,6.1,nm0796124,"nm0048932,nm0000596,nm0004778","Drama,History,Romance"
tt0066811,1971,6.0,nm0125111,"nm0000621,nm0283499,nm0604702,nm0185281","Comedy,Family"
tt1691920,2011,6.0,nm0671210,"nm0005048,nm0000507,nm0005315,nm1605114",Drama
tt0224120,2000,4.9,nm0943044,nm0001299,"Drama,Mystery,Thriller"
tt0040724,1948,7.8,"nm0744504,nm0001328","nm0000078,nm0001050,nm0000974","Action,Adventure,Romance"
```

As seen above, this file has no names for movies, directors and actors. Those mappings are present in `mapping.csv`.  

`small_mapping.csv` and `mapping.csv` have 2 columns - `id`, `name`

Here are a few rows from `mapping.csv`

```
nm0000001,Fred Astaire
nm0000004,John Belushi
nm0000007,Humphrey Bogart
tt0110997,The River Wild
tt0122151,Lethal Weapon 4
```

## 1: Creating the list of movies

### 1.1 The `get_mapping` function:

> input(s) to this function:
> * mapping\_filename : a string representing the name of the mapping file.

This function should return a dictionary where the keys are the IDs from the file and the values are the names.


You can test your `get_mapping` function in the python console as follows:

```
>>> from main import get_mapping
>>> my_mapping = get_mapping("small_mapping.csv")
>>> 
>>> import json
>>> print(json.dumps(my_mapping, indent=2, sort_keys=True))
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

> There's some new code here that you may not have seen before - `json.dumps`. The [json module](http://json.org/) allows you to
> export and import data in a format that is easy to read.
> NOTE: For this assignment, make sure to only print your results using json.dumps as shown above.


*If everything until here is correct, your score from test.py should be `18%`.*

### 1.2 The `get_movies` function:

> input(s) to this function
> * movie\_filename : a string representing the name of the movie file.

This function should return a **list of dictionaries** where each dictionary represents a movie as follows:

```
{ 
    "title": "<the movie id>",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": [<director-id1>, <director-id2>, ...],
    "actors": ["actor-id1", "actor-id2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```

You can test your `get_movies` function in the python console as follows:
```
>>> from main import get_movies
>>> mymovies = get_movies("small_movies.csv")
>>>
>>> import json
>>> print(json.dumps(mymovies, indent=2, sort_keys=True))
[
  {
    "actors": [
      "nm0000131",
      "nm0000432",
      "nm0000163"
    ],
    "directors": [
      "nm0001219"
    ],
    "genres": [
      "Crime",
      "Drama",
      "Thriller"
    ],
    "rating": 7.1,
    "title": "tt0313542",
    "year": 2003
  },
  {
    "actors": [
      "nm0000154",
      "nm0000418",
      "nm0000997",
      "nm0752751"
    ],
    "directors": [
      "nm0001149"
    ],
    "genres": [
      "Action",
      "Crime",
      "Thriller"
    ],
    "rating": 7.6,
    "title": "tt0093409",
    "year": 1987
  }
]
>>>
```

*If everything until here is correct, your score from test.py should be `36%`.*

### 1.3 The `read_data` function:

> input(s) to this function
> * movie\_filename : a string representing the name of the movie file.
> * mapping\_filename : a string representing the name of the mapping file.

If you've noticed, the output of `get_movies` is a list of dictionaries, but the title, directors and actors have IDs instead of names. This function should convert those IDs into names.

This function should return a **list of dictionaries** where each dictionary represents a movie as follows:

```
{ 
    "title": "<the movie name>",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": [<director-name1>, <director-name2>, ...],
    "actors": ["actor-name11", "actor-name2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```

You can test your `read_data` function in the python console as follows:

```
>>> from main import read_data
>>> movies = read_data("small_movies.csv", "small_mapping.csv")
>>> import json
>>> print(json.dumps(movies, indent=2, sort_keys=True))
[
  {
    "actors": [
      "John Cusack",
      "Gene Hackman",
      "Dustin Hoffman"
    ],
    "directors": [
      "Gary Fleder"
    ],
    "genres": [
      "Crime",
      "Drama",
      "Thriller"
    ],
    "rating": 7.1,
    "title": "Runaway Jury",
    "year": 2003
  },
  {
    "actors": [
      "Mel Gibson",
      "Danny Glover",
      "Gary Busey",
      "Mitchell Ryan"
    ],
    "directors": [
      "Richard Donner"
    ],
    "genres": [
      "Action",
      "Crime",
      "Thriller"
    ],
    "rating": 7.6,
    "title": "Lethal Weapon",
    "year": 1987
  }
]
```

Notice that the actors, directors and the title all have names now!
*If everything until here is correct, your score from test.py should be `54%`.*

> NOTE: Make sure that your score is at `54%` before proceeding. The `read_data` function needs to be correct before you can start any of the steps below.

## Step 2: the `stats` function

> input(s) to this function:
> * movies : the list of dictionaries (the output of read\_data("movies.csv"))

This function should return a single dictionary that contains the following information in it.

|key|value|
|---|-----|
|num\_movies|The total number of distinct movie titles in the dataset|
|num\_actors|The total number of distinct actor names in the dataset|
|num\_directors|The total number of distinct director names in the dataset|
|num\_genres|The total number of distinct genres in the dataset|

NOTE: All the values should be integers!
HINT: use sets!

In the `process_args` function, just like in P6, add a command for the `stats` function so that your main.py can run the following command.

```
python main.py stats
```

Remember, when printing the output, use `json.dumps`!

*If everything until here is correct, your score from test.py should be `70%`.*

## Step 3: The `top_n_actors` function

> input(s) to this function:
> * movies : the list of dictionaries (the output of read\_data("movies.csv"))
> * n : the length of the list to be returned

This function should calculate a "score" for every actor, sort the actors in descending order of their scores and return the first `n` entries.
The "score" is calculated as the number of movies the actor has acted in.

This function should return a *list of dictionaries* of length `n` where each dictionary contains the following information in it.

|key|value|
|---|-----|
|actor|The name of the actor|
|score|The score for the actor|

In the `process_args` function, add a command for the `top_n_actors` function so that your main.py can run the following commands.

```
python main.py top_n_actors 0
python main.py top_n_actors 3
```

*If everything until here is correct, your score from test.py should be atleast `80%`.*

## Step 4: the `top_n_versatile_actors` function

Instead of scoring actors based on the number of movies they've acted in, we are going to score them based on the different types of genres they've acted in!

> input(s) to this function:
> * movies : the list of dictionaries (the output of read\_data("movies.csv"))
> * n : the length of the list to be returned

This function is similar to `top_n_actors` except the score is going to be calculated based on the number of genres of movies they've acted in.

For example, lets look at the movies "Kevin Bacon" has acted in (his actor id is nm0000102)

```
tt3813310,2015,6.3,nm1218281,"nm0000102,nm6627667,nm4881741,nm0924154","Crime,Thriller"
tt0790736,2013,5.6,nm0777881,"nm0005351,nm0000313,nm0000102","Action,Adventure,Comedy"
tt0485851,2007,6.9,nm0497528,"nm0000409,nm0000412,nm0000102","Crime,Drama,Thriller"
tt0110997,1994,6.3,nm0000436,"nm0000102,nm0000657,nm0001515","Adventure,Crime,Thriller"
tt0117665,1996,7.6,nm0001469,"nm0000134,nm0000102,nm0000093,nm0000574","Crime,Drama,Thriller"
```

He's acted in 5 movies, and the total number of genres for these movies is 6, so he gets a score of 6.

This function should return a *list of dictionaries* of maximum length `n` where each dictionary contains the following information in it.

|key|value|
|---|-----|
|actor|The name of the actor|
|score|The score for the actor|

In the `process_args` function, add a command for the `top_n_versatile_actors` function so that your main.py can run commands like the following.

```
python main.py top_n_versatile_actors 10
```

*If everything until here is correct, your score from test.py should be atleast `89%`.*

## Step 5: the `top_n_directors` function

> input(s) to this function:
> * movies : the list of dictionaries (the output of read\_data("movies.csv"))
> * n : the length of the list to be returned

This function should calculate a "score" for every director **who has directed 5 or more movies**, sort the directors in descending order of their scores and return the first `n` entries.
The "score" is calculated by using the [median](https://www.mathsisfun.com/definitions/median.html) of the reviews of movies by that director. Make sure to round this score down to 2 decimal places using the `round()` function.

This function should return a *list of dictionaries* of maximum length `n` where each dictionary contains the following information in it.

|key|value|
|---|-----|
|director|The name of the director|
|score|The score for the director|

In the `process_args` function, add a command for the `top_n_directors` function so that your main.py can run commands like the following.

```
python main.py top_n_directors 10
```

*If everything until here is correct, your score from test.py should be atleast `97%`.*

## Step 5: Getting from `97%` to `100%`

The `top_n_actors`, `top_n_versatile_actors` and `top_n_directors` functions sort based on scores. But what if two actors or two directors have the same score? How do you break such ties?
In order to get these last few points, you'll have to ensure that if two people get the same score, then they are ordered alphabetically.

For example, if we've computed scores for actors as

```
[
    {
      "actor": "John Cusack",
      "score": 18
    },
    {
      "actor": "Jeff Bridges",
      "score": 18
    },
    {
      "actor": "Kurt Russell",
      "score": 18
    },
    {
      "actor": "Brian Donlevy",
      "score": 17
    },
    {
      "actor": "Armand Assante",
      "score": 17
    },
]
```

Then all the names for the 18's should be sorted alphabetically, and so should the 17's, to get the following

```
[
    {
      "actor": "Jeff Bridges",
      "score": 18
    },
    {
      "actor": "John Cusack",
      "score": 18
    },
    {
      "actor": "Kurt Russell",
      "score": 18
    },
    {
      "actor": "Armand Assante",
      "score": 17
    },
    {
      "actor": "Brian Donlevy",
      "score": 17
    },
]
```
