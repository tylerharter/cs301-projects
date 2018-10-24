import json
import sys

#### ADD YOUR FUNCTIONS HERE ####

def process_args():
    """
    sys.argv[0] is the python file (in our case, it's going to be main.py)
    sys.argv[1] is the command
    sys.argv[2] is the movie file
    sys.argv[3] is the mapping file
    sys.argv[4] onwards are additional parameters required by your commands
    HINT : everything in argv is going to be a string!
    """
    if len(sys.argv) < 4:
        print("USAGE: python main.py <command> <movie file> <mapping file> <args for command>")
        return

    command = sys.argv[1]

    if command == "something":
        myoutput = "We're going to be printing all output using json.dumps!"
        print(json.dumps(myoutput, indent=2))
        return

def main():
    process_args()

if __name__ == '__main__':
    main()

