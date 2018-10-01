import csv
import pandas as pd

def describe_data():
    df = pd.read_csv('IMDB-Movie-Data.csv')
    print(df.head().to_string(index=False))
    print()

def get_rows():
    return int(len(imdb_movie_data)/2)

def readData():
    imdb_movie_data = {}
    with open('IMDB-Movie-Data.csv') as csvimdb_movie_dataFile:
        csvReader = csv.reader(csvimdb_movie_dataFile)
        header=True
        for row in csvReader:
            if header:
                header=False
                continue
            # key = rank
            imdb_movie_data[int(row[0])] = {'Title':row[1],'Genres':row[2],'Description':row[3],'Director':row[4],'Cast':row[5],'Year':int(row[6]),'Runtime':int(row[7]),'Rating':float(row[8]),'Revenue':row[9]}
            # key = title
            imdb_movie_data[row[1]] = {'Index':int(row[0]),'Genres':row[2],'Description':row[3],'Director':row[4],'Cast':row[5],'Year':int(row[6]),'Runtime':int(row[7]),'Rating':float(row[8]),'Revenue':row[9]}
    return imdb_movie_data

def getMovieData(field, MovieName=None, Index=None):
    if MovieName is not None:
        if MovieName not in imdb_movie_data:
            print("Invalid Movie Name")
            return -1 
        if field not in imdb_movie_data[MovieName]:
            print("Invalid Field Name")
            return -1
        return imdb_movie_data[MovieName][field]

    if Index is not None:
        if Index not in imdb_movie_data:
            print(Index)
            print("Invalid Index")
            return -1 
        if field not in imdb_movie_data[Index]:
            print("Invalid Field Name")
            return -1
        return imdb_movie_data[Index][field]

    print("Please specify either the Movie Name or Rank")


imdb_movie_data = readData()