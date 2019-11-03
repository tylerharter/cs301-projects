# Project 9: Amazon Reviews

## Introduction

In this project, you'll be analyzing a collection of reviews of Amazon products on Amazon.
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

**Step 2:** download `test.py` to the directory from step 1 (`test.py` be next to the `data` directory, for example)

**Step 3:** create a `main.ipynb` in the same location.  Do all work for both stages there, and turn it in when complete.

Note: Make sure `data`, `main.ipynb` and `test.py` are in same directory.

## The Stages

* [Stage 1](stage1.md): parse a mix of CSV and JSON files to get Review objects
* [Stage 2](stage2.md): learn about the reviewers and recurse
