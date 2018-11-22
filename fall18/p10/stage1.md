# Stage 1: Web Scraping

In this question, you're going to write code to download the data
files, load the data to Pandas DataFrames, and then answer various
questions about the data.

The questions you must answer are below.  If a given cell is asking a
question number N, the cell should have a comment that looks like this:

```python
#q1
... code that computes the answer ...
```

For example, the cell that answers the first questions will contain a
comment that says `#q1`.



# Q1: what is the total population across all the countries in the dataset?

*Hint 1*: `pd.read_json(URL)` will return a DataFrame by downloading the
 JSON file from online at URL.  If the downloaded JSON contains a list
 of dictionaries, each dictionary will be a row in the DataFrame.

*Hint 2*: review how to extract a single column as a Series from a
 DataFrame.  You can add all the values in a Series with the `.sum()`
 method.

# Q2: what is the first URL in the https://tyler.caraza-harter.com/cs301/fall18/data/capitals.txt page?

*Hint*: use requests.get to download the capitals.txt, then split it into a list.

# Q3: what is the capital of China?

To get credit for this one, make sure you extract the data from the files referenced in capitals.txt.

*Hint 1*: construct a DataFrame where every row is from one of the
 files listed in capitals.txt.  This will be useful for answering
 other questions as well.

*Hint 2*: you can use fancy indexing to extract the row where the
 Country equals "China".  Then, extract the Capital Series, from which
 you can grab the only values with
 [Series.item()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.item.html)
 function.


https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html
