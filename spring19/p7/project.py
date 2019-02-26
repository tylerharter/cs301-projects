PlayerData = []
def __init__():
    import csv
    """This function will read in the csv_file and store it in a list of dictionaries"""
    
    fifaFile = open('FIFA18.csv',encoding='utf-8')
    fileReader = csv.reader(fifaFile)
    global PlayerData
    PlayerData = list(fileReader)
    for data in PlayerData[1:]:
        data[2] = float(data[2])
        data[6] = float(data[6])
        data[7] = float(data[7])
        data[8] = float(data[8])
    return PlayerData
    
__init__()