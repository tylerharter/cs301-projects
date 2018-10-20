# Project 7

For this assignment, we will be using the IMDB Movie dataset again.
However, this time you are given two files - `movies.csv` and `mapping.csv`.

`movies.csv` has 6 columns - `movie_id`, `release_year`, `rating`, `directors`, `actors`, `genres`

The contents look something like this
```
tt1931435,2013,5.6,nm0951698,nm0000134,"Comedy,Drama,Romance"
tt0242252,2001,6.1,nm0796124,"nm0048932,nm0000596,nm0004778","Drama,History,Romance"
tt0066811,1971,6.0,nm0125111,"nm0000621,nm0283499,nm0604702,nm0185281","Comedy,Family"
tt1691920,2011,6.0,nm0671210,"nm0005048,nm0000507,nm0005315,nm1605114",Drama
tt0224120,2000,4.9,nm0943044,nm0001299,"Drama,Mystery,Thriller"
tt0040724,1948,7.8,"nm0744504,nm0001328","nm0000078,nm0001050,nm0000974","Action,Adventure,Romance"
```

As seen above, this file has no names for movies, directors and actors. Those mappings are present in `mapping.csv`.

`mapping.csv` has 2 columns - `id`, `name`

The contents look something like this
```
nm0000001,Fred Astaire
nm0000004,John Belushi
nm0000007,Humphrey Bogart
tt0110997,The River Wild
tt0122151,Lethal Weapon 4
```

## Step 1: the `read_csv` function

Create a function `read_csv` that returns a *list of dictionaries* where each dictionary represents a movie as follows:

```
{ 
    "title": "<the movie title instead of the id>",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": ["directorname1", "directorname2", ....],
    "actors": ["actorname1", "actorname2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```

Since `movies.csv` doesn't have any of the names, first read `mapping.csv` and created a dictionary where the keys are ids and the values are names.
Then, when reading `movies.csv`, use the id's as keys and look for the values in the dictionary you previously created.

## Step 2: the `stats` function

Create a function called `stats` that takes the dataset (the list of dictionaries) as an argument.
This function should return a single dictionary that contains the following information in it.

|key|value|
|---|-----|
|num\_movies|The total number of distinct movie titles in the dataset|
|num\_actors|The total number of distinct actor names in the dataset|
|num\_directors|The total number of distinct director names in the dataset|
|num\_genres|The total number of distinct genres in the dataset|

NOTE: All the values should be integers!

In the `process_args` function, add a command for the `stats` function so that your main.py can run the following command.


```
python main.py stats
```
HINT: use sets!

## Step 3: The `top_n_actors` function

Create a function called `top_n_actors` that takes the dataset and an integer `n` as arguments.

This function should calculate a "score" for every actor, sort the actors in descending order of their scores and return the first `n` entries.
The "score" is calculated as the number of movies the actor has acted in.

This function should return a *list of dictionaries* of maximum length `n` where each dictionary contains the following information in it.

|key|value|
|---|-----|
|actor|The name of the actor|
|score|The score for the actor|

In the `process_args` function, add a command for the `top_n_actors` function so that your main.py can run the following command.

```
python main.py top_n_actors 10
```

## Step 4: the `top_n_versatile_actors` function

Create a function called `top_n_versatile_actors` that takes the dataset and an integer `n` as arguments.

This function is similar to top_n_actors except the score is going to be calculated based on the number of genres of movies they've acted in.

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

In the `process_args` function, add a command for the `top_n_versatile_actors` function so that your main.py can run the following command.

```
python main.py top_n_versatile_actors 10
```

## Step 5: the `top_n_directors` function

Create a function called `top_n_directors` that takes the dataset and an integer `n` as arguments.

This function should calculate a "score" for every director who has directed 5 or more movies, sort the directors in descending order of their scores and return the first `n` entries.
The "score" is calculated by using the [median](https://www.mathsisfun.com/definitions/median.html) of the reviews of movies by that director.

This function should return a *list of dictionaries* of maximum length `n` where each dictionary contains the following information in it.

|key|value|
|---|-----|
|director|The name of the director|
|score|The score for the director|

In the `process_args` function, add a command for the `top_n_directors` function so that your main.py can run the following command.

```
python main.py top_n_directors 10
```
