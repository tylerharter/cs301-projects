# Project 9: Amazon Reviews

## Clarifications/Corrections/Hints:
* Nov 7: Added hints for Q7
* Nov 10: Stage 2 released
* Nov 10: `test.py` updated.
* Nov 12: Added a section on linting, see bottom of document
* Nov 16 [hint]: how can you convert a string to a boolean?  Try putting `s == "False" in a cell`.  What does `bool(s)` evaluate to?  What about `s == "False"`?
* Nov 16 [hint]: if you're reading a `DictReader` for the csv, corrupt rows will have None values.  If you have a dict `d`, then `None in d.values()` is an easy way to notice.
* Nov 16 [hint]: to create Review objects, you need to match up part of the data from the CSV with another part of the data from the JSON.  The slow/bad way is to have a loop inside a loop (the outer loop over one file's data and the inner loop over the other file's data).  The better/faster way is to loop over the CSV rows, then grab the piece you want from the JSON file with a dict lookup.  Looking up a single key in a dict (with `d[key]`) is MUCH faster than looping over all the keys/values in a dict.

## Introduction

In this project, you'll be analyzing a collection of reviews of Amazon products (adapted from https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products/data).
This data is messy!  You'll face the following challenges:

* data is spread across multiple files
* some files will be CSVs, others JSONs
* the files may be missing values or be too corrupt to parse

In stage 1, you'll write code to cleanup the data, representing
everything as Review objects (you'll create a new type for these).  In
stage 2, you'll analyze your clean data.

## Setup

**Step 1:** download `data.zip` and extract it to a directory on your
computer (using [Mac directions](http://osxdaily.com/2017/11/05/how-open-zip-file-mac/) or
[Windows directions](https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files)).

**Step 2:** download `test.py` to the directory from step 1 (`test.py` should be next to the `data` directory, not in it)

**Step 3:** create a `main.ipynb` in the same location.  Do all work for both stages there, and turn it in when complete.

Note: Make sure `data`, `main.ipynb` and `test.py` are in same directory.  Otherwise getting the tests to pass on your machine only will not be a good indication of whether they'll pass when we run them with the files organized as such.

## The Stages

* [Stage 1](stage1.md): parse a mix of CSV and JSON files to get Review objects
* [Stage 2](stage2.md): analyze the reviews of the Amazon products

## Linting

We are now introducing linting as a way to help you write better code. Please check it out 
and try running it on your code! Everything you need to know to get started is explained 
[here](../../linter/README.md).