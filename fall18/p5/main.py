import project
import sys


# We have coded a function below that converts a string to uppercase or lowercase
def convertCase(original_string, case):
    if case == "uppercase":
        converted_string = original_string.upper()
    elif case == "lowercase":
        converted_string = original_string.lower()
    else:
        print("Unknown case, keeping string unchanged")
        converted_string = original_string
    return converted_string


# Write the reverseString(original_string) function here
# Note: You shouldn't use print in this function.


# Write the checkPalindrome(original_string) function here.
# Note: You shouldn't use print in this function.


# Write the findPalindromeMovie() function here
# Note: You shouldn't use print in this function.


# Write the encodeString(original_string) function here
# Note: You shouldn't use print in this function.


# Write the countMoviesByDirector(director_name) function here
# Note: You shouldn't use print in this function.


# Write the findNumSequels() function here
# Note: You shouldn't use print in this function.


# Write the mainActor(movie) function here
# Note: You shouldn't use print in this function.


# Write the findHighestRevenue(year) function here
# Note: You shouldn't use print in this function


# Write the countMoviesByActor(actor_name) function here
# Note: You shouldn't use print in this function.


# This function is incomplete, you need to write code to enable functionality for other command line arguments. 
# Follow the instructions below...
# Note: You shouldn't use print in this function.
def processCommands(command1, command2):
    output = None
    # Code for when the first command line argument is "upper"
    if command1 == "upper":
        output = convertCase(command2,"uppercase")

    # Write an if block similar to the above for the command "lower"

    
    # Write if blocks for the following commands: 
    # "reverse", "palindrome", "find_palin", "encode", "count_by_director"
    # "num_sequels", "main_actor", "highest_rev", "count_by_actor"







    # DO NOT modify any of the code below this.

    # The processCommands() function returns 
    return output



if __name__ == "__main__":
    l = len(sys.argv)
    if l<=1:
        print("No command line arguments found")
    else:
        command1 = sys.argv[1]
    
        if command1 in ['find_palin','num_sequels']:
            if l==2:
                print(processCommands(command1,None))
            else:
                print("Need 1 command line argument, Found:%d"%(l-1))
        elif command1 in ['upper','lower','reverse','palindrome','find_palin','encode',
                    'count_by_director','num_sequels','main_actor','count_by_actor','highest_rev']:
            if l==3:
                print(processCommands(command1,sys.argv[2]))
            else:
                print("Need 2 command line arguments, Found:%d"%(l-1))
        else:
            print("Invalid command")