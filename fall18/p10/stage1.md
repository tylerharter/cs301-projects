# Stage 1: Web Scraping

In this stage, you're going to write code to download the data files,
load the data to Pandas DataFrames, and then answer various questions
about the data.

The questions you must answer are below.  If a given cell is answering
a question number N, the cell should have a comment that looks like
this:

```python
#qN
... code that computes the answer ...
```

For example, the cell that answers the first question should contain a
comment that says `#q1`.



## Q1: what is the total population across all the countries in the dataset?

*Hint 1*: `pd.read_json(URL)` will return a DataFrame by downloading the
 JSON file from online at URL.  If the downloaded JSON contains a list
 of dictionaries, each dictionary will be a row in the DataFrame.

*Hint 2*: review how to extract a single column as a Series from a
 DataFrame.  You can add all the values in a Series with the `.sum()`
 method.

## Q2: what is the first URL in the capitals.txt page?

You may hardcode this URL in your program:
https://tyler.caraza-harter.com/cs301/fall18/data/capitals.txt.  You
must, however, answer this question by programmatically extracting the
first line from capitals.txt.

*Hint*: use requests.get to download the
 [capitals.txt](https://tyler.caraza-harter.com/cs301/fall18/data/capitals.txt),
 then split it into a list.

## Q3: what is the capital of China?

To solve this problem (and subsequent problems), use `requests.get` to
download every file listed in capitals.txt and combine all the data in
a DataFrame.

*Hint 1*: construct a DataFrame where every row is from one of the
 files listed in capitals.txt.  This will be useful for answering
 other questions as well.  If `rows` is a list of dictionaries (each
 representing a row), you can easily construct a DataFrame with this
 snippet: `DataFrame(rows)`.

*Hint 2*: you can use fancy indexing to extract the row where the
 `Country` equals "China".  Then, extract the `Capital` Series, from
 which you can grab the only value with the
 [Series.item()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.item.html)
 function.

## Q4: which 5 countries have the southern-most capitals?

*Format*: produce your answer as a JSON-formatted list of five
 countries.  The list should be sorted so that the countries with
 capitals farther south are first.

*Hint 1*: look at the documentation examples of how to sort a
 DataFrame with the
 [sort_values](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html)
 function.

*Hint 2*: look at examples that used the
  [head](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.head.html)
  function.

## Q5: which 3 countries have the northern-most capitals?

*Format*: produce your answer as a JSON-formatted list of three
 countries.  The list should be sorted so that the countries with
 capitals farther north are first.

## Q6: for "birth-rate" and "death-rate", what are various summary statistics (e.g., mean, max, standard deviation, etc)?

*Format*: use the
 [describe](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html)
 function on a DataFrame that contains `birth-rate` and `death-rate`
 columns.  You may include summary statistics for other columns in
 your output, as long as your summary table has stats for birth and
 death.

## Q7: for "literacy" and "phone", what are various summary statistics (e.g., mean, max, standard deviation, etc)?

In [some
 countries](https://en.wikipedia.org/wiki/Decimal_separator#Arabic_numerals),
 it is standard to use commas instead of periods to indicate decimals.
 The `literacy` and `phone` data is formatted this way (i.e., decimal
 numbers represented as strings, with commas for decimals).  You'll
 need to reformat the data to use periods (instead of commas), then
 convert the column of strings to a column of floats.

*Hint*: learn how to use the
 [astype](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.astype.html)
 and
 [replace](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.replace.html)
 Pandas functions.

## Q8: what is the largest land-locked country in Europe?

A "land-locked" country is one that has zero coastline.  Largest is in terms of population.

## Q9: what is the largest land-locked country in Africa?

Same as Q8.

## Q10: what is the largest land-locked country in South America?

Same as Q8.