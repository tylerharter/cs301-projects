import json, sys
from collections import namedtuple

# Function that reads in json file and returns a list of dictionaries
# of the cars
def read_json(json_filename):
    return None # TODO


# Function that takes in a dictionary for a particular car and a field
# to be searched and returns the value of the field. NOTE: Code this
# function using recursion
def get_value(car, field):
    return None # TODO


# This function uses takes in the jdata returned by read_json function
# and makes namedtuple objects from each of the car dictionaries. Use
# the get_value function to get values of the different fields
def make_namedtuple_list(jdata):
    return None # TODO


# This function uses takes in the list of namedtuple cars returned by
# make_namedtuple_list function and then filters them based on the
# fields specified in the attributes dictionary
def filter_cars(cars, filters):
    return None # TODO


# This function takes in the commandline arguments and calls the
# respective functions above. The fucntion has been coded to take in
# the arguments and call the function stubs. As you complete the
# functions above this funciton will call them and you can see your
# grade change
def process_args(args):
    # parse commandline inputs
    if len(args) < 2:
        print("USAGE: python main.py <json file> <command> <args for command>")
        return None
    command = args[2]
    print('Command: ' + command)

    jdata = read_json(args[1])
    if jdata == None:
        print('Please implement read_json first')
        return None

    # execute car commands
    if command == "read_json":
        return jdata

    elif command == "get_value":
        car_id = args[3]
        field = args[4]
        value = get_value(jdata[car_id], field)
        return value

    elif command == "make_list":
        car_list = make_namedtuple_list(jdata)
        for car in car_list:
            print(car)

    elif command == "filter":
        filters = {}
        for pair in args[3].split(','):
            pair = pair.split('=')
            assert(len(pair) == 2)
            filters[pair[0]] = pair[1]
        cars_list = make_namedtuple_list(jdata)
        filtered_cars = filter_cars(cars_list, filters)
        for car in filtered_cars:
            print(car)

    else:
        print("Unkown command: " + command)

    return None

def main():
    result = process_args(sys.argv)
    if result != None:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
