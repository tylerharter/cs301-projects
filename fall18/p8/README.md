# Project 8

In this assignment we are going to learn:

* How to read JSON files and parse them using recursion.
* How to create and use namedtuples


We are going to work with JSON data on cars for this assignment.

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

Here is a sample structure of a single car data from the JSON file:

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

## 1: Reading the JSON data

The first step of the assignment is to read the JSON file and load it
into our program. Let us write a function to do this.

### 1.1 The `read_json` function:
>inputs to this function: 
>
> *json_filename* : a string which represents the name of the JSON file

The function should return a Python dictionary correpsonding to the
data in the JSON file named `json_filename`.  To load JSON data you
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

Write a `recursive` function that would find the value for a given key in the JSON data and return that value.

Note: There are multiple ways of coding this function that will cause
the test to pass, however you should ONLY implement a RECURSIVE
solution.  If you write a function that is not recursive, or a
function that would not work on data from JSON data unrelated to cars,
you will lose points during code review.

You can test your program by running main.py and giving a car ID and a key to lookup, as in this example:

```
prompt> python main.py small_cars.json get_value 1 Build
{
  "Make": "Audi",
  "Model": "Audi A3",
  "Year": "2009"
}
prompt> python main.py small_cars.json get_value 1 Year
"2009"
prompt> python main.py small_cars.json get_value 2 Year
"2011"
prompt> python main.py small_cars.json get_value 2 Horsepower
"310"
```

*If everything until here is correct, your score from test.py should be 50%.*


## 2: namedtuples

We will now learn to load JSON data as namedtuple objects.

### 2.1 The `make_namedtuple_list` function: 

We will now write a function to create a namedtuple object for each
car in the JSON file.

For this, you should first define a new namedtuple type, named "Car".
A Car should have the following fields: `id`, `make`, `model`, `year`,
and `transmission`.  Make sure you use the same Car type to create all
your car objects.

The `make_namedtuple_list` function will be as follows:

>inputs to this function: 
>
> jdata: The dictionary containing the data of all the cars

This function will return a list of namedtuple objects corresponding
to each car in jdata.  The jdata dictionary will be the one returned
by `read_json`.

Recall that each car has an ID (the key in jdata) and a value (a
nesting of dictionaries containing information about the car).
Therefore, you may use the keys in jdata to populate the `id` field of
a new Car object and the `get_value` function to extract Make, Model,
Year and Transmission values for your `make`, `model`, `year`, and
`transmission` fields respectively.

To debug your function, you may use:

>python main.py small_cars.json make_list

You can test your function as shown in this example below:

```
prompt> python main.py small_cars.json make_list
Car(id='1', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='2', make='Chevrolet', model='Chevrolet Express', year='2011', transmission={'Classification': '4 Speed Automatic', 'Driveline': '2011', 'Type': 'Automatic'})
Car(id='3', make='Nissan', model='Nissan 370Z Coupe', year='2009', transmission={'Classification': '6 Speed Manual', 'Driveline': '2009', 'Type': 'Manual'})
```


*If everything until here is correct, your score from test.py should be 70%.*


### 2.2 The `filter_cars` function: 

This function will help us extract data from the namedtuple list of objects. Data is extracted based on some filtering condition.

>inputs to this function: 
>
>car_list: list of namedtuple objects
>
>filters: a dictionary with conditions based on which filtering needs to be done.

The function will go through the list of all JSON data and select the
ones that match all of the given criteria and add that into a
list. The new list with the filtered objects is returned.

For example, if `cars` is a list of Car objects, one could find all Audis from 2011 my making the following call:

```python
filter_cars(cars, {"year": "2011", "make": "Audi"})
```

For your convenience, we have already provided the code for
constructing filters based on command line arguments within
the `process_args` function.

Here is an example of what you should expect when you run this `filter_cars` function:

```
prompt> python main.py cars.json filter year=2009,make=Audi
Car(id='1', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='10', make='Audi', model='Audi A4 Sedan', year='2009', transmission={'Classification': '6 Speed Manual', 'Driveline': '2009', 'Type': 'Manual'})
Car(id='11', make='Audi', model='Audi A4 Sedan', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='12', make='Audi', model='Audi A4 Sedan', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='2', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='3', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Manual', 'Driveline': '2009', 'Type': 'Manual'})
Car(id='4', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='5', make='Audi', model='Audi A3', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='6', make='Audi', model='Audi A5', year='2009', transmission={'Classification': '6 Speed Manual', 'Driveline': '2009', 'Type': 'Manual'})
Car(id='7', make='Audi', model='Audi A5', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='8', make='Audi', model='Audi Q7', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
Car(id='9', make='Audi', model='Audi Q7', year='2009', transmission={'Classification': '6 Speed Automatic Select Shift', 'Driveline': '2009', 'Type': 'Automatic'})
```

NOTE: Your `filter_cars` function may ignore all dictionary keys besides the
following: "make", "model", and "year".

*If everything until here is correct, your score from test.py should be 100%.*

####Good luck with this project! :) 
