# Project 7

For this assignment, we will be using the IMDB Movie dataset again!
Like with Project 6, there will be no `project.py`. You're going to be working directly with the CSV file and using dictionaries!

## 1. Implement the `read_csv` function.

> ##### input(s) to this function :
> * `csv_filename` : the name of the csv file to read in

Our first step is to read in our CSV file and save it as a list of *dictionaries*.

Create a function called `read_csv` which takes a filename as the only parameter and returns all
the rows in the csv file as a list of dictionaries.

The CSV file has 6 columns and these are their names and datatypes.

> Column 1 : `title` : `string`  
> Column 2 : `release_year` : `int`  
> Column 3 : `rating` : `float`  
> Column 4 : `actors` : `list of strings`  
> Column 5 : `genre` : `string`  
> Column 6 : `revenue` : `int`  

## 2. Implement Functions to Analyze the Data

### 2.1 : 

Find actors who've acted in the most number of movies by keeping track of the number of movies per actor in a dictionary.

```
$> python main.py num_distinct_actors movies.csv
{ "num_distinct_actors": 100 }
```

### 2.2 :

Find all the genres in movies.csv. Make sure they are distinct!

```
$> python main.py genres movies.csv
{ "genres": [ "horror", "comedy", "thriller", ... ] }
```

### 2.3 :

Find the N most popular actors. We define popularity here as the number of movies an actor has acted in.

```
$> python main.py most_popular_actors movies.csv N
{
    "most_popular_actors": ["actor_1", "actor_2", .... "actor_N"],
}
```

### 2.4 :

Find the number of movies in the dataset per genre.

```
$> python main.py count_titles_by_genre movies.csv
{
    "count_titles_by_genre": {
        "horror": 20,
        "comedy": 25,
        "thriller": 10,
        ...
    }
}
```

### 2.5 : 

Find the number of actors in the dataset per genre.

```
$> python main.py count_actors_by_genre movies.csv
{
    "count_actors_by_genre": {
        "horror": 40,
        "comedy": 25,
        ...
    }
}
```

### 2.6 :

Find the highest rated movie per year in the dataset.

```
$> python main.py highest_rated_movie_per_year movies.csv
{
    "highest_rated_movie_per_year": {
        2010: "Movie 1",
        2011: "Movie 2",
        2012: "Movie 3"
    }
}
```

### 2.7 :

We're going to print out the top N most successful directors by looking at the total revenue of their movies.
We're also going to print out the highest rating and lowest rating.

```
$> python main.py most_successful_directors 5
{
    "most_successful_directors": [
        {"name": "Director 1", "highest_movie_rating": 9.8, "lowest_movie_rating": 5},
        {"name": "Director 2", "highest_movie_rating": 9.5, "lowest_movie_rating": 4},
        {"name": "Director 3", "highest_movie_rating": 9.3, "lowest_movie_rating": 3},
        {"name": "Director 4", "highest_movie_rating": 9.1, "lowest_movie_rating": 5},
        {"name": "Director 5", "highest_movie_rating": 8.8, "lowest_movie_rating": 7},
    ]
}
```

### 2.8 :

Find all actors who've acted in movies for N continuous years. i.e. Actor1 acted in movies released in 2010, 2011, 2012 (three consecutive years)

```
$> python main.py find_a_name_for_this
{
    "find_a_name_for_this": [
        {"name": "Actor 1", "num_consecutive_years": 3, "began_at": 2010},
        {"name": "Actor 1", "num_consecutive_years": 3, "began_at": 2010},
        {"name": "Actor 1", "num_consecutive_years": 3, "began_at": 2010},
    ]
}
```


### 2.9

```
$> python main.py general_stats movies.csv

{
    "num_movies": 200,
    "num_actors": 500,
    "genres": [ "comedy", "horror", ..... ],
    "oldest_year": 2010,
    "latest_year": 2018,
}
```
