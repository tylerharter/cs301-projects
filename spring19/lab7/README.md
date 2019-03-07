# Lab 7: Dictionaries

In this lab, we'll practice using dictionaries in preperation for P7
(and exam 2!).  Start a new scratch notebook to do the exercises.

## Exercises

### Counting Letters

Fill in the blanks so that `counts` becomes a dictionary where each
key is a character and the corresponding value is how many times it
appeared in `text`.

```python
text = "do, re, do, re, mi, do, re, mi, fa, sol, la, ti"
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
{'d': 3, 'o': 4, ',': 11, ' ': 11, 'r': 3, 'e': 3, 'm': 2, 'i': 3, 'f': 1, 'a': 2, 's': 1, 'l': 2, 't': 1}
```

### Counting Words

```python
text = "do, re, do, re, mi, do, re, mi, fa, sol, la, ti"
counts = {}
for word in text.????(????):
    if ????:
        ????
    else:
        ????
counts
```

If done correctly, you should see something like this:

```python
{'do': 3, 're': 3, 'mi': 2, 'fa': 1, 'sol': 1, 'la': 1, 'ti': 1}
```

### Dictionary from Two Lists

Fill in the blanks:

```python
keys = ["dog", "cat", "bird"]
vals = ["perro", "gato", "pájaro"]
en2sp = ???? # empty dictionary
for i in range(len(????)):
    en2sp[keys[????]] = ????
en2sp
```

The resulting dictionary should map the English words to the Spanish
words, like this:

```python
{'dog': 'perro', 'cat': 'gato', 'bird': 'pájaro'}
```

Try using your dictionary:

```python
words = "the dog chased the cat down the stairs".split(" ")
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

### Dictionary Division

### Ordered Print

### Dictionary Diff

## Project Hints
