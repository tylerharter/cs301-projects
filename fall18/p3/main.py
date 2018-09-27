import project

# my-login: YOUR-NETID
# partner-login: PARTNER-NETID

# TODO: finish this function
def searchHurricane(name):
    # create an index variable, starting at 0

    while False: # stopping condition, this will currently not loop, fix it
        pass # this is a placeholder for an empty loop, so delete it

        # use the project.getName function to check if the hurricane
        # at the current index is the one we're looking for and if so
        # return True

        # increment your index
    return None  # fix this


# TODO: define searchHurricaneByLocation(latitude, longitude)


# TODO: define countHurricane(oceanName)


# TODO: define maxWindSpeedHurricane()


# TODO: define minWindSpeedHurricane()


def main():
    # For problems 1 to 4, you need not define any functions
    # but instead you just need to use the helper functions
    # that we have written for you in the file project.py
    print("\nProblem 1")
    print("The number of records in the dataset is ")
    print() # answer here

    print("\nProblem 2")
    print("The name of the hurricane at index 0 is ")
    print() # answer here

    print("\nProblem 3")
    print("The name of the hurricane at index 1 is ")
    print() # answer here

    print("\nProblem 4")
    print("The name of the hurricane at index 19 is ")
    print() # answer here

    # For problems 5 to 10 below, you should first define
    # the functions given at the top of this file and call
    # the corresponding function for each problem as needed.

    # For example, you should first define the method named
    # searchHurricane(name) and then call that method inside
    # the print statement below (that says # answer here) to
    # solve problem 5.
    print("\nProblem 5")
    print("Does the hurricane 'BOB' exist in the dataset?")
    print() # answer here
    
    print("\nProblem 6")
    print("Does the hurricane 'BRITNEY' exist in the dataset?")
    print() # answer here
    
    print("\nProblem 7")
    print("Find the hurricane that came at 9.0N Latitude and 157.0W Longitude")
    print() # answer here
    
    print("\nProblem 8")
    print("How many hurricanes came from the Pacific?")
    print() # answer here
    
    print("\nProblem 9")
    print("How many hurricanes came from the Atlantic?")
    print() # answer here
    
    print("\nProblem 10")
    print("What is the difference between the max wind speed and min wind speed of the dataset?")
    print() # answer here


if __name__ == '__main__':
    main()    
