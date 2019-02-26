# Project 6

This project is a wine connoisseurs' delight! We will be exploring a
subset (the first 1500 rows) of the Kaggle
[wine reviews dataset](https://www.kaggle.com/zynicide/wine-reviews); you will be
using various string manipulation functions that come with Python as
well as rolling some of your own to solve the problems posed. Happy
coding, and remember the [Ballmer Peak](https://xkcd.com/323/) is nothing but a myth!

# Directions

Begin by downloading `wine.csv`, `test.py`, and `project.py`.  Create
a `main.ipynb` file to start answering the following questions, and
remember to run `test.py` often.  Use the `#qN` format as you have
previously.

## Q1: which country names are listed in the `country` column of the dataset?

Your output should be in the form of a Python list containing the
country names.  The tests don't care about the order, but there should
should be no duplicates.  Also, some country names are missing in the
dataset (real-life data is often messy, unfortunately!).  Missing
values are represented as `None`, but you should make sure `None` does
not appear in your answer list.

Now is a good time to run the tests with `python test.py`.  If you did Q1 correctly, it should look like this:

```
Summary:
  Test 1: PASS
  Test 2: not found
  Test 3: not found
  Test 4: not found
  Test 5: not found
  Test 6: not found
  Test 7: not found
  Test 8: not found
  Test 9: not found
  Test 10: not found
  Test 11: not found
  Test 12: not found
  Test 13: not found
  Test 14: not found
  Test 15: not found
  Test 16: not found
  Test 17: not found
  Test 18: not found
  Test 19: not found
  Test 20: not found

TOTAL SCORE: 5.00%
```

## Q2: what is the average wine price?

Be careful!  There may be missing price information for some rows, so
it's best to skip those.

## Q3: which wine varieties are produced by Spain?

Answer in the form of a list containing no duplicates.

TODO: Lets look at what varieties of wine are produced by individual countries by performing a filtering operation. 
Using the API provided, print varieties of wines produced by `Spain`. Ensure that there are no repeated entries in your
output. You can do this by writing a function to remove duplicates form your output. Writing ths function will help you in 
questions that follow.

## Q4:
For this question you are required to perform string search operation on wine description field. Use the API provided to
 get a list of wineries which make wines having the black-fruit aroma. You can use `black-fruit aroma` as search string 
 to search in the description field. Make sure your final list has no repeated entries!
 

## Q5 (8 points):

Search the dataset to identify and output the country that makes the costliest wine.

## Q6 (5 points):
Print wineries which make wines which have `blackberry aroma`. This time, however, print the names after removing all
spaces from the names. For example, if `Patricia Green Cellars` is one of the entries in your list, it should be converted to 
`PatriciaGreenCellars`. We recommend you write a dedicated function to do this as it will help you to answer the next question

## Q7 (7 points):
If you liked Professor Langdon's adventures in Da Vinci code you'll like this one:) Search the dataset and print 
Which wine varieties are anagrams of the phrase `antibus governance`? An anagram is a word or phrase formed by rearranging
the letters of a different word or phrase, typically using all the original letters exactly once. 
(Read more here : https://en.wikipedia.org/wiki/Anagram). For this question, you need to convert both the strings you are comparing
to lowercase, strip spaces from them and then check for them being anagrams. NOTE: RETAIN spaces when you print your final 
output!

## Q8 (3 points):
Following the same rules as above output wine varieties that are anagrams of the phrase `Banned Petrol Mill`.

## Q9 (5 points):
Which variety is the best rated wine made by `USA`?

## Q10 (5 points):
Which variety is the best rated wine made by `Spain`?

## Q11 (5 points):
Write a function that calculates average points per dollar for all wines made by a winery and then
print price per dollar of the Winery called `Heitz`. Assume all prices in dataset are in dollars.

## Q12 (5 points):
Print price per dollar of the Winery called `Ponzi`.

## Q13 (5 points):
Which winery in `USA` has the highest price per dollar?

## Q14 (5 points):
Which winery in `France` has the highest price per dollar?

## Q15 (2 points):
Which winery in `Italy` has the highest price per dollar?

## Q16 (5 points):
Given a winery X, design a function to find out `variety` of all the wines produced. Using this function output the 
`variety` of all wines produced by `Heitz`.

## Q17 (5 points):
Re-use the function above to find out the `variety` of all wines produced by `Silvan Ridge`.

## Q18 (5 points):
What is the range of wine `prices` listed in the dataset? You can define a function that calculates the range of a list to do this.
Note: A Range is defined as the difference between the maximum and minimum value of the list.
For example: `[2, 1, 4, 8, 2, 5, 9, 3]` has range `9 - 1 = 8`

## Q19 (5 points):
What is the range of wine `points` listed in the dataset?
Use the range function created above for prices to calculate the range for points in the dataset.

## Q20 (5 points):
This is a challenge question! It requires careful thought and structuring of your code.

For this question we try to find wineries which are in direct competition with each other. By direct competition we mean
the wineries which have the most number of wine varieties in common.
Output the winery name which is a direct competitor to `Grand Pacific` and also output its ppd ratio. You can output these
as a list with the winery name at index 0 and the ppd ratio at index 1.
