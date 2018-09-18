import csv


def getArea(stateName):
    """ Function that takes in state name and returns the area of the state"""
    with open('area.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[0] == stateName:
                return float(row[1])


def getPopulation(stateName,year):
    """ Function that takes in state name and year to returns the population for that year"""
    with open('population.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        row0= next(csvReader)
        for row in csvReader:
            if row[0] == stateName and year == int(row0[1]):
                return float(row[1])
            elif row[0] == stateName and year == int(row0[2]):
                return float(row[2])
            elif row[0] == stateName and year == int(row0[3]):
                return float(row[3])

