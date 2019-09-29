__hurricane__ = []

def __init__():
    import csv
    """This function will read in the csv_file and store it in a list of dictionaries"""
    with open('hurricanes.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            __hurricane__.append(row)

def count():
    """This function will return the number of records in the dataset"""
    return len(__hurricane__)

def get_name(idx):
    """get_name(idx) returns the name of the hurricane in row idx"""
    return __hurricane__[int(idx)]['name']

def get_formed(idx):
    """get_formed(idx) returns the date of formation of the hurricane in row idx"""
    return (__hurricane__[int(idx)]['formed'])

def get_dissipated(idx):
    """get_dissipated(idx) returns the date of dissipation of the hurricane in row idx"""
    return (__hurricane__[int(idx)]['dissipated'])

def get_mph(idx):
    """get_mph(idx) returns the mph of the hurricane in row idx"""
    return int(__hurricane__[int(idx)]['mph'])

def get_damage(idx):
    """get_damage(idx) returns the damage in dollars of the hurricane in row idx"""
    return __hurricane__[int(idx)]['damage']

def get_deaths(idx):
    """get_deaths(idx) returns the deaths of the hurricane in row idx"""
    return int(__hurricane__[int(idx)]['deaths'])

__init__()
