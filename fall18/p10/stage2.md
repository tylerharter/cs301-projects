# Stage 2: Database Queries

In this section, you're going to be further analyzing the dataset.
Some of your answers can be answered by loading your data into a
SQLite database and sending queries to the database.  You need to
decide which questions to answer with SQL queries and which to answer
by writing Python code (some are not easily answerable with a query).

## Q11: what is the distance between Camp Randall Stadium and the Wisconsin State Capital?

This isn't related to countries, but it's a good warmup for the next
problems.  Your answer should be about 1.433899492072933 miles.

Assumptions:
* the latitude/longitude of Randall Stadium is 43.070231,-89.411893
* the latitude/longitude of the Wisconsin Capital is 43.074645,-89.384113
* use the Haversine formula: [http://www.movable-type.co.uk/scripts/gis-faq-5.1.html](http://www.movable-type.co.uk/scripts/gis-faq-5.1.html)
* the radius of the earth is 3956 miles
* answer in miles

If you find code online that computes the Haversine distance for you,
great!  You can use it as long as you (1) it works and (2) you cite
the source with a comment.

If you decide to implement it yourself (it's fun!), here are some tips:
* review the formula: [http://www.movable-type.co.uk/scripts/gis-faq-5.1.html](http://www.movable-type.co.uk/scripts/gis-faq-5.1.html)
* remember that latitude and longitude are in degrees, but sin, cos, and other Python math functions usually expect radians.  Consider [math.radians](https://docs.python.org/3/library/math.html#math.radians)
* people often use x^N to mean x raised to the Nth power.  Make sure you write it as x**N in Python.

## Q12: what is the distance between India and Brazil?

For the coordinates of a country, use its capital.

*Hint 1*: if your DataFrame of capitals is called `capitals`, what do
 you get from `capitals.set_index('country')`?

*Hint 2*: what do you get when you evaluate `capitals.set_index('country').loc['France']`?

## Q13: what is the distance between every pair of South American countries?

Your result should be a table with 12 rows (for each country) and 12
columns (again for each country).  The value in each cell should be
the distance between the country of the row and the country of the
column.  For a general idea of what this should look like, open the
expected.html file you downloaded.  When displaying the distance
between a country and itself, the table should should NaN (instead of
0).

## Q14: what is the most central South America country?

This is the country that has the shortest average distance to other
South American countries.

*Hint 1*: check out the following Pandas functions:
* [DataFrame.mean](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mean.html)
* [Series.sort_values](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.sort_values.html) (note this is not the same as the DataFrame.sort_values function you've used before)

*Hint 2*: a Pandas Series contains indexed values.  If you have a
 Series `s` and you want just the values, you can use `s.values`; if
 you want just the index, you can use `s.index`.  Both of these
 objects can readily be converted to lists.

## Q15: how close is each country in South America to it's nearest neighbour?

The answer should be in a table with countries as the index and two
columns: `nearest` will contain the name of the nearest country and
`distance` will contain the distance to that nearest country.

*Hint 1*: find a Series of numerical data you can experiment with
 (perhaps from one of the DataFrames you've been using for this
 project).  If your Series is named `s`, try running `s.min()`.
 Unsurprisingly, this returns the smallest value in the Series.  Now
 try running `s.idxmin()`.  What does it seem to be doing?

*Hint 2*: if you run `df.min()` on a DataFrame, Pandas applies that
 function to every column Series in the DataFrame.  The returned value
 is a Series.  The index of the returned Series contains the columns
 of the DataFrame, and the values of the returned Series contain the
 minimum values.  If you run `df.idxmin()` on a DataFrame, the
 returned values contain indexes from the DataFrame.
 