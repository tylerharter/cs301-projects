# Project 9

In this assignment we are going to learn

* How Read Multiple CSV/JSON files
* How to Write JSON files
* How to use try/except

Download the zip file from the link below, and unarchive it. You should be able to do this just by double clicking on it once downloaded, and it will create a new folder containing everything you need for this assignment. Please do all your coding within this folder. 

* [cs301_p9.zip](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p9/cs301_p9.zip)

# Task
Your Boss, music prodigy turned data analyst extraordinaire, Nick Jonas, has asked you to create a program that takes in a bunch of tweet data, and to combine it into one single file for analysis.

He has reached out to his sourcing agency to obtain a whole bunch of tweets to help him analyze what caused his music career to come to a screeching halt, and they've sent back a couple of sample files so that we can start writing out data cleaning pipelines. 

In this first pass, we will work **only** with the files in the folder "sample_data". 

# Pass 1

## 1. `get_list_of_files` function

> input(s) to this function:
> * data_dir : a string representation of the directory to be searched

This function will be taking in a directory as a parameter, and returning a list of files that were located in that directory.

The list of files needs to be **sorted in ascending alphabetical order**. You don't have to worry about how python's sort treats numbers and so forth, just sort() the list and you should be okay, as long as it's contents are accurate. 

> The `os.listdir` function will be helpful in achieving this task    
> for more information on os.listdir
> * [os.listdir official documentation](https://docs.python.org/2/library/os.html)
> * [Tyler's Slides](https://tyler.caraza-harter.com/cs301/fall18/materials/lec-25.pdf)

The files should have the path as well as the file name.  For example If I had the file `test.csv` and the file was located in the `sample` directory your result should look like : 

> *If you're using linux/Mac : *
> sample/test.csv

> *If you're using Windows : * 
> sample\\test.csv

In order to achieve this, you need to use the os.path.join() function. **Please do not hardcode "/" or "\\"** because doing so will cause your function to fail on a computer that's not using the same operating system as yours.

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py get_list_of_files sample_data
```

an example of output on a windows machine

```
[
  "sample_data\\1.csv",
  "sample_data\\1.json",
  "sample_data\\2.csv",
  "sample_data\\2.json"
]
```

*If everything until here is correct, your score from test.py should be `10%`.*

## 2: Reading Files

The next three functions will focus on reading in the different types of files, and combining them together into a single data structure.  Some of these will look similar to past functions we've designed in this course.

### 2.1 `read_json_file` function

> input(s) to this function:
> * filepath : a string representation of the **full path** to a json file

This function will be taking in a filepath and returning a list of dictionaries that correspond to the tweet data that was in the .json file.

Take note here that the key of the dictionaries in the original JSON files is the tweet_id, which becomes a new field in the output JSON (see example below). 

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py read_json_file sample_data/1.json
```

an example of output from this call
```
[
  {
    "date": "Mon Apr 06 22:19:45 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": true,
    "num_liked": 4448,
    "tweet_id": "1467810369"
  },
  {
    "date": "Mon Apr 06 22:19:49 PDT 2009",
    "username": "USERID_3",
    "tweet_text": "is upset that he can't update his Facebook by texting it... and might cry as a result  School today also. Blah!",
    "is_retweet": false,
    "num_liked": 4304,
    "tweet_id": "1467810672"
  },
  {
    "date": "Mon Apr 06 22:19:53 PDT 2009",
    "username": "USERID_8",
    "tweet_text": "@Kenichan I dived many times for the ball. Managed to save 50%  The rest go out of bounds",
    "is_retweet": false,
    "num_liked": 8420,
    "tweet_id": "1467810917"
  },
  {
    "date": "Mon Apr 06 22:19:57 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "my whole body feels itchy and like its on fire ",
    "is_retweet": false,
    "num_liked": 9573,
    "tweet_id": "1467811184"
  },
  {
    "date": "Mon Apr 06 22:19:57 PDT 2009",
    "username": "USERID_9",
    "tweet_text": "@nationwideclass no, it's not behaving at all. i'm mad. why am i here? because I can't see you all over there. ",
    "is_retweet": false,
    "num_liked": 1851,
    "tweet_id": "1467811193"
  }
]
```
*If everything until here is correct, your score from test.py should be `20%`.*

### 2.2 `read_csv_file` function

> input(s) to this function:
> * filepath : a string representation of the **full path** to a CSV file

This function will be taking in a file_name and returning a list of dictionaries that correspond to the tweet data that was in the .csv file.

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py read_csv_file sample_data/1.csv
```
an example of output for this code
```
[
  {
    "tweet_id": "1467811372",
    "date": "Mon Apr 06 22:20:00 PDT 2009",
    "username": "USERID_3",
    "num_liked": "699",
    "tweet_text": "@Kwesidei not the whole crew ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811592",
    "date": "Mon Apr 06 22:20:03 PDT 2009",
    "username": "USERID_6",
    "num_liked": "9526",
    "tweet_text": "Need a hug ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811594",
    "date": "Mon Apr 06 22:20:03 PDT 2009",
    "username": "USERID_7",
    "num_liked": "4816",
    "tweet_text": "@LOLTrish hey  long time no see! Yes.. Rains a bit ,only a bit  LOL , I'm fine thanks , how's you ?",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811795",
    "date": "Mon Apr 06 22:20:05 PDT 2009",
    "username": "USERID_4",
    "num_liked": "5782",
    "tweet_text": "@Tatiana_K nope they didn't have it ",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467812025",
    "date": "Mon Apr 06 22:20:09 PDT 2009",
    "username": "USERID_3",
    "num_liked": "2010",
    "tweet_text": "@twittera que me muera ? ",
    "is_retweet": "False"
  }
]
```
*If everything until here is correct, your score from test.py should be `25%`.*

### 2.3 `read_all` function

> input(s) to this function:
> * data_dir : a string representation of the directory to be searched.

This step of the assignment will require you calling your past functions in order to combine all the different files into one single data structure.  This means that you will start with the directory name, and using this you will:

* get the list of files that are located in the directory
* read the data that is in the .csv or .json using the appropriate functions
* combine the lists of data into one single list

At the end of this function you should have one single list that contains all the data that was in the separate files.

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py read_all sample_data
```

example of this code being run

```
[
  {
    "tweet_id": "1467811372",
    "date": "Mon Apr 06 22:20:00 PDT 2009",
    "username": "USERID_3",
    "num_liked": "699",
    "tweet_text": "@Kwesidei not the whole crew ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811592",
    "date": "Mon Apr 06 22:20:03 PDT 2009",
    "username": "USERID_6",
    "num_liked": "9526",
    "tweet_text": "Need a hug ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811594",
    "date": "Mon Apr 06 22:20:03 PDT 2009",
    "username": "USERID_7",
    "num_liked": "4816",
    "tweet_text": "@LOLTrish hey  long time no see! Yes.. Rains a bit ,only a bit  LOL , I'm fine thanks , how's you ?",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811795",
    "date": "Mon Apr 06 22:20:05 PDT 2009",
    "username": "USERID_4",
    "num_liked": "5782",
    "tweet_text": "@Tatiana_K nope they didn't have it ",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467812025",
    "date": "Mon Apr 06 22:20:09 PDT 2009",
    "username": "USERID_3",
    "num_liked": "2010",
    "tweet_text": "@twittera que me muera ? ",
    "is_retweet": "False"
  },
  {
    "date": "Mon Apr 06 22:19:45 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": true,
    "num_liked": 4448,
    "tweet_id": "1467810369"
  },
  {
    "date": "Mon Apr 06 22:19:49 PDT 2009",
    "username": "USERID_3",
    "tweet_text": "is upset that he can't update his Facebook by texting it... and might cry as a result  School today also. Blah!",
    "is_retweet": false,
    "num_liked": 4304,
    "tweet_id": "1467810672"
  },
  {
    "date": "Mon Apr 06 22:19:53 PDT 2009",
    "username": "USERID_8",
    "tweet_text": "@Kenichan I dived many times for the ball. Managed to save 50%  The rest go out of bounds",
    "is_retweet": false,
    "num_liked": 8420,
    "tweet_id": "1467810917"
  },
  {
    "date": "Mon Apr 06 22:19:57 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "my whole body feels itchy and like its on fire ",
    "is_retweet": false,
    "num_liked": 9573,
    "tweet_id": "1467811184"
  },
  {
    "date": "Mon Apr 06 22:19:57 PDT 2009",
    "username": "USERID_9",
    "tweet_text": "@nationwideclass no, it's not behaving at all. i'm mad. why am i here? because I can't see you all over there. ",
    "is_retweet": false,
    "num_liked": 1851,
    "tweet_id": "1467811193"
  },
  {
    "tweet_id": "1467812799",
    "date": "Mon Apr 06 22:20:20 PDT 2009",
    "username": "USERID_4",
    "num_liked": "53",
    "tweet_text": "@iamjazzyfizzle I wish I got to watch it with you!! I miss you and @iamlilnicki  how was the premiere?!",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467812964",
    "date": "Mon Apr 06 22:20:22 PDT 2009",
    "username": "USERID_6",
    "num_liked": "7696",
    "tweet_text": "Hollis' death scene will hurt me severely to watch on film  wry is directors cut not out now?",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467813137",
    "date": "Mon Apr 06 22:20:25 PDT 2009",
    "username": "USERID_9",
    "num_liked": "8804",
    "tweet_text": "about to file taxes ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467813579",
    "date": "Mon Apr 06 22:20:31 PDT 2009",
    "username": "USERID_5",
    "num_liked": "5619",
    "tweet_text": "@LettyA ahh ive always wanted to see rent  love the soundtrack!!",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467813782",
    "date": "Mon Apr 06 22:20:34 PDT 2009",
    "username": "USERID_5",
    "num_liked": "1824",
    "tweet_text": "@FakerPattyPattz Oh dear. Were you drinking out of the forgotten table drinks? ",
    "is_retweet": "False"
  },
  {
    "date": "Mon Apr 06 22:20:16 PDT 2009",
    "username": "USERID_2",
    "tweet_text": "spring break in plain city... it's snowing ",
    "is_retweet": true,
    "num_liked": 9215,
    "tweet_id": "1467812416"
  },
  {
    "date": "Mon Apr 06 22:20:17 PDT 2009",
    "username": "USERID_9",
    "tweet_text": "I just re-pierced my ears ",
    "is_retweet": true,
    "num_liked": 9393,
    "tweet_id": "1467812579"
  },
  {
    "date": "Mon Apr 06 22:20:19 PDT 2009",
    "username": "USERID_9",
    "tweet_text": "@caregiving I couldn't bear to watch it.  And I thought the UA loss was embarrassing . . . . .",
    "is_retweet": false,
    "num_liked": 7345,
    "tweet_id": "1467812723"
  },
  {
    "date": "Mon Apr 06 22:20:19 PDT 2009",
    "username": "USERID_3",
    "tweet_text": "@octolinz16 It it counts, idk why I did either. you never talk to me anymore ",
    "is_retweet": true,
    "num_liked": 1879,
    "tweet_id": "1467812771"
  },
  {
    "date": "Mon Apr 06 22:20:20 PDT 2009",
    "username": "USERID_9",
    "tweet_text": "@smarrison i would've been the first, but i didn't have a gun.    not really though, zac snyder's just a doucheclown.",
    "is_retweet": true,
    "num_liked": 6476,
    "tweet_id": "1467812784"
  }
]
```

*If everything until here is correct, your score from test.py should be `40%`.*

## 3 `read_and_clean_all` function

> input(s) to this function:
> * data_dir : a string representation of the directory to be searched.

This function will be calling the `clean_dict` function that we have provided in order to format the data properly.    

The `clean_dict` function takes in a dictionary, and returns a dictionary that has been reformatted.

<INSERT EXAMPLE HERE for CLEAN_DICT OUTPUT> 

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py read_and_clean_all sample_data
```

example of output from this function
 ```
 [
  {
    "tweet_id": "1467811372",
    "date": "04-06-2009",
    "username": "USERID_3",
    "num_liked": 699,
    "tweet_text": "@Kwesidei not the whole crew ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811592",
    "date": "04-06-2009",
    "username": "USERID_6",
    "num_liked": 9526,
    "tweet_text": "Need a hug ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811594",
    "date": "04-06-2009",
    "username": "USERID_7",
    "num_liked": 4816,
    "tweet_text": "@LOLTrish hey  long time no see! Yes.. Rains a bit ,only a bit  LOL , I'm fine thanks , how's you ?",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467811795",
    "date": "04-06-2009",
    "username": "USERID_4",
    "num_liked": 5782,
    "tweet_text": "@Tatiana_K nope they didn't have it ",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467812025",
    "date": "04-06-2009",
    "username": "USERID_3",
    "num_liked": 2010,
    "tweet_text": "@twittera que me muera ? ",
    "is_retweet": "False"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": true,
    "num_liked": 4448,
    "tweet_id": "1467810369"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_3",
    "tweet_text": "is upset that he can't update his Facebook by texting it... and might cry as a result  School today also. Blah!",
    "is_retweet": false,
    "num_liked": 4304,
    "tweet_id": "1467810672"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_8",
    "tweet_text": "@Kenichan I dived many times for the ball. Managed to save 50%  The rest go out of bounds",
    "is_retweet": false,
    "num_liked": 8420,
    "tweet_id": "1467810917"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_4",
    "tweet_text": "my whole body feels itchy and like its on fire ",
    "is_retweet": false,
    "num_liked": 9573,
    "tweet_id": "1467811184"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_9",
    "tweet_text": "@nationwideclass no, it's not behaving at all. i'm mad. why am i here? because I can't see you all over there. ",
    "is_retweet": false,
    "num_liked": 1851,
    "tweet_id": "1467811193"
  },
  {
    "tweet_id": "1467812799",
    "date": "04-06-2009",
    "username": "USERID_4",
    "num_liked": 53,
    "tweet_text": "@iamjazzyfizzle I wish I got to watch it with you!! I miss you and @iamlilnicki  how was the premiere?!",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467812964",
    "date": "04-06-2009",
    "username": "USERID_6",
    "num_liked": 7696,
    "tweet_text": "Hollis' death scene will hurt me severely to watch on film  wry is directors cut not out now?",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467813137",
    "date": "04-06-2009",
    "username": "USERID_9",
    "num_liked": 8804,
    "tweet_text": "about to file taxes ",
    "is_retweet": "False"
  },
  {
    "tweet_id": "1467813579",
    "date": "04-06-2009",
    "username": "USERID_5",
    "num_liked": 5619,
    "tweet_text": "@LettyA ahh ive always wanted to see rent  love the soundtrack!!",
    "is_retweet": "True"
  },
  {
    "tweet_id": "1467813782",
    "date": "04-06-2009",
    "username": "USERID_5",
    "num_liked": 1824,
    "tweet_text": "@FakerPattyPattz Oh dear. Were you drinking out of the forgotten table drinks? ",
    "is_retweet": "False"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_2",
    "tweet_text": "spring break in plain city... it's snowing ",
    "is_retweet": true,
    "num_liked": 9215,
    "tweet_id": "1467812416"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_9",
    "tweet_text": "I just re-pierced my ears ",
    "is_retweet": true,
    "num_liked": 9393,
    "tweet_id": "1467812579"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_9",
    "tweet_text": "@caregiving I couldn't bear to watch it.  And I thought the UA loss was embarrassing . . . . .",
    "is_retweet": false,
    "num_liked": 7345,
    "tweet_id": "1467812723"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_3",
    "tweet_text": "@octolinz16 It it counts, idk why I did either. you never talk to me anymore ",
    "is_retweet": true,
    "num_liked": 1879,
    "tweet_id": "1467812771"
  },
  {
    "date": "04-06-2009",
    "username": "USERID_9",
    "tweet_text": "@smarrison i would've been the first, but i didn't have a gun.    not really though, zac snyder's just a doucheclown.",
    "is_retweet": true,
    "num_liked": 6476,
    "tweet_id": "1467812784"
  }
]
 ```
*If everything until here is correct, your score from test.py should be `50%`.*

## 4 `write_json` function

> input(s) to this function:
> * data_dir : a string representation of the directory to be searched.
> * output_filename : the name of the file to be written to

This function calls the read_and_clean_all() function on the data_dir given to it, **sorts the resulting list of dictionaries based on the username in ascending order** and then writes the resulting list of dictionaries as a **JSON File** to the filename specified by the "output_filename" parameter. We've provided the sort_list_of_dicts() function from P7 to help you do this. 

You should be able to test out this specific function by typing in the following at the command line : 

```(bash)
python main.py write_json sample_data out.json
```

This will not output anything. You should however have a new file called out.json, which you can open up to look at the contents of. 

*If everything until here is correct, your score from test.py should be `70%`.*


# Pass 2

After your program was finished your Boss, Nick Jonas, was quite excited to finally know why he is unable to find work as a musician.  However the data that was given by his sourcing agent caused your code to crash in multiple different locations.  Upon taking a closer look at the data, it is clear why this occurred.  The sample dataset that was given to you had already been cleaned, and so it worked nicely with your code.  However the real dataset has inconsistencies that cause crashes within your code.  We will now return to your previous functions and modify them to work better with a more realistic dataset.  The final `30%` of this assignment will be focused on error handling, and debugging in order to fit a more robust dataset. 


## 5 Exception handling

In order to create code that will better handle bad data, we will be using exception handling strategies, so that our 
code will still run even when introduced to bad data. 


### 5.1 `get_list_of_files`

The problem with this function is that there are files other than .json and .csv in this directory, modify your code so that it only returns the files that end in .csv or .json.  If a file is not a .csv or .json you should ignore it in this function.

*If everything until here is correct, your score from test.py should be `75%`.*

### 5.2 `read_json_file`

The problem with this function is that there are some .json files that have been corrupted.  Instead of crashing, use try and except blocks in your code to ignore files that have been corrupted.  When a file is corrupted, read_json should instead return an empty list instead of crashing.

*If everything until here is correct, your score from test.py should be `80%`.*

### 5.3 `read_csv_file`

the problem with this function is that some of the .csv files do not have the appropriate number of columns.  Instead of crashing your code should skip rows in the .csv that do not have the appropriate number of elements.

Take note that if you've used DictReader from the csv module to accomplish this task, DictReader replaces values it can't find with None, so you'd still end up with the right number of elements, one of them would just be a None. 

*If everything until here is correct, your score from test.py should be `90%`.*

### 5.4 `read_and_clean_all`

the problem with this function is that some of the data is not in the correct format in order to be converted.  If this occurs you should ignore the row (it should not be included in your parsed dictionary) and your function should continue running.

*If everything until here is correct, your score from test.py should be `100%`.*

Hurray, now your program works and Nick Jonas can analyze the tweet data.  We don't quite understand how tweet data will relate to a dying music career but we're sure Nick Jonas will find a way.
