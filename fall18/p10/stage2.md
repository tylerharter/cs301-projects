# Stage 2: Database Queries

In this section, you're going to be further analyze the dataset.
Some of your answers can be answered by loading your data into a
SQLite database and sending queries to the database. The questions
11 - 15 should be answered by writing Python code and questions 
16 - 20 should be answered by using SQL queries.

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
great!  You can use it as long as (1) it works and (2) you cite
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

## Q14: what is the most central South American country?

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
 
## NOTE: The following questions need to be answered using SQL queries.
You should create a database table before you are able to answer the
following questions using SQL queries. For creating a table, you may use
the below code snippet. This code snippet creates and connects to a database
named *countries.db* and the `to_sql()` function creates a database table
named `countries_table` from the `countries` DataFrame
(note this name may be different in your code) that was created using the
*countries.json* file (in step 1).

```Python
import sqlite3
conn = sqlite3.connect('countries.db')
countries.to_sql("countries_table", conn, if_exists="replace", index=False)
```

## Q16: which countries in North America have a population less than 100000?
You should display the `country` name and `population` of the countries that match
the above criteria. The countries should be listed in the *ascending* order of population.

*Hint*: `pd.read_sql(query, conn)` executes a SQL query on the database connection
object conn and returns the result as a pandas DataFrame. You may use this function
to write and execute the SQL queries by replacing the `query` with the appropriate
SQL query.

## Q17: what are the top 3 countries in Europe that have the largest population?
You should display the `country` name and `population` of the top three countries
in Europe that have the largest population. These top three countries should be
displayed in *descending* order of population.

## Q18: what is the average population of every continent?
For this question, you should calculate the average population of every continent
and display the `continent` name and average population of the continent (using a 
column named `avg_pop`). The results should be displayed in *descending* order of the
column `avg_pop`.

*Hint*: You can rename a column using the `AS` keyword in SQL.

## Q19: what is the number of countries within each continent?
For this question, you should calculate the number of countries within every continent
and display the `continent` name and number of countries within that continent (using a 
column named `num_countries`). The results should be displayed in *ascending* order of the
column `num_countries`. If two continents have the same number of countries, then those
continents should be displayed in alphabetical order (e.g., if Australia and South America
have the same number of countries, then Australia should be displayed before South America).

## Q20: which continents have an average death-rate greater than 10?
For this question, you should calculate the average death-rate of every continent
and display the `continent` name and average death-rate of the continents (using a 
column named `avg_death_rate`) that have an average death rate greater than 10. 
The results should be displayed in *descending* order of the column `avg_death_rate`.

*Hint*: For filtering based on an aggregated column (e.g., avg_death_rate), you should
use `HAVING` instead of `WHERE`.