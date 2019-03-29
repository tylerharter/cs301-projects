# Stage 1

# Introduction

In this assignment, we're going to deal with three common problems you will encounter when dealing with almost any data science problem.

* Working with multiple files
* Working with multiple file formats
* Working with broken files

Download the zip file below to get started, and unzip it to a folder. If you are unsure how to unzip a file, please check the following links : 

* Mac OS - http://osxdaily.com/2017/11/05/how-open-zip-file-mac/
* Windows - https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files
* Ubuntu - https://www.hostingadvice.com/how-to/unzip-file-linuxubuntu/

[INSERT ZIP FILE LINK]


# File vs Filename vs Path?

Before we get started with the assignment, let's talk about the distinction between these three terms, which will become important as we go along.

**File** 

(source : https://www.lifewire.com/what-is-a-file-2625878)

*A file, in the computer world, is a self-contained piece of information available to the operating system and any number of individual programs. A computer file can be thought of much like a traditional file that one would find in an office's file cabinet. Just like an office file, information in a computer file could consist of basically anything.*

In Python, we have many different ways of interacting with files, some which you have already used, such as the **open** function. 

**Filename** 

A filename, as you might guess, refers to the name given to a file. In Python, a filename is nothing more than a regular string. People often use the terms file and filename interchangably, because the way we refer to files is through their filename.

**Path**

A path is basically the location of a file on your computer. The path to a file depends on where you saved it on your computer. Windows and Mac paths look different, but they basically have a structure that looks like this : 

*directory1/directory2/file1*

The path above tells you that file1 is stored in directory1, which in turn, is present inside directory2. Therefore the "path" for the file `file1` is `directory1/directory2/file1`

Quick note about paths : On Windows, paths use "\\" whereas on Mac and Linux, they use "/".

In Python, a path too, is saved as a regular string. 

#### Question 1 : What are the files present in the 'sample_data' directory?

HINT : Look into the `os.listdir` function. Return a list of filenames, sorted in **reverse-alphabetical** order.

#### Question 2 : What are the paths of all the files in the 'sample_data' directory?

Build on what you wrote for question 1, but you must now get the path instead of just the filename.

In order to achieve this, you need to use the `os.path.join()` function. Please do not hardcode "/" or "\\" because doing so will cause your function to fail on a computer that's not using the same operating system as yours. Again, return a list sorted in **reverse-alphabetical** order. 

#### Question 3 : What are the paths of all the files in the 'full_data' directory?

#### Question 4 : What are the paths of the CSV and JSON files present in the "sample_data" directory?

Again, building on your code for Question 2, now write a function that filters out all files except CSV and JSON files. A CSV or JSON file is simply one that ends with ".csv" or ".json" respectively. 

To clarify, this function must do everything you did for Question 2, as well as the additional step above. 

#### Question 5 : What are the paths of the CSV and JSON files present in the "full_data" directory?

#### Question 6 : What are the tweets present in the CSV file "sample_data/1.csv"?

Now, we will look into parsing a CSV file. 

Whenever you're working with different types of files (which we will be, there's some JSON files coming up soon) it's good to have a common data format to be able to put everything into. 

What we're going to use is a namedtuple, with the following specifications : 

**Name** : Tweet        
**Fields** : 
* tweet_id
* username
* num_liked

Please ensure you define your namedtuple exactly according to the specifications above, or you will be unable to pass the tests. 

Your goal for this question is to parse the CSV file, and construct a **list of namedtuples**, where each row of the CSV file corresponds to one namedtuple in the list. 

For example, here's what the first (non-header) row of the "sample_data/1.csv" file looks like : 

`1467811372,Mon Apr 06 22:20:00 PDT 2009,USERID_6,5882,@Kwesidei not the whole crew ,True`

The corresponding namedtuple, should look like this : 

`Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882)`

Notice that we're not using all the fields in the row, just tweet_id, username, and num_liked. Also note that num_liked is being saved as a number, not a string.

#### Question 7 : What are the tweets present in the CSV file "sample_data/2.csv"?

#### Question 8 : What are the tweets present in the CSV file "full_data/1.csv"?

#### Question 9 : What are the tweets present in the CSV file "full_data/2.csv"?

If you just tried to run your code as-is on this file, chances are it crashed, or you had some missing data (If not, great!). This is because some of the rows in this file, are incomplete or inconsistent in some way. You must now go back and modify your CSV parsing function to deal with situations like this. 

Essentially, whenever you see a row in the CSV file which does not have all the fields present, just skip that row and move on to the next one, parsing it as normal. 

#### Question 10 : What are the tweets present in the JSON file "sample_data/1.json"?

Just like before with the CSV files, we're going to now parse a JSON file and convert it to a list of namedtuples, so that all of our data from different files is going into one common format that's easy for us to work with. 

The JSON files we have have the data saved as one big dictionary, with the keys in the dictionary being the tweet_id, and the values being a smaller dictionary, containing all the details of the tweet with that tweet_id. Feel free to open up a JSON file and take a look at it to get a sense of how it's structured (this is always a great first step when you're trying to parse data you're unfamiliar with, just take some time to look at it and understand it's structure).

Your task here is to convert each JSON file to a **list of namedtuples** with the exact same format for the namedtuple as before (remember, we're trying to get to a common data format we can work with). Each key-value pair in our big dictionary therefore corresponds to one namedtuple in the list. 

Here's the first tweet in the JSON file, "sample_data/1.json" 

```json
{
  "1467810369": {
    "date": "Mon Apr 06 22:19:45 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": false,
    "num_liked": 315
},
```

And here's the corresponding namedtuple :

`Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315)`

Remember, you need to return a **list of namedtuples**.

#### Question 11 : What are the tweets present in the JSON file "sample_data/2.json"?

#### Question 12 : What are the tweets present in the JSON file "full_data/5.json"?

#### Question 13 : What are the tweets present in the JSON file "full_data/1.json"?

Once again, we have some JSON files that are broken, such as this one. Unfortunately, unlike CSV files, broken JSON files are much more complicated to fix so we can't just skip over one tweet and salvage the rest, so let's just skip the entire file and **return an empty list** if we find that it is broken. The goal here is to get your code to not crash. We're dealing with tweets here, and there's billions of them for us to analyze, so losing one file is not a big deal. Your code crashing however, is a big deal. 

#### Question 14 : Which file in the directory 'sample_data' contains the tweet with tweet_id '1467912100'?

Return the **path to the file**. If you can't find this tweet_id in any of the files in this folder, return `False`.

Hint : Use the functions you've written to help you accomplish this task, as it involves a combination of looking through all the files in a folder, parsing them, and then looking through the parsed list. 

#### Question 15 : Which file in the directory 'full_data' contains the tweet with tweet_id '1467862937'?

#### Question 16 : Which file in the directory 'full_data' contains the tweet with tweet_id '1467907751'?

#### Question 17 : Which files in the directory "sample_data" contain tweets by the user "USERID_1"?

Be sure to return a **list of paths** (even if it's just 1 path) sorted in **reverse-alphabetical order**.

#### Question 18 : What are the tweets present in all the files in the "sample_data" directory?

Return a single **list of namedtuples** containing all the tweets, sorted in **ascending order by tweet_id**.

Note that this step now gives you a way to read in multiple files present in a directory, of different formats, and end up with a single list of namedtuples, all in the same format. Let's use it to perform some data analysis that runs across all the files in a directory.

#### Question 19 : What are the tweets present in all the files in the "sample_data" directory, sorted by num_liked?

Return a single **list of namedtuples** containing all the tweets, sorted in **ascending order by num_liked**.

Consider extending your code in the last function to include a `sort_by` parameter.

#### Question 20 : What are the first 20 tweets present in all the files in the "full_data" directory, sorted by num_liked?

Return a single **list of namedtuples** of length 20 containing the first 20 tweets sorted in **ascending order by num_liked**.

Consider extending your code in the last function to include a `sort_by` parameter.

That's it for Stage 1. In the next stage, we'll begin using the data structures we've set up to do some analysis that spans across multiple files! 
