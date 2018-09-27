import csv

__hurricane__ = []

def init():
    """This function will read in the csv_file and store it in a list of dictionaries"""
    with open('hurricanes.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            __hurricane__.append(row)
            
def getNumRecords():
    """This function will return the number of records in the dataset"""
    return len(__hurricane__)

def getName(index):
    """This function will return the name of the hurricane at the given index"""
    return __hurricane__[int(index)]['Name']

def getDate(index):
    """This function will return the date of the hurricane at the given index"""
    return int(__hurricane__[int(index)]['Date'])

def getTime(index):
    """This function will return the time of the hurricane at the given index"""
    return int(__hurricane__[int(index)]['Time'])

def getStatus(index):
    """This function will return the status of the hurricane at the given index"""
    return __hurricane__[int(index)]['Status']

def getLatitude(index):
    """This function will return the Latitude of the hurricane at the given index"""
    return __hurricane__[int(index)]['Latitude']

def getLongitude(index):
    """This function will return the Longitude of the hurricane at the given index"""
    return __hurricane__[int(index)]['Longitude']

def getWindSpeed(index):
    """This function will return the WindSpeed of the hurricane at the given index"""
    return int(__hurricane__[int(index)]['WindSpeed'])

def getOcean(index):
    """This function will return the oceanName of the hurricane at the given index"""
    return __hurricane__[int(index)]['Ocean']

init()