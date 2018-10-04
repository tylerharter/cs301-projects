# Project 4

This project will primarily focus on providing further practice with
**conditional statments** and **loops**. You will also get some
experience accepting user input, and checking whether such inputs are
sane.  To start, download the test.py file to your project
directory.

* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p3/test.py)

**Note:** This project does not provide you a project.py (you won't be
needing it) or a main.py to start from (you can start from
scratch). You should hand in **main.py** file when you are done.

Your program will grade students and provide basic statistics when
requested.  Hence, no data file is necessary, because all data is
typed by the user.

# Overview

Below is an example of how a user might interact with your program
(parts typed by the user are in bold).

<pre>
ty-mac:p4$ <b>python main.py</b>
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>80</b>
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>70</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>a</b>
80.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$ 
</pre>

Your program should keep taking input until the user indicates they
want to exit.  There are five valid things the user may type, and here
is what your program should do in each case:

* **any number between 0 and 100**: the program should treat the number as a percent, and print a corresponding letter grade (between A and F)
* **q**: print "done" and quit running
* **c**: print the number of scores entered so far
* **a**: print the average score entered so far
* **r**: clear the statistics so that the number of scores entered is considered 0 and the average is reset

The user may also enter tricky input, including (but not limited to)
upper case commands (which should be accepted) and numbers over 100
(which should be rejected).

# Getting Started

There are a lot of tests this time (200 of them!), and many of them
are fairly complicated, so it's probably easier to start writing your
main.py directly and testing it yourself manually before you try
running our tests.  If you focus on writing a correct program, you
won't need to worry about looking at each of the 200 tests.

Your program will need to keep asking the user for input in a loop.
To get started, you could write a simple program that just echoes
input by typing the following in your new main.py file:

```python
while True:
    val = input("enter something: ")
    print(val)
print('done')
```

Try running it:

<pre>
ty-mac:p4$ python main.py
enter something: <b>3</b>
3
enter something: <b>howdy</b>
howdy
enter something: <b>how do i exit?</b>
how do i exit?
enter something:   C-c C-cTraceback (most recent call last):
  File "main.py", line 2, in <module>
      val = input("enter something: ")
      KeyboardInterrupt
ty-mac:p4$ 
</pre>

The program never prints "done", because it contains an infinite loop.
The only way to stop the program is to kill it, by hitting control-C
on your keyboard (in the terminal, this kills a program instead of
copying, contrary to what you may have expected).

To get started, you only need to make two small changes to the above
program in order to pass the first test in test.py:

1. change the prompt from "enter something: " to "enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: "
2. TODO

# Directions

