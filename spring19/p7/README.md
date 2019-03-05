# DRAFT!!!

# Project 7: Fédération Internationale de Football Association (Soccer!)

Let's Play Fifa18, Python style!  In this project, you will get more
practice with lists and start using dictionaries.  Start by
downloading `test.py` and `Fifa18.csv`.  This dataset is too large to
preview on GitHub (>17K rows), but you can view the
[raw version](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/spring19/p7/Fifa18.csv)
or using a program such as [Excel](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/excel.md).
You can also preview the first 100 rows [here](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/preview.md).
For this project, you'll create a new `main.ipynb` and answer
questions in the usual format.

## The Data

Try to familarize yourself with the data before starting the
analysis. We have players belonging to a wide range of nationalities
and clubs in Fifa18. As you can see the numeric data includes their
weekly wages (in Euros) (Yes, wages are per week!), net worth of the
player (in Euros) and the performace rating (score out of 100). For
instance, the player named "Neymar" is associated with Brazil, and is
signed up by club "Paris Saint-Germain", and is paid a weekly wage of
280000 Euros.

To ingest the data to your notebook, paste the following in an early cell:

```python
fifa_file = open('Fifa18.csv', encoding='utf-8')
file_reader = csv.reader(fifa_file)
player_data = list(fileReader)
for row in player_data[1:]:
    for idx in [2,6,7,8]:
        row[idx] = float(row[idx])
```

Consider peeking at the first few rows:
```python
for row in player_data[:5]:
    print(row)
```

It's up to you to write any functions that will make it more
convenient to access this data.

## Let's Start!

###### Define a function named "get_value" with two parameters named row_index and col_index. You should return "out_of_bounds" if the row or column indices are out of range of our list.
###### Reminder! Both column and row start with index 0

#### Question 1

Get the value of a cell using the  by passing the arguments row_index as 10 and col_index as 3 in get_value function. You should call the function you just created with these parameters.

#### Question 2

Call get_value and pass the values 17469,8 to the function.

---
#### Question 3

Write a function to return the name of the highest paid player in this roster and then call this function.

#### Question 4

Get the name and club of the highest net worth player in the list using a function. Return the values in the form of (name, club) from this function.

---
###### Next we are going to create a get_column function that returns an entire column from the dataset. There should be one parameter for this function col_idx.

For example, if the dataset is

```
[
    ["a", "b", "c"],

    ["d", "e", "f"],

    ["g", "h", "i"]

]
```

Then column 0 is `["a", "d", "g"]`, column 1 is `["b", "e", "h"]`, column 2 is `["c", "f", "i"]`.

The function `get_column` should return the entire column (a list) at position `col_idx`.

In the above example, `get_column(1)` should return `["b", "e", "h"]`

You're going to be using this function a lot, as it's a very common operation (getting an entire column), so make sure it works perfectly! Make sure it returns "out_of_bounds" when the column index is out of range.

#### Question 5
Get the list of nationalities in the dataset using the get_column function you defined above.
Output the first 5 elements as a list from this column list to the out cell.

#### Question6

Get the list of names of the players using the same function, but this time output a list of first 5 names after alphabetically sorting them.

---
#### Question 7

Output the average of the net worth of all the players in this roster.

#### Question 8

Which country's players have the least average age- Argentina, Germany, Belgium or Croatia? 
Define as follows a function that returns the name of the country for which the average age of its players  is the least -
```python
def least_avg_age(countries):
```
where countries is a parameter that contains the list of countries. Use this function to find out the answer to the above question.

---

###### Define a function "player_count" with a parameter (country) which can be used to count the number of players belonging to that country. This function will be useful for many questions that follow.
#### Question 9

Find the total number of players belonging to "Portugal" using the above function.

#### Question 10 

Which country has the maximum players participating in FIFA18 and how many? The "player_count" function can be useful here. Output the answer in the form of (country, count_of_players)
Hint: You will first need the list of countries participating in FIFA18.

#### Question 11

Define a function named age_limit taking a parameter (country) and return a list of players whose age is in the range of 16 through 20 (inclusive). 
Get this list of players for "United States"

---

###### Define a function called "compare_clubs" that takes three input parameters(club1, club2, compare_on_col) and returns the name of the club with the greater average value for the column compare_on_col. For example, if you want to know which club has higher average age, the compare_on_col would be 2 for this function since age is at index 2 in the list of columns.

#### Question 12

Which club pays the higher average wage to its players? "Real Madrid CF" or "FC Barcelona". Use the "compare_clubs" function with the compare_on_col having  the column number of wages attribute.

#### Question 13

Which club has higher average score of players? "Manchester City" or "Chelsea"?  Use the "compare_clubs" function for the performance rating (score_of_100) column.

---
#### Question 14

Output a list of dictionaries where each dictionary contains data of a single player from our 'PlayerData' list. Do this for the first 10 players from the PlayerData list.
The list with the first dictionary should look something like below-
```
[{'name': 'Cristiano Ronaldo',
'club': 'Real Madrid CF',
'nationality': 'Portugal',
'networth': 95500000.0},
]
```
---

###### Make a function named 'get_unique_element_list' with an input parameter column_name. This should return a list having only distinct elements from this column which means you need to eliminate the duplicates. You can use the get_column function you defined earlier to get the list of elements of a particular column and then create a new list with only distinct elements.

#### Question 15

Output a list of all unique leagues using the get_unique_element_list function.

#### Question 16

Which clubs pay an average wage above 100,000 euros  per week to their players? Return a list of clubs that match the criteria.
Hint: You can first use the get_unique_element_list function to get the participating clubs.

#### Question 17

Output a dictionary containing count of unique nationalities and number of clubs in the dataset. The dictionary should be of the form {'nationalities': < number of nations>, 'clubs': < number of clubs>}. 

#### Question 18

Which clubs have played in "German Bundesliga" league? Return a list matching the criteria.

#### Question 19

Define a function that takes a parameter (club) and returns a list of players with best performance ratings (score_of_100) in that club.


#### Question 20

A particular club decided to cut down each of their player's yearly wage by 2%. What is the net gross saving in euros of the club in that year? 
Hint: 52 weeks in a year

 
