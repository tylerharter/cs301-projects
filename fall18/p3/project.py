import csv

class Project():
    hdata={}
    total=0
    def __init__(self):
        with open('hurricanes.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            iterator=0
            for row in csvReader:
                if iterator ==0:
                    iterator+=1
                    continue
                self.hdata[iterator]=row
                iterator+=1
            self.total=iterator-1

    """ Function that takes in record number and returns the name of the hurricane"""
    def GetName(self, recordNumber):
        if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][0] #storing Name at 0th index
        print("invalid row number for the data")
        return ""

    """ Function that takes in record number and returns the Date of the hurricane"""
    def GetDate(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][1] #storing Date at 1th index
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the time of the hurricane"""
    def GetTime(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][2] #storing Time at 2nd index
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the status of the hurricane"""
    def GetStatus(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][3]
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the latitude of the hurricane"""
    def GetLatitude(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][4]
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the longitude of the hurricane"""
    def GetLongitude(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][5]
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the wind speed of the hurricane"""
    def GetWindSpeed(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][6]
         print("invalid row number for the data")
         return ""

    """ Function that takes in record number and returns the ocean name of the hurricane"""
    def GetOcean(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][7]
         print("invalid row number for the data")
         return ""

    def GetNumberofRecords(self):
        return self.total

if __name__ == '__main__':
    p = Project()
    """index = p.total
    a=p.GetName(index)
    print(a)
    a=p.GetDate(index)
    print(a)
    a=p.GetTime(index)
    print(a)
    a=p.GetStatus(index)
    print(a)
    a=p.GetLatitude(index)
    print(a)
    a=p.GetLongitude(index)
    print(a)
    a=p.GetWindSpeed(index)
    print(a)
    a=p.GetOcean(index)
    print(a)
    print(p.GetNumberofRecords())"""
