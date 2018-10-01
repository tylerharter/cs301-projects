import project
import math, sys


# Function 0
# We have coded a function below that converts a string to uppercase or lowercase
def convertCase(original_string, case):
    if case == "Upper":
        converted_string = original_string.upper()
    elif case == "Lower":
        converted_string = original_string.lower()
    else:
        print("Unknown case, keeping string unchanged")
        converted_string = original_string
    return converted_string


# Function 1
# Write the reverseString(original_string) function here
# This function should return the reversed version of original_string
# For example, if original_string was equal to "mary", the function should return "yram"
# Note: You shouldn't use print in this function.
#def reverseString(original_string):


# Function 2
# Write the checkPalindrome(original_string) function here.
# This function should return True if original_string is a palindrome, otherwise False.
# Note: You shouldn't use print in this function.
# Hint: Use the function you have defined above!
#def checkPalindrome(original_string):

# Function 3
# Write the findPalindromeMovieName() function here
# This function should return the title of the movie in the dataset which is a palindrome.
# Note: There is only one such movie in the dataset!
# Note: You shouldn't use print in this function.
# Hint: Use the function you have defined above!
#def findPalindromeMovieName():


# Function 4
# Write the encodeString(original_string) function here
# Replace all 'A' and a' with '@', all 'O' and 'o' with '0' and all 'I' and 'i' with '!'
# This function should return the original_string, after encoding it
# Note: You shouldn't use print in this function.
#def encodeString(original_string):



# Function 5
# Write the countMoviesByDirector(director_name) function here
# Count the number of movies by the given director
# This function should return an integer, the number of movies released by director_name
# Note: You shouldn't use print in this function.
# Hint: For each movie in the dataset, check who was the director
#def countMoviesByDirector(director_name):


# Function 6
# Write the findSecondHighestRevenue(year) function here
# This function should return the revenue of the second largest grossing movie in the given year
# Note: You shouldn't use print in this function
# Hint: For each movie in the dataset, check when it was released and its revenue
# Hint: To find the second highest revenue, you may need to also keep track of the highest revenue!
#def findSecondHighestRevenue(year):




# Function 7
# Write the findKeyword(movie,genre) function here
# Step1: Retrieve the movie genres for the given movie (There may be more than one, separated by commas)
# Step2: Use string find function check if the genres has the desired genre
# Step3: If the genre is present then return "Yes", otherwise "No"
# Note: You shouldn't use print in this function.
#def findKeyword(movie,genre):


# Function 8
# Write the countGreaterThan(min_rating) function here
# Count the number of movies in the dataset with rating greater than or equal to min_rating
# Note: You shouldn't use print in this function.
#def countGreaterThan(min_rating):



# Function 9
# Write the mainActor(movie) function here
# Step1: Get the movie's cast by using our getMovieData function.
# Step2: Retrieve the main actor's name by slicing the string. The main actor is listed first.
# Step2: Return the string containing the main actor's name
# Note: You shouldn't use print in this function.
#def mainActor(movie):


# Function 10
# Write the findNumSequels() function here
# Find all movies in dataset which have a sequel called the name of the first movie followed by a 2
# eg. "Iron Man" and "Iron Man 2"
#def findNumSequels():


# Function 11
# Write the mainActor(movie) function here
# Step1: Get the movie's cast by using our getMovieData function.
# Step2: Retrieve the main actor's name by slicing the string. The main actor is listed first.
# Step2: Return the string containing the main actor's name
# Note: You shouldn't use print in this function.
#def processCommands(command1,command2):


def main(command1=None,command2=None):

    # In each of the below problems, edit only the print(0) statement.

    # Read and understand Function 0 which we have written for you above.
    # Use it in Problems 1 and 2
    print("Problem 1")
    print("The lowercase version of the string \"The Last Samurai\" is : ")
    print()
    print()

    print("Problem 2")
    print("The uppercase version of the string \"Fight Club\" is : ")
    print()
    print()

    # Practice reading data from the dataset
    # (read and understand the instructions in the readme file carefully)
    print("Problem 3")
    print("The director of \"La La Land\" is : ")
    print()
    print()

    print("Problem 4")
    print("\"Sherlock Holmes\" was released in : ")
    print()
    print()

    print("Problem 5")
    print("The cast of the movie ranked 320th in the dataset: ")
    print()
    print()

    # Make sure you complete writing Function 1
    print("Problem 6")
    print("Lets reverse the string \"madagascar\". The reversed string is : ")
    print()
    print()

    # Make sure you complete writing Function 2
    print("Problem 7")
    print("The string \"Spacecaps\" is a Palindrome ")
    print()
    print()

    # Make sure you complete writing Function 3
    print("Problem 8")
    print("A movie whose name is a palindrome in the given dataset is : ")
    print()
    print()

    # Make sure you complete writing Function 4
    print("Problem 9")
    print("Encoding the string \"Password Incorrect\" gives: ")
    print()
    print()

    # Make sure you complete writing Function 5
    print("Problem 10")
    print("The total number of movies in the dataset that are directed by Christopher Nolan are: ")
    print()
    print()

    # Make sure you complete writing Function 6
    print("Problem 11")
    print("The second-highest grossing movie of 2016 had a revenue of: ")
    print()
    print()

    # Make sure you complete writing Function 7
    print("Problem 12")
    print("Is \"The Prestige\" a \"Mystery\" movie? ")
    print()
    print()

    print("Problem 13")
    print("Is \"Kimi no na wa\" a \"Fantasy\" movie? ")
    print()
    print()

    # Make sure you complete writing Function 8
    print("Problem 14")
    print("The main actor in \"Black Swan\" is: ")
    print()
    print()

    print("Problem 15")
    print("The main actor in \"Inception\" is: ")
    print()
    print()

    print("Problem 16")
    print("Find number of movies in dataset which have a sequel called the name of the first movie followed by a 2 (eg. \"Iron Man\" and \"Iron Man 2\")")
    print()
    print()


    # DO NOT modify any of the code below this.
    # The below three problems are not graded, but they are for you to check if your function is working properly
    # Use the appropriate command line arguments to test your code!
    if command1=="describe":
        print("Problem 17")
        print("Use the command line argument describe to print the movie description of \"Arrival\"")
        print()

    if command1=="greater_than":
        print("Problem 18")
        print("Use the command line argument to count the number of movies with a minimum rating of 7.6")
        print()

    if command1=="count":
        print("Problem 19")
        print("Use the command line argument to count the number of movies directed by Ridley Scott")
        print()


if __name__ == "__main__":
    if len(sys.argv)>1:
        if len(sys.argv)!=3:
            print("Only 2 command line arguments allowed")
        else:
            command1 = sys.argv[1]
            command2 = sys.argv[2]
            if command1 not in ['describe','greater_than','count']:
                print("Invalid command")
            else:
                main(command1, command2)
    else:
        main()