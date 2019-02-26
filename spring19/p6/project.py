import math
import pandas as pd

__wine_data = None
__num_records = None

def init(path):
    """This function loads the specified CSV file and must be called before other functions"""
    global __wine_data
    global __num_records
    __wine_data = pd.read_csv(path, encoding = 'utf-8')
    __num_records = len(__wine_data)


def count():
    """This function will return the number of rows in the dataset """
    if __num_records:
        return __num_records
    else:
        raise Exception("Error! Please load the data file using init(path) first")


def preview():
    """This function will show a preview of the data """
    if __wine_data is not None:
        return __wine_data
    else:
        raise Exception("Please load the data file using init(path) first")


def cell(row, col):
    """cell(row, col) returns the data in the cell at the for the specified row index and column name."""
    if __num_records:
        val = __wine_data.loc[row][col]
        if pd.isnull(val):
            return None
        return val
    else:
        raise Exception("Please load the data file using init(path) first")
