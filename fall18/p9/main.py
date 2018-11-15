import json

#######################################################
               # FILL IN THESE FUNCTIONS #
#######################################################

def get_list_of_files(data_dir):
    pass

def read_json_file(filepath):
    pass

def read_csv_file(filepath):
    pass

def read_all(data_dir):
    pass

def read_and_clean_all(data_dir):
    pass

def write_json(data_dir, output_filename):
    pass

#######################################################
   # PLEASE DON'T MODIFY ANYTHING BELOW THIS POINT  #
#######################################################

def clean_dict(dictionary):
    """
    This function takes 1 single dictionary [1 tweet's data] 
    and does the following : 
    -- converts the datetime format
    -- converts the "num_liked" field to an int

    It returns a new dictionary with the above changes, but all the other
    data intact.
    """
    from datetime import datetime 

    newd = {}
    newd.update(dictionary)

    # convert num_liked to an int 
    newd['num_liked'] = int(dictionary['num_liked'])

    # convert datetime to MM-DD-YYYY format
    format_string = "%a %b %d %H:%M:%S PDT %Y"
    datetime_obj = datetime.strptime(dictionary['date'], format_string)
    newd['date'] = datetime_obj.strftime("%m-%d-%Y")
    
    return newd

def sort_list_of_dicts(items, dict_key, reverse=False):
    """
    items: a list of dicts to be sorted
    dict_key: what key use in the dicts to determine the order
    reverse: False means smallest first, True means biggest first

    For example:
    rows = [{"name": "Alice", "score": 10}, {"name": "Bob", "score": 9}]
    sort_list_of_dicts(rows, "score")
    # rows will be: [{"name": "Bob", "score": 9}, {"name": "Alice", "score": 10}]
    sort_list_of_dicts(rows, "name")
    # rows will be: [{"name": "Alice", "score": 10}, {"name": "Bob", "score": 9}]
    """
    items.sort(key=lambda item: item[dict_key], reverse=reverse)

def process_args(argv):
    command = argv[1]
    out = None

    if command == "get_list_of_files":
        rootdir = argv[2]
        out = get_list_of_files(rootdir)
    
    elif command == "read_json_file":
        path_to_file = argv[2]
        out = read_json_file(path_to_file)

    elif command == "read_csv_file":
        path_to_file = argv[2]
        out = read_csv_file(path_to_file)
    
    elif command == "read_all":
        rootdir = argv[2]
        out = read_all(rootdir)

    elif command == "read_and_clean_all":
        rootdir = argv[2]
        out = read_and_clean_all(rootdir)

    elif command == "write_json":
        rootdir = argv[2]
        outfile = argv[3]
        write_json(rootdir, outfile)

    else:
        print("Bad command")

    if out:
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    from sys import argv
    import os 

    if len(argv) < 2: 
        print("Please enter a command.") 
        exit(1)
    
    should_exit = False
    if argv[1] == 'write_json': 
        if len(argv) != 4:
            print("write_csv takes exactly 2 additional arguments : [root_directory] and [output_path]")
            should_exit = True
    else:
        if len(argv) != 3:
            print("%s takes exactly 1 additional argument : [path_to_file/directory]" % argv[1])
            should_exit = True
    
    arg_path = argv[2]
    if not os.path.exists(arg_path):
        print("The path '%s' you specified does not exist, are you sure you have it in your current directory?" % argv[2])
        should_exit = True
    else:
        if argv[1] in ['read_json_file', 'read_csv_file']:
            if not os.path.isfile(arg_path):
                print("'%s' does not refer to a single file. Are you sure you supplied the right path?" % arg_path)
                should_exit = True
        else:
            if not os.path.isdir(arg_path):
                print("'%s' is not a directory. Are you sure you supplied the right path?" % arg_path)
                should_exit = True
    
    if should_exit:
        print("Exiting.. please try again with the correct arguments.")
    else:
        process_args(argv)
    
