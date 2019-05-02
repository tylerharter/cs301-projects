# Lab 14: P10 wrapup and Exam Prep

You can use your final lab for two purposes:

1. ask TAs questions about P10
2. practice the following 10 questions to prep for the final (ask TAs if you have any questions)

The answers are [here](answers.md).

## Practice Questions

### 1. what is printed?

```python
from bs4 import BeautifulSoup

html = """
<b>hello</b> <i><b>cs</b> 301</i> <b>class</b>.
"""

doc = BeautifulSoup(html, "html.parser")
element = doc.find("i")
b_elements = element.find_all("b")
print(len(b_elements))
```

<ol type="a">
<li> -1
<li> 0
<li> 1
<li> 2
<li> 3
</ol>

### 2. what is a possible output?

```python
import numpy as np
from numpy.random import choice
seed_val = ???? # seed is some valid integer
np.random.seed(seed_val)
x = choice(5)
np.random.seed(seed_val)
y = choice(5)
print(x, y)
```

<ol type="a">
<li> 0 0
<li> 1 4
<li> 4
<li> 5 5
<li> 4 4 4
</ol>

### 3. which of the following evaluates to "X"?

```python
items = ["X", "Y"]
items.append(items)
```

<ol type="a">
<li> items[1]
<li> items[-1]
<li> items[-1][2][0]
<li> items[2][-1][0]
<li> both c and d
</ol>

### 4. what is a function that contains the yield keyword called?

<ol type="a">
<li> a yielder
<li> a generator function
<li> a recursive function
<li> an iterator
</ol>

### 5. what do Python frames contain?

<ol type="a">
<li> functions
<li> variables
<li> objects
<li> pictures of snakes
</ol>

### 6. what should replace ???? to get 60 in the result?

Assume the <b>students</b> table looks like this:

| student | project | score |
|---------|---------|-------|
| X       | P1      | 80    |
| Y       | P1      | 70    |
| X       | P2      | 60    |
| Y       | P2      | 50    |

```sql
SELECT score
FROM   students
????   student = 'X' AND project = 'P2'
```

<ol type="a">
<li> if
<li> IF
<li> WHERE
<li> HAVING
<li> WHEN
</ol>

### 7. what should replace ???? to get 75 and 55 in the results?

Assume the same <b>students</b> table from the previous question.

```sql
SELECT AVG(score)
FROM students
????
```

<ol type="a">
<li> GROUP BY student
<li> GROUP BY students
<li> GROUP BY project
<li> GROUP BY student, project
<li> GROUP BY score
</ol>

### 8. what is printed?

```python
letters = Series(["A", "B", "B", "C", "C", "C", "D", "D", "D"])
counts = letters.value_counts().value_counts() # not a typo!
print(counts[3])
```

<ol type="a">
<li> 0
<li> 1
<li> 2
<li> 3
<li> 4
</ol>

### 9. what values will be in s?

```python
df = DataFrame({
  "x": [1,2,3,4],
  "y": [4,3,2,1],
  "z": [5,6,7,8],
})

s = df[(df["y"] > df["x"]) | (df["z"] > 7)]["z"]
```

<ol type="a">
<li> s will be empty
<li> 5, 6
<li> 8
<li> 5, 6, 8
<li> 5, 6, 7, 8
</ol>

### 10. which of the following is true?

Calling `df.plot.line()` on a DataFrame `df` will:

<ol type="a">
<li> plot one line per row
<li> plot one line per column
<li> plot one line per cell
<li> plot one line, with x values from the `x` column and y values from the `y` column
<li> plot one line, with x values from the DataFrame's index and y values from the `y` column
</ol>
