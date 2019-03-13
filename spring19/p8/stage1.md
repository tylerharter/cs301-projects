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
