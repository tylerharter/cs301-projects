import pandas as pd

# Wine data is a DataFrame , which is like a table, exactly like the one you see when you open the datafile wine_reviews.csv
__wine_data = None
__num_records = None


def init(path):
    """This function initializes the __wine_data and __num_records variables by loading the data from  the dataset file"""
    global __wine_data
    global __num_records
    
    if path != 'wine_reviews.csv' and path!= 'wine_reviews_sample.csv':
            print("WARNING!  Opening a path other than wine_reviews.csv or wine_reviews_sample.csv.  " +
                  "That's fine for testing your code yourself, but madison.csv " + 
                  "will be the only file around when we test your code for grading.")
    __wine_data = pd.read_csv(path,encoding = 'utf-8')
    __num_records = len(__wine_data)
    
    
def get_num_records():
    """This function will return the number of records or rows in the dataset """
    if __num_records:
        return __num_records
    else:
        print("Error! Please load the data file using init(path) first")

def preview_data():
    """This function will show a preview of the data """
    if __wine_data is not None:
        return __wine_data.head()
    else:
        print("Please load the data file using init(path) first")

def get_wine_data(field, query = None, qvalue =None, index=None):
    """This function will first check if a query value is specified along with the 'field', if so, it performs a filtering operation
    on the dataset based on qvalue corresponding to the query and returns the values of the 'field'. For example,
    calling get_wine_data('winery',query ='country', qvalue = 'Spain') gives all wineries in Spain. If no 'query' and 'qvalue' are specified,
    an index must be specified, in which case the value of field at that index is returned. For example
    calling get_wine_data('country',index = 23) will return value of the column country at index 23. Any other combination of inputs
    is prohibited"""
    if __num_records:
        if query is not None:
            if qvalue is not None:
                if query in __wine_data.columns and field in __wine_data.columns:
                    return __wine_data[__wine_data[query]==qvalue][field].tolist()
                else:
                    print("Invalid Input")
                    return None
            else:
                print("Invalid Input")
                return None
        else:
            if index is not None:
                return __wine_data.loc[index][field]
    else:
        print("Error!, please run init(path) before running any other function")

def get_record(index):
    """ Returns the row corresponding to index in the dataset"""
    if __num_records:
        if index>0 and index<__num_records:
            return __wine_data.loc[index]
        else:
            print("Error! Index value out of bounds.")
    else:
        print("Error! Please run init(path) before running any other function in project")
