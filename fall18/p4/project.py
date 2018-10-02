import csv

def getNumRecords():
    """This function will return the number of records in the dataset"""
    return len(imdb_movie_data)//2

def getMovieData(field, movie=None, index=None):
    """This function will return the value of the field corresponding to either a movie or an index"""
    if movie is not None:
        if movie not in imdb_movie_data:
            print("Invalid Movie Name")
            return -1 
        if field not in imdb_movie_data[movie]:
            print("Invalid Field Name")
            return -1
        return imdb_movie_data[movie][field]

    if index is not None:
        if index not in imdb_movie_data:
            print(index)
            print("Invalid index")
            return -1 
        if field not in imdb_movie_data[index]:
            print("Invalid Field Name")
            return -1
        return imdb_movie_data[index][field]

    print("Please specify either the Movie Name or Rank")


def readData():
    """This function reads the data from the csv file"""
    imdb_movie_data = {}
    with open('IMDB-Movie-Data.csv') as csvimdb_movie_dataFile:
        csvReader = csv.reader(csvimdb_movie_dataFile)
        header=True
        for row in csvReader:
            if header:
                header=False
                continue
            # key = rank
            imdb_movie_data[int(row[0])] = {'Title':row[1],'Genres':row[2],'Director':row[3],'Cast':row[4],'Year':int(row[5]),'Runtime':int(row[6]),'Rating':float(row[7]),'Revenue':row[8]}
            # key = title
            imdb_movie_data[row[1]] = {'Index':int(row[0]),'Genres':row[2],'Director':row[3],'Cast':row[4],'Year':int(row[5]),'Runtime':int(row[6]),'Rating':float(row[7]),'Revenue':row[8]}
    return imdb_movie_data

imdb_movie_data = readData()