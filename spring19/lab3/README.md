# Lab 3: Intro and Vocabulary

For many projects this semester, we'll provide you with a *module* (a
collection of functions) named `project`, in a file named
`project.py`.  This module will provide functions that will help you
complete the project.  Today, we'll introduce the `project.py` file
you'll use for P3.

When using a module for the first time, the first thing you should do
is study the module's *API*.  API stands for "Application Programming
Interface", and refers to a collection of related functions (e.g.,
those in a module).  Understanding the API will involve learning about
each function and the parameters it takes.  You might need to learn
new *protocols* for using the function; protocols often specify the
order in which you may call functions.

There are two ways you can learn about an API.  First, the person who
created the API may have provided written directions, called
`documentation`.  Second, there are ways to can write code to learn
about a collection of functions; this approach is called `inspection`.

Summary of new terms:
* module
* API
* protocol
* documentation
* inspection

## Note on Academic Misconduct

You may do these lab exercises with anybody you like.  But be careful!
It's very natural to start working on P3 immediately after completing
the lab.  If you start working with somebody on P3, that person must
be your project partner until the next project; you not allowed to
start working on P3 with one person during lab, then finish working
with your actual partner.  Now may be a good time to review [our course policies](https://tyler.caraza-harter.com/cs301/spring19/syllabus.html).

## Setup

Create a `lab3` directory and download `lab.csv` above.  Also download
these files from the [P3 posting](https://github.com/tylerharter/cs301-projects/tree/master/spring19/p3)
to the `lab3` directory:
* `madison.csv`
* `project.py`

Open a terminal and navigate to your `lab3` directory.  Run `ls` to
make sure your three files are available.

We'll be doing these exercises in interactive mode, so type `python`
(or `python3`, if that's what you need to do on your laptop), and hit
ENTER.

## Inspecting builtins and `math`

In interactive mode, try the following examples (only type things after the `>>>`).

```python
>>> abs(-4)
4
>>> x = abs(-3)
>>> x
3
```

These two calls invoke the `abs` function because we have parenthesis.
What if we don't use parenthesis?  Try the following and see what you
get:

```python
>>> abs
```

```python
>>> type(abs)
```

What if we want to read about what `abs` does?  Run this:

```python
>>> abs.__doc__
```

Or this (compare the result):

```python
>>> print(abs.__doc__)
```

We didn't need to import anything to use `abs` because it is part of a
special module that is always imported called `__builtins__`.  Try
running this to see:

```python
type(__builtins__)
```

The `dir` function will show you everything that is inside a module,
so let's use it to learn about `__builtins__`.  Run this:

```python
dir(__builtins__)
```

This displays the names of lots of functions we've seen, such as
`abs`, `print`, `int`, `input`, and others.  Choose one you're
familiar with, and one that is unfamiliar to you, and then use
`.__doc__` to read the description.  For example, you might learn
about `max` like this:

```python
>>> print(max.__doc__)
max(iterable, *[, default=obj, key=func]) -> value
max(arg1, arg2, *args, *[, key=func]) -> value

With a single iterable argument, return its biggest item. The
default keyword-only argument specifies an object to return if
the provided iterable is empty.
With two or more arguments, return the largest argument.
```

Wow, that mentions a lot of things we haven't learned about yet!  As a
new Python programmer reading documentation, you'll have to dig
through things you don't understand yet to find bits that are useful
for you.  For example, in this case, the last line tells you
everything you need to know: "With two or more arguments, return the
largest argument."



## Inspecting `project`

## Filling Parameters
