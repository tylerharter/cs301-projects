# Stage 2: Database Queries

In this section, you're going to be further analyzing the dataset.
Some of your answers can be answered by loading your data into a
SQLite database and sending queries to the database.  You need to
decide which questions to answer with SQL queries and which to answer
by writing Python code (some are not easily answerable with a query).

## Q11: what is the distance between the Randall Stadium and the State Capital?

This isn't related to countries, but it's a good warmup.  Your answer
should be about 1.433899492072933 miles.

Assumptions:
* the latitude/longitude of Randall Stadium is 43.070231,-89.411893
* the latitude/longitude of the Wisconsin Capital is 43.074645,-89.384113
* use the Haversine formula: [http://www.movable-type.co.uk/scripts/gis-faq-5.1.html](http://www.movable-type.co.uk/scripts/gis-faq-5.1.html)
* the radius of the earth is 3956 miles
* answer in miles

