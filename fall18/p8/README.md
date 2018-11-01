# Project 8

In this assignment we are going to learn:

* How to read json files and parse them using recursion.
* How to create and use namedtuples


We are going to work with json data on cars for this assignment.

Download the files using the links below

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/main.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/test.py)
* [test.txt](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/test.txt)
* [small_cars.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/small_cars.json)
* [cars.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/cars.json)

# JSON Files:

The small_cars.json only contains data of 3 cars. We recommend you use
this file to manually test your code by running main.py.

Our test.py will run some tests using small_cars.json and some tests
using the much larger cars.json file.

Here is a sample structure of a single car data from the json file:

```json
{
  "1": {
    "Performance": {
      "Mileage": {
        "City mpg": "18",
        "Highway_mpg": "25"
      },
      "Horsepower": "250"
    },
    "Build": {
      "Make": "Audi",
      "Model": "Audi A3",
      "Year": "2009"
    },
    "Config": {
      "Transmission": {
        "Type": "Automatic",
        "Driveline": "2009",
        "Classification": "6 Speed Automatic Select Shift"
      },
      "Engine_Type": "Audi 3.2L 6 cylinder 250hp 236ft-lbs",
      "Dimensions": {
        "Length": "143"
      },
      "Height": "140"
    },
    "Hybrid": "False"
  }
}

Notice that the data consists of nested dictionaries, and that all
values are strings.

```

## 1: Reading the json data

The first step of the assignment is to read the json file and load it
into our program. Let us write a function to do this.

### 1.1 The `read_json` function:
>inputs to this function: 
>
> *json_filename* : a string which represents the name of the json file

The function should return a Python dictionary correpsonding to the
data in the JSON file named `json_filename`.  To load json data you
can read about how to use the `json.loads` function.  The `json.loads`
function returns Python data structures corresponding to JSON,
represented as a string (which may have been read from a file).  We
have created a skeleton of the `read_json` function for you to
complete.

Note: The `process_args` function has been provided for you in initial
main.py. This function handles commandline arguments and calls the
functions based on the commands. For this assignment, no major
modification to `process_args` is necessary.

You can test your code from terminal:
>python main.py small_cars.json read_json

```json
{
  "1": {
    "Build": {
      "Make": "Audi",
      "Model": "Audi A3",
      "Year": "2009"
    },
    "Config": {
      "Dimensions": {
        "Length": "143"
      },
      "Engine_Type": "Audi 3.2L 6 cylinder 250hp 236ft-lbs",
      "Height": "140",
      "Transmission": {
        "Classification": "6 Speed Automatic Select Shift",
        "Driveline": "2009",
        "Type": "Automatic"
      }
    },
    "Hybrid": "False",
    "Performance": {
      "Horsepower": "250",
      "Mileage": {
        "City mpg": "18",
        "Highway_mpg": "25"
      }
    }
  },
  "2": {
    "Build": {
      "Make": "Chevrolet",
      "Model": "Chevrolet Express",
      "Year": "2011"
    },
    "Config": {
      "Dimensions": {
        "Length": "60"
      },
      "Engine_Type": "Chevrolet 5.3L 8 Cylinder 310 hp 334 ft-lbs FFV",
      "Height": "77",
      "Transmission": {
        "Classification": "4 Speed Automatic",
        "Driveline": "2011",
        "Type": "Automatic"
      }
    },
    "Hybrid": "False",
    "Performance": {
      "Horsepower": "310",
      "Mileage": {
        "City mpg": "13",
        "Highway_mpg": "17"
      }
    }
  },
  "3": {
    "Build": {
      "Make": "Nissan",
      "Model": "Nissan 370Z Coupe",
      "Year": "2009"
    },
    "Config": {
      "Dimensions": {
        "Length": "75"
      },
      "Engine_Type": "Nissan 3.7L 6 Cylinder 350hp 276 ft-lbs",
      "Height": "35",
      "Transmission": {
        "Classification": "6 Speed Manual",
        "Driveline": "2009",
        "Type": "Manual"
      }
    },
    "Hybrid": "False",
    "Performance": {
      "Horsepower": "350",
      "Mileage": {
        "City mpg": "18",
        "Highway_mpg": "26"
      }
    }
  }
}
```

In the above example, there are three cars, with IDs "1", "2", and
"3", as indicated by the keys in the top-level dictionary.  Each maps
to a dictionary with information about a car.  For example, the last
car dictionary is as follows:

```json
{
    "Build": {
      "Make": "Nissan",
      "Model": "Nissan 370Z Coupe",
      "Year": "2009"
    },
    "Config": {
      "Dimensions": {
        "Length": "75"
      },
      "Engine_Type": "Nissan 3.7L 6 Cylinder 350hp 276 ft-lbs",
      "Height": "35",
      "Transmission": {
        "Classification": "6 Speed Manual",
        "Driveline": "2009",
        "Type": "Manual"
      }
    },
    "Hybrid": "False",
    "Performance": {
      "Horsepower": "350",
      "Mileage": {
        "City mpg": "18",
        "Highway_mpg": "26"
      }
    }
  }
```

*If your read_json function is correct, your score from test.py should
 be 10% before you proceed.*

### 1.2: The `get_value` function:

As you can see in the above example, data about a car is nested in
dictionaries at varying levels.  For example, if `car` is a
dictionary, one might determine whether the car is hybrid by
evaluating `car["Hybrid"]` or lookup the make with
`car["Build"]["Make"]`.

You must now write a recursive function called `get_value` that
searches through the nested dictionaries for a given key, and returns
the associated values.  For example, `get_value(car, "Hybrid")` would
find the value at `car["Hybrid"]`, and `get_value(car, "Length")`
would find the value at `car["Config"]["Dimensions"]["Length"]`.

>inputs to this function: 
>
>car\_data : a dictionary containing information of  a particular car.
>
>field: The key that we are searching for.

Write a `recursive` function that would find the value for a given key in the json data and return that value.

Note: There are multiple ways of coding this function that will cause
the test to pass, however you should ONLY implement a RECURSIVE
solution.  If you write a function that is not recursive, or a
function that would not work on data from JSON data unrelated to cars,
you will lose points during code review.

You can test your program by running main.py and giving a car ID and a key to lookup, as in this example:

```
prompt> python correct.py small_cars.json get_value 1 Year
"2009"
prompt> python correct.py small_cars.json get_value 2 Year
"2011"
prompt> python correct.py small_cars.json get_value 2 Horsepower
"310"
```

*If everything until here is correct, your score from test.py should be 50%.*


## 2: namedtuples

We will now learn to quickly load json data as namedtuple objects.

### 2.1 The `make_namedtuple_list` function: 

Now we write a function that would create a list of namedtuple objects for all the cars in the json file. Here we will go through all car entries in the dictionary, create a namedtuple object for each of them. For this you can should have the following fields as your class members:'Id', 'Make', 'Model', 'Year', 'Transmission'.
> Note: They keys of the dictionary will now become the *Id* field in your namedtuple. The values of Make,Model,Year and Transmission can be obtained by calling the `get_value` function.

You can pull out the values for these fields from the json data by calling the getValue function you coded earlier.

>inputs to this function: 
>
> json_data: The dictionary containing the data of all the cars

This function will return a list of namedtuple objects for all cars.To run this function use:

>python main.py cars.json makelist

*If everything until here is correct, your score from test.py should be 70%.*


### 2.2 The `create_filter` function: 

This function will help us extract data from the namedtuple list of objects. Data is extracted based on some filtering condition.

>inputs to this function: 
>
>car_list: list of namedtuple objects
>
>filtering_criteria: a dictionary with conditions based on which filtering needs to be done.

The function will go through the list of all json data and select the ones that match all of the given criteria and add that into a list. The new list with the filtered objects is returned.

Here is a sample:
>python main.py  cars.json filter {\\\"Make\\\":\\\"Acura\\\"}
>
>Note:When passing a dictionary as a command line argument please take care to escape quotes with backslashes.

```python
Output:
[Car(Id='13', Make='Acura', Model='Acura TL', Year='2012', Transmission={'Type': 'Automatic', 'Driveline': '2012', 'Classification': '6 Speed Automatic Select Shift'}), Car(Id='14', Make='Acura', Model='Acura TL', Year='2012', Transmission={'Type': 'Automatic', 'Driveline': '2012', 'Classification': '6 Speed Automatic Select Shift'})]


```
*If everything until here is correct, your score from test.py should be 100%.*


