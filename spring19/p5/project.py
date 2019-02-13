from csv import DictReader as __DictReader

# key: (agency_id, year), val: spending in millions
__data = None

# key: agency name, val: agency ID
__agency_to_id = None


def init(path):
    """init(path) must be called to load data before other calls will work.  You should call it like this: init("madison.csv")"""

    global __data
    global __agency_to_id

    if path != 'madison.csv':
        print("WARNING!  Opening a path other than madison.csv.  " +
              "That's fine for testing your code yourself, but madison.csv " +
              "will be the only file around when we test your code " +
              "for grading.")

    __data = {}
    __agency_to_id = {}

    with open(path) as f:
        reader = __DictReader(f)
        for row in reader:
            agency_id = int(row['agency_id'])
            __agency_to_id[row['agency']] = agency_id
            for year in range(2015, 2018+1):
                __data[(agency_id, year)] = float(row[str(year)])

def dump():
    """prints all the data to the screen"""
    if __agency_to_id == None:
        raise Exception("you did not call init first")
    
    for agency in sorted(__agency_to_id.keys()):
        agency_id = __agency_to_id[agency]
        print("%-7s [ID %d]" % (agency, agency_id))
        for year in range(2015, 2018+1):
            print("  %d: $%f MILLION" % (year, __data[(agency_id, year)]))
        print()


def get_id(agency):
    """get_id(agency) returns the ID of the specified agency."""
    if __agency_to_id == None:
        raise Exception("you did not call init first")
    if not agency in __agency_to_id:
        raise Exception("No agency '%s', only these: %s" %
                        (str(agency), ','.join(list(__agency_to_id.keys()))))
    return __agency_to_id[agency]


def get_spending(agency_id, year=2018):
    """get_spending(agency_id, year) returns the dollars spent (in millions) by the specified agency in specified year."""
    if __data == None:
        raise Exception("you did not call init first")
    if not (agency_id, year) in __data:
        raise Exception("No data for agency %s, in year %s" %
                        (str(agency_id), str(year)))
    return __data[(agency_id, year)]
