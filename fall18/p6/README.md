# Project 6

Downlaod the files using the links below **(please don't use the hurricanes.csv from P3 as we've made some changes to it)** :

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p6/main.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p6/test.py)
* [expected.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p6/expected.json)
* [hurricanes.csv](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p6/hurricanes.csv) 

For this assignment, we're actually revisiting the hurricanes dataset, with one small catch. There's no `project.py`. You're going to be working directly with the CSV file, reading it into memory and saving it into a list of lists.

There are two key concepts you need to be really comfortable with before you dive into this assignment.

* Representing a dataset as a list of lists, and working with that list of lists
* Using `sys.argv` to read in and parse command line arguments

So make sure you take a second to refresh your understanding of these two concepts before getting started.

**NOTE:** The following python program `args.py` takes in two command line arguments from the user,
converts them to integers and prints them to the console.
```python
import sys

x = int(sys.argv[1])
y = int(sys.argv[2])
print(x, y)
print(x+y)
```

The above program should be executed as shown below in the terminal.
In the example below, we pass two command line arguments, i.e., 100 and 200.
```python
$ python args.py 100 200
100 200
300
```

## 1. Implement the `read_csv` function.

> ##### input(s) to this function :
> * `csv_filename` : the name of the csv file to read in

Our first step, is to read in our CSV file and save it as a list of lists.

Create a function called `read_csv` which takes a filename as the only parameter and returns all the rows in the csv file as a list of lists.

This function should use the `csv.reader` function [[link to documentation]](http://automatetheboringstuff.com/chapter14/) that we discussed in the class to read the file.

A really important point here is that you have to convert the values in `read_csv` to the right data types! The `read_csv` function gives you all strings by default.

The CSV file has 3 columns, and this is what their data types should end up as in the list of lists your function returns:

> Column 1 : Name of Hurricane : `string`       
> Column 2 : Windspeed  : `int`     
> Column 3 : Name of Ocean : `string`       

Please keep in mind that this function is the **only place** you will ever work directly with the CSV file. All functions from this point on should work on the list of lists the `read_csv` function returns (which is going to be called `dataset` from here on.)

*If your `read_csv` function is implemented correctly, you can run `test.py` and you should be getting a score of `15%`.*

## 2. Implement Functions to Analyze the Data

### 2.1 : The `sample` function :

#### 2.1.1 : Implement the function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `num_rows` : an integer
> * `start_or_end` : a string

The value returned by `read_csv` is a list of lists, but this list is too huge to look at.

We'd like you to create a function that returns a few rows from this big list.

The function `sample` should return :

- the **first** `num_rows` from the dataset if `start_or_end` is `"start"`     
- the **last** `num_rows` if `start_or_end` is `"end"`     
- `None` if `start_or_end` is anything besides `start` or `end`      

The function `sample` should return a list of lists similar to `read_csv`, but of size `num_rows`.


#### 2.1.2 : Tie everything until now together

Now that we have a function that's capable of reading in a CSV file and converting it to a list of lists, and a function that can return a small subset of the rows of the dataset, we need to tie it together.

Here's how you do this.

In the `process_args` function :
* Call the `read_csv` function with the `csv_file` and save the resulting list of lists into a variable called `dataset`
* Add a command (we've given you an example, `get_row`) for the `sample` function
* Use `sys.argv` to pass the command line arguments to your function    
* Run the sample command from the command line as follows :

Each line below shows one sample of the program main.py with different command line arguments. 
```bash
$ python main.py sample hurricanes.csv 10 start

$ python main.py sample hurricanes.csv 10 end

$ python main.py sample hurricanes.csv 10 abcd
```

Don't forget to convert the command line parameters to whatever type your function expects. A lot of the functions will require integer inputs.

Make sure you have this working before proceeding! We're going to repeat this flow over and over; implementing a function, and adding it to our list of commands we can run.

*If everything until here is correct, your score from test.py should be `25%`.*

### 2.2 The `get_cell` function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `row_idx` : an integer
> * `col_idx` : an integer

This function returns a **single value** at a given row (`row_idx`) and column (`col_idx`).

Don't forget to add it to the list of commands once you implement it. _(see Section 2.1.2 of this readme)_

Here's how you should be able to run it, once you have implemented this function and added it to the list of commands :

```bash
$ python main.py get_cell hurricanes.csv 20 2
```

*If everything until here is correct, your score from test.py should be `30%`.*

### 2.3 : The `get_fastest` function :
> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`

This function is very similar to the one we had in the earlier assignment. All you have to do is find the name of the fastest hurricane in the list.

Remember, your function needs to return the **name** of the fastest hurricane, not it's windspeed.

Go ahead and add it into the list of commands once done. 

You should be able to run it as follows : 

```bash
$ python main.py get_fastest hurricanes.csv 
```

*If everything until here is correct, your score from test.py should be `40%`.*

### 2.4 : The `get_column` function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `col_idx` : an integer

We are going to create a function that returns an entire column from the dataset.

For example, if the dataset is

```

[

    ["a", "b", "c"],

    ["d", "e", "f"],

    ["g", "h", "i"]

]

```


Then column 0 is `["a", "d", "g"]`, column 1 is `["b", "e", "h"]`, column 2 is `["c", "f", "i"]`.

The function `get_column` should return the entire column (a list) at position `col_idx`.

In the above example, `get_column(dataset, 1)` should return `["b", "e", "h"]`

You're going to be using this function a lot, as it's a very common operation (getting an entire column), so make sure it works perfectly!

This one goes into the list of commands as well, so go ahead and add it in. 

Once you do that, you should be able to run it as follows : 

```bash
$ python main.py get_column hurricanes.csv 1
```
*If everything until here is correct, your score from test.py should be `55%`.*

### 2.5 : The `names_alphabetical` function:

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`,

This function is just going to return a list of all the hurricane names, **sorted in alphabetical order.**

Use the `get_column` function you just wrote to make this a lot simpler!

Don't forget to add this to the list of commands. 

Once done, you should be able to run it as follows : 

```bash
$ python main.py names_alphabetical hurricanes.csv
```

*If everything until here is correct, your score from test.py should be `60%`.*

### 2.6 : The `avg_windspeed` function:

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`,

This function is just going to return the **average windspeed of all the hurricanes in the `dataset`**. Therefore, this returns just a single number, and not an entire list.

This function, as well as the one above, are examples of more complex things you can do since you already have a `get_column` function. Using functions can really help simplify complex tasks into smaller, more manageable pieces.

Add this into the list of commands once done. You should be able to run it as :

```bash
$ python main.py avg_windspeed hurricanes.csv
```

For this function, please return the result **rounded to 4 decimal places**. You can accomplish this using the round function. [[Link to Documentation]](https://docs.python.org/3/library/functions.html#round)  

*If everything until here is correct, your score from test.py should be `65%`.*

### 2.7 : The `filter_on_col` function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `col_idx` : an integer
> * `filter_condition` : a string

The ability to filter out rows based on a condition is a basic, but very important and useful part of working with datasets.

We're going to write a function that returns all the rows where the value of the `col_idx` column matches the `filter_condition`. You can assume that `filter_condition` will only be a `string`, so don't worry about comparing integers for now. 

For instance, if we had this dataset : 

```python
dataset = [
    ['0001', 'Anne', 'San Francisco', 92000]
    ['0002', 'Ashley', 'Madison', 102000]
    ['0003', 'Hartley', 'New York City', 120000]
    ['0004', 'Ash', 'San Francisco', 92000]
]
```

And we called the `filter_on_col` function with the following arguments :

```python
filter_on_col(dataset, 2, 'San Francisco')
```

We would get back : 

```python
[
  ['0001', 'Anne', 'San Francisco', 92000],
  ['0004', 'Ash', 'San Francisco', 92000],
]
```

Here's another example, if we used these arguments instead : 

```python
filter_on_col(dataset, 1, 'Anne')
```

We would get back :

```python
[
  ['0001', 'Anne', 'San Francisco', 92000],
]
```

Note that even though this returns just 1 row (since there's only 1 row where the 2nd column is `Anne`), it's _still returning a list of lists._ Just like you can have a list with only 1 item inside it (for instance, `[5]`), you can have a list of lists with only 1 element inside it.

Once you're done, add it to the list of commands as before.

You should be able to run it as follows once you add it to the list of commands: 

```bash
$ python main.py filter_on_col hurricanes.csv 0 DOG

$ python main.py filter_on_col hurricanes.csv 2 Atlantic
```
*If everything until here is correct, your score from test.py should be `75%`.*

### 2.8 : The `num_in_ocean` function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `ocean_name` : a string

This one is going to look familiar as well, but try using one of the functions you've already written to implement this.

All this needs to do, is return the **number of hurricanes** that happened in the Ocean who's name is `ocean_name`.

Add this to the commands as well. Once done, you should be able to run it from the terminal as : 

```bash
python main.py num_in_ocean hurricanes.csv Atlantic
```
*If everything until here is correct, your score from test.py should be `80%`.*

### 2.9 : The `cmp_avg_windspeed_by_ocean` function :

> ##### input(s) to this function :
> * `dataset` : the list of lists from `read_csv`
> * `ocean_name_1` : a string
> * `ocean_name_1` : a string

This function compares the average windspeeds for all hurricanes that happened in a particular ocean, against the average windspeed of those that happened in another.

Here's what it returns :

- If the averge windspeed of hurricanes in `ocean_name_1` is higher than that of `ocean_name_2` : **return 1**    
- If the averge windspeed of hurricanes in `ocean_name_2` is higher than that of `ocean_name_1` : **return -1**    
- If the averge windspeed of hurricanes in `ocean_name_2` is the same as that of `ocean_name_1` : **return 0**    

Here's an example to make this clearer :

> Let's say the Atlantic Ocean had 4 hurricanes with the following windspeeds : **10, 20, 30 and 50**        
> And, let's say, the Pacific Ocean had 5 hurricanes with the following windspeeds : **10, 30, 30, 50 and 80**            

_(of course, this data is just made up, your function will work on the real values in your list of lists)_

> The average windspeed of hurricanes in the Atlantic Ocean is **(10 + 20 + 30 + 50) / 4 = 27.5**               
> The average windspeed of hurricanes in the Pacific Ocean is **(10 + 30 + 30 + 50 + 80) / 5 = 40**             

So **in this case**, if we ran our function as follows :

```bash
python main.py cmp_avg_windspeed_by_ocean hurricanes.csv Atlantic Pacific
```

It would return a value of -1 (as the first ocean's windspeed is lower than the second)

However, if we ran it as follows :
```bash
python main.py cmp_avg_windspeed_by_ocean hurricanes.csv Pacific Atlantic
```
It would return a value of 1 instead. The order of the arguments plays an important role here as we're comparing the speeds of the first against the second ocean!

This function might seem complex, but if you use the right combination of functions you've already written, you'll be able to do it with just a few lines of code. Try to break the problem down into it's smaller parts, and see if you already have a function that does each part.

Last one! Add it into the list of commands. You should be able to run it as shown above.

*If everything until here is correct, your score from test.py should be `95%`.*

## Wrapping up

Almost done, all we need to do now is have an error message if someone enters a command we don't recognize.

If you see a command you don't recognize, just print out :

`Unknown command {command_name}`

So if I tried something like this :

```bash
python main.py avg_distance hurricanes.csv 20 10
```

I would get :
```bash
Unknown command avg_distance
```

Here's a hint : you don't need a function to do this.  

*If everything until here is correct, your score from test.py should be `100%`!*

## Summary

One of the key things you learnt in this assignment is the idea of breaking down complex tasks into simpler functions. This is something that every good programmer needs to be able to do, as without breaking down your code into functions, it becomes really challenging to end up with code that's easy to debug, test, and reuse.
