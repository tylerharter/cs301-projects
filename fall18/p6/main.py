import sys

def get_row(dataset, n):
  if dataset == None:
    return None
  else:
    return dataset[n]

#### ADD YOUR FUNCTIONS HERE ####

def process_args():
  """
  sys.argv[0] is the python file (in our case, it's going to be main.py)
  sys.argv[1] is the command
  sys.argv[2] is the name of the CSV file
  sys.argv[3] onwards are additional parameters required by commands
  HINT : everything in argv is going to be a string!
  """
  # Use the read_csv function to read in the CSV file and save it to a "dataset" variable
  # This is also the only time you should ever call the read_csv function. All the subsequent functions MUST use the dataset variable
  dataset = None

  # define a command for each of the functions you implement
  # we've implemented get_row for you
  command = sys.argv[1]
  output = None

  if command == 'get_row':
    # USAGE - python main.py get_row hurricanes.csv <row_index>
    # This function is going to return None until you actually implement read_csv and save it's result in dataset
    output = get_row(dataset, int(sys.argv[3]))

  print(output)

def main():
  process_args()

if __name__ == '__main__':
    main()

