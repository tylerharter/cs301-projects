import json,sys, operator
from collections import namedtuple

# Function that reads in json file and returns a list of dictionaries of the cars
def read_json(json_filename):
    return None

# Function that takes in a dictionary for a particular car and a field to be searched and returns the value of the
# field. NOTE: Code this function using recursion
def get_value(d, field):
    return None

#This function uses takes in the jdata returned by read_json function and makes namedtuple objects
# from each of the car dictionaries. Use the get_value function to get values of the different fields
def make_namedtuple_list(jdata):
    return None

#This function uses takes in the list of namedtuple cars returned by make_namedtuple_list function and then filters
# them based on the fields specified in the attributes dictionary
def create_filter(Cars, attributes):
    return None



#This function takes in the commandline arguments and calls the respective functions above. The fucntion has been coded
# to take in the arguments and call the function stubs. As you complete the functions above this funciton will call them
# and you can see your grade change
def process_args(args):
    if len(args) < 2:
        print("USAGE: python main.py <json file> <command> <args for command>")
        return
    command = args[2]
    jdata = read_json(args[1])
    #print(str(sorted(jdata.items(), key=operator.itemgetter(0))))
    if command == "get_value":
        if jdata==None:
            return None
        car_id = args[3]
        field = args[4]
        value = get_value(jdata[car_id],field)
        return(value)

    elif command == "read_json":
        if jdata==None:
            print("Create read_json function and assign value to jdata")
            return None
        else:
            return str(sorted(jdata.items(), key=operator.itemgetter(0))) #This code lets us sort your output by car id. Do not change this

    elif command =="makelist":
        cars_list = make_namedtuple_list(jdata)
        if cars_list==None:
            print("Function make_namedtuple_list() not coded properly")
            return None
        clist = sorted(cars_list, key=operator.attrgetter("Id"))  #This code lets us sort your output by car id. Do not change this
        return str(clist)
    elif command == "filter":
        arg = json.loads(args[3])
        if jdata==None:
            return None
        cars_list = make_namedtuple_list(jdata)
        if cars_list==None:
            return None
        carlist = create_filter(cars_list, arg)
        if carlist==None:
            print("Function make_namedtuple_list() not coded properly")
            return None
        flist = sorted(carlist, key=operator.attrgetter("Id"))  #This code lets us sort your output by car id. Do not change this
        return str(flist)

def main():
    print(process_args(sys.argv))
if __name__ == '__main__':
    main()

