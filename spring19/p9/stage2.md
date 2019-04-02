# DRAFT (don't start this stage yet)

# Stage 2

We're going to pick up where we left off in Stage 1, and focus on analyzing the dataset. Even though it spans multiple files and different formats, the fact that we did all that work in Stage 1 to bring it all into a common format means a lot of the techniques you use to analyze this data will seem familiar to what you've done before.

Be sure to use your code from Stage 1 to start off your analysis from a list of namedtuples.

#### Question 21 : How many tweets are present in total, in the "full_data" directory? 

Of course, ignoring the ones that are broken rows in CSV files, or present in broken JSON files.

#### Question 22 : How many unique users' tweets do we have in the 'full_data' directory? 

#### Question 23 : What was the average number of likes received per tweet for tweets in the "full_data" directory? 

#### Question 24 : Which tweet has the highest number of likes ("num_liked") among all the tweets in the "full_data" directory? 

Return only the tweet_id.

#### Question 25 : What was user USERID_2's best tweet (tweet with the most likes) counting only the tweets in the full_data directory? 

Return the tweet_id.

#### Question 26 : Which user has tweeted the most times (counting only the tweets in the "full_data" directory)?

Return the count of the number of times they've tweeted.

#### Question 27 : Who has the second highest number of tweets (counting only the tweets in the "full_data" directory)? 
 
Again, return the count of the number of times they've tweeted. 

#### Question 28 : Which user has the highest average likes per tweet (counting only the tweets in the "full_data" directory)? 

#### Question 29 : Which user had the highest variability (highest likes - lowest likes) in the number of likes they received for their tweets? 

A quick note here : this idea of reading in files of multiple formats and converting them to one format to play with is a common and powerful idea that is used everywhere in data science. 

If at this stage, you wanted to incorporate a different kind fo file format (say you got a new batch of data that uses some other format), all you'd have to do is write some code to convert it to your standard format (a list of namedtuples) but your code to do the actual data analysis itself (questions 18 through 24) wouldn't have to change at all! 

This separation between the code used to read in data and prepare it (**data preprocessing**) and code used to do actual data analysis is a crucial part of data science. 

#### Question 30 : Which users have more total likes than user USERID_2? 

Return a list of usernames who's sum of likes across all their tweets exceeds the sum of likes that user USERID_2 has received across all their tweets. 

#### Question 31 : Which users have more total likes than user USERID_4? 

#### Question 32 : What are the paths to all the files in the "play" directory?

Let's take a break from data analysis and take a look at recursion. If you look through the "play" directory, you will notice that there are *nested folders*, i.e., folders within folders. Go ahead and try running your existing code from Question 2 on this folder. 

You will notice that it just lists out the first level, that is, files and folder present inside the play directory itself, but it does not go any deeper (i.e. down into each individual directory within the play directory). 

For instance, there is a file called "ppt.ppt" whose path is "play/rb/ppt.ppt" which is to say, it is located inside the "rb" directory, which in turn, is located inside the play directory. Your current code does not go into the "rb" directory and look for the files present there. 

Your goal for this task is to print out the paths to **all files present in the play directory and all it's nested directories**, using recursion.
