import project
import math

# Function 1
# Insert getMaximumLand(stateName1, stateName2, stateName3) function here
# Step1: Retrieve area values for all 3 states using getArea function and assign it to variables.
# Step2: Use max() function to calculate the max value and store it as a variable
# Step3: Return the max value that you calculated.
# Note: You shouldn't use print in this function.

# Function 2
# Insert getMinimumPopulationDensity(stateName1, stateName2, stateName3, year) function here
# Step1: Retrieve area and population values for all 3 states using getArea and the getPopulation function and assign it to variables.
# Step2: Use min() function to calculate the min value and store it as a variable
# Step3: Return the min value that you calculated.
# Note: You shouldn't use print in this function.

# Function 3
# Insert predictPopulation(stateName, yearA, yearB, growthRate = 0.1) function here
# Step 1: Using the statename retrieve the population for yearA
# Step 2: Calculate time between yearA and yearB
# Step 3: Use the math.exp() function in the given formula to calculate final population
# Step 4: Return the predicted final population
# Note: You shouldn't use print in this function.

# Function 4
# Insert calcGrowthRate(stateName, yearA, yearB) function here
# Step 1: Using the statename retrieve the population for yearA
# Step 1: Using the statename retrieve the population for yearB
# Step 2: Calculate time between yearA and yearB
# Step 3: Use the math.log() function in the given formula to calculate growth rate
# Step 4: Return the growth rate.
# Note: You shouldn't use print in this function.

def main():
    # Example state names. Please play around by changing the state names
    # Fix the main code so it will print the correct value

    # Problem 1
    # Read Area Data
    print('Problem 1')
    print("The area of Wisconsin is ")
    print(project.getArea("Wisconsin"))
    print()

    # Problem 2
    # Read Population Area
    # Fix the code below to print out the correct value
    print('Problem 2')
    print("The population of Wisconsin in 2010 is ")
    print(0)
    print()

    # Problem 3
    # Solving Q1: Finding max Area
    # Fix the code below to print out the correct value
    print('Problem 3')
    print("Maximum land area among Wisconsin, Iowa, Minnesota is ")
    print(0)
    print()

    # Problem 4
    # Solving Q2: Finding minimum Population Density
    # Fix the code below to print out the correct value
    print('Problem 4')
    print("Minimum population density among Wisconsin, Iowa, Minnesota is ")
    print(0)
    print()

    # Problem 5
    # Solving Q3: Finding final population
    # Fix the code below to print out the correct value
    print('Problem 5')
    print("The predicted population for Wisconsin in year 2010 is (assume start yearA is 2000, growth rate is 0.5) ")
    print(0)
    print()

    # Problem 6
    # Solving Q4: Calculating growth rate
    # Fix the code below to print out the correct value
    print('Problem 6')
    print("The growth rate for Wisconsin between year 2000 and 2010 is ")
    print(0)
    print()

if __name__ == "__main__":
    main()
