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

    """ Function that takes in state name and year and returns the population for that year"""
    def GetName(self, recordNumber):
        if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][0] #storing Name at 0th index
        print("invalid row number for the data")
        return ""

    def GetDate(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][1] #storing Date at 1th index
         print("invalid row number for the data")
         return ""

    def GetTime(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][2] #storing Time at 2nd index
         print("invalid row number for the data")
         return ""

    def GetStatus(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][3]
         print("invalid row number for the data")
         return ""

    def GetLatitude(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][4]
         print("invalid row number for the data")
         return ""

    def GetLongitude(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][5]
         print("invalid row number for the data")
         return ""

    def GetWindSpeed(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][6]
         print("invalid row number for the data")
         return ""

    def GetOcean(self, recordNumber):
         if recordNumber <= self.total and recordNumber >0:
            return self.hdata[recordNumber][7]
         print("invalid row number for the data")
         return ""

    def GetNumberofRecords(self):
        return self.total

if __name__ == '__main__':
    p = Project()
    index = p.total
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
    print(p.GetNumberofRecords())
