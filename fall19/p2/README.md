# Project 2

In this project, you'll learn about types, operators, and boolean
logic.  To start, create a `p2` directory, and download `main.ipynb`
and `test.py` to that directory (IMPORTANT: use the same process to
download that you used for P1, which involves left-clicking the files
and then right-clicking the "Raw" button).

You will change `main.ipynb` and hand it in.  You should not change
`test.py`, and you should not hand it in.

After you've downloaded both files to `p2`, open a terminal window and
use `cd` to navigate to that directory.  You will likely need to
review the steps you used to cd to `p1` for the previous project, then
adapt those steps for `p2`.  To make sure you're in the correct
directory in terminal, type `ls` and make sure you see `main.ipynb`
and `test.py` listed.

Now run the following command:

```
python test.py
```

You should see the following output:

```
Summary:
  Test 1: PASS
  Test 2: no outputs in an Out[N] cell
  Test 3: PASS
  Test 4: no outputs in an Out[N] cell
  Test 5: no outputs in an Out[N] cell
  Test 6: no outputs in an Out[N] cell
  Test 7: no outputs in an Out[N] cell
  Test 8: no outputs in an Out[N] cell
  Test 9: no outputs in an Out[N] cell
  Test 10: found 34 but expected 7
  Test 11: found $$$ but expected $$$$$$$$$$$$$$$
  Test 12: found 333333333333333 but expected 45
  Test 13: found 16 but expected 64
  Test 14: no outputs in an Out[N] cell
  Test 15: found True but expected False
  Test 16: found False but expected True
  Test 17: found False but expected True
  Test 18: found 2 but expected True
  Test 19: found False but expected True
  Test 20: no outputs in an Out[N] cell

TOTAL SCORE: 10.00%
```

This means if you turn in main.py now, you'll get 10% for your score.
Pretty good for having done nothing yet, no?

You would get 10% because there are 20 problems, each worth 5%, and we
have done problems 1 and 3 for you.  You can see this because the
output above says "PASS" by them.  Your goal is to get more points by
getting test.py to print "PASS" by more problems.  In some cases, you
can see there is no answer in the original notebook (when it says `no
outputs in an Out[N] cell`), and in other cases you need to make a
change to correct a wrong answer (e.g., when it says `found 34 but
expected 7`).

Now let's open a second terminal window (we want one to run Jupyter
and one to run the tests).  In the second one, perform the same steps
to navigate to `p2` (again checking with `ls`).  Now run `jupyter
notebook` (or, if that doesn't work, try `python -m jupyter
notebook`).

Try solving the second question.  Then do a `Kernel` > `Restart & Run
All`.  If that looks good, save your work, switch to your other
terminal, and run the tests.  Make sure you're scoring 15% before
proceeding to the other questions.

Have fun, and run tests.py often to track your progress!
