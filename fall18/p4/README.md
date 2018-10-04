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
requested.  No data file is necessary, because all data is
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

The program never prints "done" because it contains an infinite loop.
The only way to stop the program is to kill it, by hitting control-C
on your keyboard (in the terminal, this kills a program instead of
copying, contrary to what you may have expected).

To get started, you only need to make two small changes to the above
program in order to pass the first test in test.py:

1. change the prompt from "enter something: " to "enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: " (make sure to get this EXACTLY right)
2. inside your loop, add a conditional that checks whether val is "q"; if it is, break out of the loop (review the "break" in chapter 7 of your textbook if you don't remember how to do this)

Great, now run the tests.  You ought to be getting a score of 0.5%.
If not, working on passing that first test before continuing.

# General Directions

We now describe how to handle each of the five kinds of valid input a
user might type.

## 1. An integer between 0 and 100

In this case, you should print the letter grade corresponding to the
score.  The grades should be assigned as follows:

* A: 90 to 100
* B: 85 to 89
* C: 80 to 84
* D: 50 to 79
* F: 49 or less

You write the code for this as you like, but we recommend creating a
grading function that you can call from your main loop like this:

```python
print(grade(score))
```

The grading function might contain a chain of if and elif's to handle
each case.

You'll also need to maintain some stats so you can print the average
for when the user types "a" (another command).  For this, we recommend
keeping track of the number of grades that have been entered in one
variable and the sum of all the grades entered in a another variable
(please use descriptive names for the variables!).

It should look like this as the user enters numbers:

<pre>
ty-mac:p4$ python <b>main.py</b>
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>30</b>
F
...
</pre>

## 2. "q" command

This stands for "quit".  Your program should print "done" and stop
running.  It will look like this:

<pre>
ty-mac:p4$ python <b>main.py</b>
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$ 
</pre>

## 3. "c" command

This stands for count.  This prints the number of scores that have
been entered so far.  It works like this:

<pre>
ty-mac:p4$ python <b>main.py</b>
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>99</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>95</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>79</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
4
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$ 
</pre>

## 4. "a" command

This stands for average.  It prints the average score entered so far,
and looks like this:

<pre>
ty-mac:p4$ python <b>correct.py
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>80</b>
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>a</b>
80.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>a</b>
85.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>90</b>
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>a</b>
86.66666666666667
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$
</pre>

## 4. "r" command

This stands for reset.  It prints "reset" and clears the statistics,
starting fresh.  It looks like this:

<pre>
ty-mac:p4$ python correct.py
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>50</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>51</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>r</b>
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>52</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>53</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>54</b>
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>r</b>
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>c</b>
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: <b>q</b>
done
ty-mac:p4$ 
</pre>

# Tricky Input

There are three error messages you should sometimes display for
certain invalid inputs.  The messages and when you should display them
are as follows:

* "no scores entered", when the user tries to compute an average, but no scores have been entered (e.g., right after a reset)
* "out of range" if a user enters an integer larger than 100
* "bad input" if the user types something that does not consist solely of digits and does not match one of the commands given (e.g., "help", "-3", or "HAHAHAHAHA!")

Your program should be able to work properly under these scenarios:

* user uses capitals: you should treat "Q" the same as "q" and similar
* user types extra spaces before or after a command/number: your program should ignore those spaces
* user hints ENTER without typing anything (just ignore it)

Here are some example functions and code snippets from an interactive
Python session that might inspire your handling of the tricky input:

```python
>>> msg = '    hello   '
>>> print('message: ' + msg + '.')
message:     hello   .
>>> msg = msg.strip()
>>> print('message: ' + msg + '.')
message: hello.
>>> spaces = '    '
>>> spaces == ''
False
>>> spaces.strip() == ''
True
>>> x = '3'
>>> y = 'b'
>>> '0' <= x <= '9'
True
>>> '0' <= y <= '9'
False
>>> for letter in 'hello':
...   print(letter)
... 
h
e
l
l
o
```