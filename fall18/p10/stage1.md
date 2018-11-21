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

# Question 1: what is the total population across all the countries in the dataset?

*Hint 1*: `pd.read_json(URL)` will return a DataFrame by downloading the
 JSON file from online at URL.  If the downloaded JSON contains a list
 of dictionaries, each dictionary will be a row in the DataFrame.

*Hint 2*: review how to extract a single column as a Series from a
 DataFrame.  You can add all the values in a Series with the `.sum()`
 method.