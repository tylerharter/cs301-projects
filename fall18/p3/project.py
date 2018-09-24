import csv
hurricane_data_do_not_touch = []
def init():
    with open('hurricanes.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            hurricane_data_do_not_touch.append(row)
            
def getNumRecords():
    return len(hurricane_data_do_not_touch)

def getName(index):
    return hurricane_data_do_not_touch[int(index) - 1]['Name']

def getDate(index):
    return int(hurricane_data_do_not_touch[int(index) - 1]['Date'])

def getTime(index):
    return int(hurricane_data_do_not_touch[int(index) - 1]['Time'])

def getStatus(index):
    return hurricane_data_do_not_touch[int(index) - 1]['Status']

def getLatitude(index):
    return hurricane_data_do_not_touch[int(index) - 1]['Latitude']

def getLongitude(index):
    return hurricane_data_do_not_touch[int(index) - 1]['Longitude']

def getWindSpeed(index):
    return int(hurricane_data_do_not_touch[int(index) - 1]['WindSpeed'])

def getOcean(index):
    return hurricane_data_do_not_touch[int(index) - 1]['Ocean']

init()