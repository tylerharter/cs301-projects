# Lab 6

In this lab, we'll practice accessing CSVs, learn about sorting,
organize data with sets, and practice processing command line
arguments.

To start, familiarize yourself with the dataset for P6 on GitHub here:
[wine.csv](https://github.com/tylerharter/cs301-projects/blob/master/spring19/p6/wine.csv).
Download the `wine.csv` to a new `lab6` directory, and start a new
notebook in that directory for this lab.

## CSV

[Chapter 14](https://automatetheboringstuff.com/chapter14/) of
Automate the Boring Stuff introduces CSV files and provides a code
snippet we can reuse.  We showed how to turn this code into a function
in class.  Copy the following into a cell in your notebook and run it:

```python
import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData

# use process_csv to pull out the header and data rows
csv_rows = process_csv("wine.csv")
csv_header = csv_rows[0]
csv_data = csv_rows[1:]
```

We recommend you also copy the above code into your P6 notebook when
you start the project.

Try running the following and thinking about the results:
* `csv_header`
* `len(csv_data)`
* `csv_data[:5]`
* `csv_data[0]`
* `csv_data[0][3]`
* `csv_header.index("variety")`
* `csv_data[0][csv_header.index("variety")]`

Note on last two: you can find the index of a value in a list by using the `.index(val)`
method.  For example, the following prints 2:

```python
letters = ["A", "B", "C", "D"]
print(letters.index("C"))
```

While looking at the wine data, now try to write Python expressions to extract the following:
* `Tinta de Toro`
* `Ponzi`
* `90.0`

Also try to complete the following:
* `csv_data[0][csv_header.index(????)]` to get "US"
* `csv_data[1][csv_header.index(????)]` to get "Bodega Carmen Rodríguez"
* `csv_data[2][csv_header.index(????)]` to get "Sauvignon Blanc"

You'll use the following function as the basis for accessing data in
P6, but first you need to fill in some missing pieces (ONLY change the
???? parts):

```python
def cell(row_idx, col_name):
    col_idx = ????
    val = csv_data[????][col_idx]
    if val == "":
        return None
    # optional: convert types based on column name?
    return val
```

Hints:
* it's fine to access earlier global variables in this function, such as `csv_data` and `csv_header`
* use the `index` list method

Is your implementation correct?  Test it with the following:

1. `cell(0, "country")` should return "US"
2. `cell(1, "points")` should return "96"
3. `cell(2, "price")` should return "90.0"
4. `cell(3, "variety")` should return "Pinot Noir"

**Optional:** it will save you time in the long run if `cell(1,
"points")` returns an `int` (example 2) and `cell(2, "price")` returns
a `float` (example 3) instead of strings.  Consider improving the
`cell` function so it automatically converts the result to the desired
value based on the column name (e.g., the value for any price might be
cast to a float).

**Important Reminder:** while you and your lab partner (if you have one) can
collaborate on writing the `cell` function, you may not collaborate with your lab
partner on other parts of the project, unless of your the person
you're doing the lab with is also your project partner.

## Sorting

## Sets

## Command-Line Arguments

