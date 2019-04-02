# Lab 10: Files and Formats (not ready yet!!!)

In this lab, you'll get practice with files, formats, and namedtuples.

## File Vocabulary

In this lab and P9, you'll need to be familiar with the following
file-related terms to know what we're asking you to do.

Before we get started with the assignment, let's talk about the
distinction between these three terms, which will become important as
we go along.

* **Directory:** a collection of files.  "Folder" is a less-technical synonym you've doubtless heard frequently.

* **File Name:** a name you can use for a file if you know what directory you're in.  For example, `movies.csv`, `test.py`, and `main.ipynb` are examples of file names.  Note that different files can have the same name, as long as those files are in different directories.

* **Path:** a more-complete name that tells you the file name AND what directory it is in.  For example, `p8/main.ipynb` and `p9/main.ipynb` are examples of path names on a Mac, referring to a file named `main.ipynb` in the `p8` directory and a second file with the same name in the `p9` directory, respectively.  Windows uses back-slashes instead of forward slashes, so on a Windows laptop the paths would be `p7\main.ipynb` and `p8\main.ipynb`.  There may be more levels in a path to represent more levels of directories.  For example, `courses\cs301\p8\test.py` refers to the `test.py` file in the `p8` directory, which is in the `cs301` directory, which is in the `courses` directory.

In Python, there's not a special type for file names or paths; we just
use regular strings instead.

## Practice

Create a new directory named `lab10` and create a `main.ipynb` file there.

Let's start by doing some imports we'll need:

```python
import os, json, csv
from collection import namedtuple
```

### Files and Directories



file object

### JSON

loads
load

### CSV

DictReader

### namedtuple
