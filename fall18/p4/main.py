import project
import sys


# We have coded a function below that converts a string to uppercase or lowercase
def convertCase(original_string, case):
    if case == "upper":
        converted_string = original_string.upper()
    elif case == "lower":
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


# Write the countMoviesByActor(actor_name) function here
# Note: You shouldn't use print in this function. 


# Write the findHighestRevenue(year) function here
# Note: You shouldn't use print in this function


def main(command1, command2):
    
    # Code for when the first command line argument is "upper"
    if command1=="upper":
        print(convertCase(command2,"upper"))

    # Write an if block similar to the above for the command "lower"

    # Let's get familiar with the IMBB dataset
    # Write an if block for the command "describe"








# DO NOT modify any of the code below this.
if __name__ == "__main__":
    l = len(sys.argv)
    if l<=1:
        print("No command line arguments found")
    else:
        command1 = sys.argv[1]
    
        if command1 in ['find_palin','num_sequels']:
            if l==2:
                main(command1,None)
            else:
                print("Need 1 command line argument, Found:%d"%(l-1))
        elif command1 in ['upper','lower','reverse','palindrome','find_palin','encode',
                    'count_by_director','num_sequels','main_actor','count_by_actor','highest_rev']:
            if l==3:
                main(command1,sys.argv[2])
            else:
                print("Need 2 command line arguments, Found:%d"%(l-1))
        else:
            print("Invalid command")