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

Try running this cell to see the files and directories available
alongside your notebook (remember that "." is a shorthand referring to
the current directory):

```python
# cell 1
os.listdir(".")
```

Let's try creating a new directory for some testing by running this cell:

```python
# cell 2
os.mkdir("fruits")
```

Now go back and manually rerun `cell 1` (when you called `listdir`).
Do you see the `fruits` directory this time?

Now click `Restart & Run All` from the `Kernel` menu.  Do you notice
that there's an exception in the cell where you created the `fruits`
directory?  This is because the directory already exists, and it is
not possible to create another with the same name.

There are two options for doing the `mkdir` in a way that won't cause
your notebook to fail in the case that the directory already exists.
To get familiar with them, replace the code with option 1 below, then
do a "Restart & Run All".  The try option 2 as well.

#### Option 1: try/except

```python
try:
    os.mkdir("fruit")
except FileExistsError:
    print("tried to create fruit, but it already existed")
```

#### Option 2: check beforehand

```python
if not os.path.exists("fruit"):
    os.mkdir("fruit")
else:
    print("did not try to create fruit because it already existed")
```

Let's try creating a couple files in the directory.  We'll need to
specify a path to the file.  Run this cell to get a path:

```python
path = os.path.join("fruit", "apple.txt")
path
```

If you're on a Mac, you'll see `fruit\apple.txt`; on Windows, you'll
see `fruit/apple.txt`.  Be careful!  Use this way to create paths.
Never use the regular string join method we've learned, because that
will not work on everbody's computer.

Now let's create it:

```python
f = open(path, "w", encoding="utf-8")
f.write("apples are red\n")
f.close()
```

Did it work?  Let's check:

```python
os.listdir("fruit")
```

Also, try using `idle` to find and open the `apple.txt` file.

Now copy and adapt the above code to create a `banana.txt` and
`orange.txt` file.  You can decide what to write to these files.

```python
def fruit_message(name):
    f = open(os.path.join("fruit", name+".txt"))
    msg = f.read()
    f.close()
    return msg
```

What does `fruit_message("apple")` return?  (try it!)

Try the other fruits too.  What if you try getting the message for a
fruit that doesn't exist?  Modify `fruit_message` so it return "bad
fruit" in that scenario.  Use the `mkdir` example from earlier for
inspiration.

### JSON

loads
load

### CSV

DictReader

### namedtuple

getattr
