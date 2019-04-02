# Lab 11: Recursion (Not Read Yet!!!)

## Recursion

As we learned in class, a function is recursive when it calls itself,
directly or indirectly.  We'll give you some practice here completing
some recursive code.

### Problem 1: Factorial

Yes, we did this in class, but see if you can complete it from memory
(or by deducing the answer) before referring back to your notes:

```python
def fact(n):
    if ????:
        return 1
    return n * ????
```

Here's a hint (the following is math, not Python):

```
1! = 1
2! = 1 * 2 = 2
3! = 1 * 2 * 3 = 6
4! = 1 * 2 * 3 * 4 = 24
```

When you're done, test your code with a few different inputs.  To
better understand what's happening, here are a couple things you could
do:
* run your code in Python Tutor
* add a print to the beginning of your function, like this: `print("fact(" + str(n) + ") was called")`

### Problem 2: String Reversal

We want `reverse` to reverse the letters in a string.  So, for
example, `reverse("Nacirema")` should return "America".

```python
def reverse(s):
    if len(s) < 2:
        return ????
    return reverse(????) + ????
```

Hints:
* using indexing and slicing on s
* notice that "ABCD" reversed is "BCD" reversed (i.e., "DCB"), concatenated with "A"

Try your function with a few strings.

### Problem 3: List Reversal

Write a function that reverses a list.  So, for example,
`list_rev([1,2,3])` should return `[3,2,1]`.  Both lists and strings
are sequences, so the code should be very similar to your string
reversal function.  In fact, we recommend you start by copying that
code, calling it with a list, then identifying the one reason the your
previous function doesn't work for lists as well as strings.

Hint:
* `[1,2,3]+4` is invalid, but `[1,2,3]+[4]` performs list concatenation.

**Challenge:** can you devise a single function that works for all
  types of sequences, including strings, lists, and tuples?

### Problem 4: Dictionary Printer

Complete the following function so that it prints nested dictionaries
in an easy-to-read way:

```python
def dprint(d, indent=0):
    print("Dictionary:")
    for k in d:
        v = d[????]
        print(" " * indent, end="")
        print(k + " => ", end="")
        if type(????) == dict:
            dprint(v, ????)
        else:
            print(v)
```

A call to `dprint({"A": 1, "B": {"C": 2, "D": 3, "E": {"F": 4}}, "G": 5})` should print the following:

```
Dictionary:
A => 1
B => Dictionary:
  C => 2
  D => 3
  E => Dictionary:
    F => 4
G => 5
```
