def read_csv(filename):
  """

  read_csv("dataset.csv") -> [ [name, windspeed, ocean], .... ]

  """
  pass


def sample(dataset, n, start_or_end):
  """

  returns the first n or last n elements in dataset depending on start_or_end

  """
  pass


def get_column(dataset, col_idx):
  """

  returns the entire column at col_idx

  """
  pass


def windspeed_filter(rows, low, high):
  """
  returns rows with windspeed between low and high
  """
  pass


def filter_on_col(rows, filter_on_col, filter_value):
  """

  returns rows where the value of filter_on_col == filter_value
  --> filter_row(rows, 0, "BOB") --> only 1 row returned
  --> filter_row(rows, 2, "Atlantic" ---> multiple rows returned
  """
  pass


def main():

  ## TODO - IMPLEMENT read_csv() BEFORE YOU DO THESE
  hurricanes = read_csv("hurricanes.csv")

  print("Number of hurricanes: ")
  print()

  print("The first row is: ")
  print()

  print("The 10th row is: ")
  print()

  print("What is the name of the hurricane in the 5th row? ")
  print()

  print("What is the windspeed of the hurricane in the 5th row? ")
  print()

  ## TODO - IMPLEMENT sample() BEFORE YOU DO THESE
  print("The first 5 rows in the dataset are: ")
  print()

  print("The last 7 rows in the dataset are: ")
  print()

  ## TODO - IMPLEMENT get_column() BEFORE YOU DO THESE
  print("The names of all the hurricanes sorted alphabetically are: ")
  print()

  print("The average windspeed of all hurricanes is : ")
  print()

  print("What was the 2nd fastest hurricane?")
  print()

  ## TODO - IMPLEMENT windspeed_filter() BEFORE YOU DO THESE
  print("How many hurricanes had a windspeed betewen 30 and 50?")
  print()

  ## TODO - IMPLEMENT filter_on_col() BEFORE YOU DO THESE
  print("How many hurricanes occured in the Atlantic Ocean? ")
  print()

  print("Is the average windspeed of hurricanes in the atlantic ocean > pacific?")
  print()
