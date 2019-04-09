# DRAFT (don't start this stage yet)

# Stage 2

We'll now use the clean data from stage 1 to analyze the tweets of a
few users.  We'll also write some code to recursively find and process
JSON nested inside multiple directories.  To start, do the following:

1. download and extract `recursive.zip` in the same location of your notebook (you need to have the `recursive` directory in the same directory as your `main.ipynb`)
2. re-download `test.py` to get all 40 tests

Through question 32, everything is about the data in `full_data`.  Use
your code from last time to answer the questions (this means you'll
ignore corrupt data, as in stage 1).

#### Question 21: How many tweets are present in total?

#### Question 22: Which usernames appear in the dateset?

Answer in the form of a `set`.

#### Question 23: How **prolific** is each user?

Answer with a `dict` that maps username to the number of tweets by that user.

#### Question 24: How **popular** is each user?

Answer with a `dict` that maps username to the average number of likes that user gets per tweet.

#### Question 25: How **verbose** is each user?

Answer with a `dict` that maps username to the average number of characters per tweet by that user.

#### Question 26: What is the relationship between number of tweets and length of tweets?

Answer with a scatter plot showing 10 points (one per user).  The
x-axis represents number of tweets, and the y-axis represents average
length.  It should look like this:

<img src="q26.png" width="400">

#### Question 27: What is the relationship between number of tweets and likes?

Answer with a scatter plot showing 10 points (one per user).  The
x-axis represents number of tweets, and the y-axis represents average
likes.  It should look like this:

<img src="q27.png" width="400">

#### Question 28: What is the relationship between length and likes?

Answer with a scatter plot showing 10 points (one per user).  The
x-axis represents average length, and the y-axis represents average
likes.  It should look like this:

<img src="q29.png" width="400">

#### Question 29: What is the username of the user represented by the outlier in the last two plots?

#### Question 30: What are the tweets made by that outlier user?

Answer with a list of Tweet objects, sorted by `num_liked` descending.

#### Question 31: What percent of the outlier user's total likes (across all tweets) come from the most-liked tweet?

#### Question 32: If we exclude that most-liked tweet, what is that user's like-per-tweet average?

----

TODO

----

