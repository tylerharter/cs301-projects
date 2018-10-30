# Project 8

In this assignment we are going to learn:

* How to read json files and parse them using recursion.
* How to create and use namedtuples


We are going to work with json data on cars for this assignment.

Download the files using the links below

* [main.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/main.py)
* [test.py](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/test.py)
* [cars_sample.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/cars.json)
* [cars.json](https://raw.githubusercontent.com/tylerharter/cs301-projects/master/fall18/p8/carssmaple.json)



# Files involved:

The cars_sample.json only contains data of 3 cars. It is useful to use this file to develop your code.

The file “cars.json” has the actual data. This should be used to test your code.

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

```

## 1: Reading the json data

The first step of the assignment is to read the json file and load it into our program. Let us write a function to do this.

### 1.1 The `read_json` function:
>inputs to this function: 

>*json_filename* : a string which represents the name of the json file

To load a json data you will use json.loads.
This function should return a dictionary that you obtain when you load the json data.

You can test your code from your console:


```python 

>>import main
>> main.read_json("cars_sample.json")

Output:

{'1': {'Build': {'Make': 'Audi', 'Model': 'Audi A3', 'Year': '2009'},
  'Config': {'Dimensions': {'Length': '143'},
   'Engine_Type': 'Audi 3.2L 6 cylinder 250hp 236ft-lbs',
   'Height': '140',
   'Transmission': {'Classification': '6 Speed Automatic Select Shift',
    'Driveline': '2009',
    'Type': 'Automatic'}},
  'Hybrid': 'False',
  'Performance': {'Horsepower': '250',
   'Mileage': {'City mpg': '18', 'Highway_mpg': '25'}}},
 '2': {'Build': {'Make': 'Audi', 'Model': 'Audi A3', 'Year': '2009'},
  'Config': {'Dimensions': {'Length': '143'},
   'Engine_Type': 'Audi 2.0L 4 cylinder 200 hp 207 ft-lbs Turbo',
   'Height': '140',
   'Transmission': {'Classification': '6 Speed Automatic Select Shift',
    'Driveline': '2009',
    'Type': 'Automatic'}},
  'Hybrid': 'False',
  'Performance': {'Horsepower': '200',
   'Mileage': {'City mpg': '22', 'Highway_mpg': '28'}}},
 '3': {'Build': {'Make': 'Audi', 'Model': 'Audi A3', 'Year': '2009'},
  'Config': {'Dimensions': {'Length': '143'},
   'Engine_Type': 'Audi 2.0L 4 cylinder 200 hp 207 ft-lbs Turbo',
   'Height': '140',
   'Transmission': {'Classification': '6 Speed Manual',
    'Driveline': '2009',
    'Type': 'Manual'}},
  'Hybrid': 'False',
  'Performance': {'Horsepower': '200',
   'Mileage': {'City mpg': '21', 'Highway_mpg': '30'}}}}
```

Note: The process args function has been pre-written. Hence for this assignment no modification of process_args() is necessary.

>python main.py cars.json read_json

*If everything until here is correct, your score from test.py should be 10%.*

### 1.2: The `get_value` function: 
In the next step we need to create car objects. In order to do so  we need to first have a mechanism to retrieve specific information from the json data.Let us write a function that will help us find the value for the given field in the json_data. We will use **recursion** for this function. 

>inputs to this function: 

>car\_data : a dictionary containing information of  a particular car.

> field: The key that we are searching for.

Write a `recursive` function that would find the value for a given key in the json data and return that value.

>Note: There are multiple ways of coding this function that will cause the test to pass, however you should ONLY implement a RECURSIVE solution.

>python main.py cars.json read_json

*If everything until here is correct, your score from test.py should be 35%.*


## 2: namedtuples

We will now learn to quickly load json data as namedtuple objects.

### 2.1 The `make_namedtuple_list` function: 

Now we write a function that would create a list of namedtuple objects for all the cars in the json file. Here we will go through all car entries in the dictionary, create an object for each of them(using the existing `make_object` function.

>inputs to this function: 

>json_data: The dictionary containing the data of all the cars

This function will return a list of namedtuple objects for all cars.To run this function use:

>python main.py cars.json makelist

*If everything until here is correct, your score from test.py should be 55%.*


### 2.2 The `create_filter` function: 

This function will help us extract data from the namedtuple list of objects. Data is extracted based on some filtering condition.

>inputs to this function: 

>car_list: list of namedtuple objects

>filtering_criteria: a dictionary with conditions based on which filtering needs to be done.

The function will go through the list of all json data and select the ones that match all of the given criteria and add that into a list. The new list with the filtered objects is returned.

Here is a sample:
>python main.py  cars.json filter {\"Make\":\"Acura\"}

>Note:When passing a dictionary as a command line argument please take care to escape quotes with backslashes.

```python
Output:
[Car(Make=u'Acura', Model=u'Acura TL', Year=u'2012', Transmission={u'Type': u'Automatic', u'Classification': u'6 Speed Automatic Select Shift', u'Driveline': u'2012'}),
Car(Make=u'Acura', Model=u'Acura TL', Year=u'2012', Transmission={u'Type': u'Automatic', u'Classification': u'6 Speed Automatic Select Shift', u'Driveline': u'2012'})]

```
*If everything until here is correct, your score from test.py should be 100%.*


