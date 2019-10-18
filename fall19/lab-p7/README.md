# Lab 7: Dictionaries

In this lab, we'll practice using dictionaries in preperation for P7
(and exam 2!).  Start a new scratch notebook to do the exercises.

## Exercises

### Counting Letters

Fill in the blanks so that `counts` becomes a dictionary where each
key is a character and the corresponding value is how many times it
appeared in `PI`.

```python
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for char in ????:
    if not char in counts:
        counts[????] = ????
    else:
        ????[char] += ????
counts
```

If done correctly, you should see something like this:

```python
{'t': 4, 'h': 2, 'r': 3, 'e': 11, ',': 12, ' ': 12, 'd': 1, 'o': 5, 'n': 6, 'f': 4, 'u': 1, 'i': 6, 'v': 3, 'w': 1, 's': 1, 'x': 1}
```

### Counting Words

```python
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for word in PI.????(????):
    if ????:
        ????
    else:
        ????
counts
```

If done correctly, you should see something like this:

```python
{'three': 2, 'dot': 1, 'one': 2, 'four': 1, 'five': 3, 'nine': 2, 'two': 1, 'six': 1}
```

### Dictionary from Two Lists

Fill in the blanks:

```python
keys = ["three", "zero", "one"]
vals = ["tres", "cero", "uno"]
en2sp = ???? # empty dictionary
for i in range(len(????)):
    en2sp[keys[????]] = ????
en2sp
```

The resulting dictionary should map the English words to the Spanish
words, like this:

```python
{'three': 'tres', 'zero': 'cero', 'one': 'uno'}
```

Try using your dictionary:

```python
words = "I love Comp Sci three zero one".split(" ")
for i in range(len(words)):
    default = words[i] # don't translate it
    words[i] = en2sp.get(words[i], default)
" ".join(words)
```

Not exactly going to replace Google translate any time soon, but it's
a start...

### Flipping Keys and Values

What if we want a dictionary to convert from Spanish back to English?
Complete the code:

```python
sp2en = {}
for en in en2sp:
    sp = ????
    sp2en[sp] = ????
sp2en
```

You should get this:

```python
{'tres': 'three', 'cero': 'zero', 'uno': 'one'}
```

### Dictionary Division

What if we want to do a lot of division, but we have all our
numerators in one dictionary and all our denominators in another?

```python
numerators = {"A": 1, "B": 2, "C": 3}
denominators = {"A": 2, "B": 4, "C": 4}
result = {}
for key in ????:
    result[????] = ????[key] / ????[key]
result
````

If done correctly, you should get `{'A': 0.5, 'B': 0.5, 'C': 0.75}`.

### Ordered Print

Complete the code so it prints the incidents per year, with earliest
year first, like this:

```python
incidents = {2016: 14, 2019: 18, 2017: 13, 2018: 16, 2014: 8, 2015: 10}
keys = sorted(list(????.keys()))
for k in ????:
    print(k, incidents[????])
```

```
2014 8
2015 10
2016 14
2017 13
2018 16
2019 18
```

### Histogram

Modify the above code so it prints a histogram with letters, like this:

```
2014 ********
2015 **********
2016 **************
2017 *************
2018 ****************
2019 ******************
```

### Dictionary Max

Complete the following to find the year with the most incidents:

```python
incidents = {2016: 14, 2019: 18, 2017: 13, 2018: 16, 2014: 8, 2015: 10}
best_key = None
for key in incidents:
    if best_key == None or incidents[????] > incidents[????]:
        best_key = ????
print("Year", best_key, "had", incidents[????], "incidents (the max)")
```

## Project Hints

1. for project questions like q12, you'll need to pair up two lists to make a dictionary (review "Dictionary from Two Lists" from the lab)
2. q16 and q17 require some counting (review the first lab exercises)
3. q18  requires an average (review "Dictionary Division" above).
4. q19 and q20 are finding the key that yields the max value in a dictionary (in comparison, we've solved many problems prior involving finding the argument that yields the max return value from a function)
