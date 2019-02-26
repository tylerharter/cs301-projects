# Project 7: Soccer


Let's Play Fifa18 Python style! In this project, you will learn more ways of using lists and also get an introduction to using dictionaries. We will define functions, use loops and conditionals to perform data operations like sorting and basic statistical analysis. You will write the functions for this project in a jupyter notebook. If you're answering a particular question in a cell in your notebook, you need to put a comment in the cell so we know the question for which you're
answering. For example, if you're answering question 13, the first line of your cell should contain #q13.


To start, download the files given below into your project directory and understand the dataset provided to you.
* [README.md](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/README.md)
* [project.py](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/project.py)
* [Fifa18.csv](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/Fifa18.csv)
* [test.py](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p7/test.py)

## Opening the file 
You can see the contents of the Fifa18.csv file by clicking on the file from jupyter notebook home. If you want to open it using excel, some extra steps might be required depending on your excel settings since this file is utf-8 encoded.
If the file contents have unwanted characters (especially in windows OS), please follow the following steps. 
* Open Microsoft Excel.
* Click on the Data menu bar option.
* Click on the From Text icon.
* Navigate to the location of the file that you want to import. Click on the filename and then click on the Import button. The Text Import Wizard - Step 1 or 3 window will now appear on the screen.
* Choose the file type that best describes your data - Delimited or Fixed Width.
* Choose 65001: Unicode (UTF-8) from the drop-down list that appears next to File origin.
* Click on the Next button to display the Text Import Wizard - Step 2 or 3 window.
* Place a checkmark next to the delimiter that was used in the file you wish to import into Microsoft Excel 2007. The Data preview window will show you how your data will appear based on the delimiter that you chose. In our case, check "comma".
* Click on the Next button to display the Text Import Wizard - Step 3 of 3.
* Choose the appropriate data format for each column of data that you want to import. In our case, keep it "General".
* Click on the Finish button to finish importing your data into Microsoft Excel.

Similar procedure is needed for MacOS.

## Data introduction

Try to familarize yourself with the data before starting the analysis. We have players belonging to a wide range of nationalities and clubs in Fifa18. As you can see the numeric data includes their weekly wages (in euros) (Yes! wages per week.), networth of the player(in euros) and the performace rating(score out of 100). For instance, a player named "Neymar" belongs to Brazil and is signed up by club "Paris Saint-Germain" paying him a weekly wage of "280000 euros" and has a huge
networth.

We have provided you with a project.py file that will read the FIFA csv file and convert the data into a list of lists. Import the project file and type the following snippet to see the type of some of the numeric columns example wages, networth is float. Also check the number of rows and columns. 

```sh
import project
PlayerData = project.PlayerData
print(type(PlayerData[1][6]))  #this should return you float
print(len(PlayerData)) # this prints the number of rows
print(len(PlayerData[0])) #this is the number of columns in the data
```
Remember that the first row in your list contains the column headings for the columns. Print the headings to see for yourself and verify with the csv file.

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

Get the name and club of the highest networth player in the list using a function. Return the values in the form of (name, club) from this function.

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

Output the average of the networth of all the players in this roster.

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

 
