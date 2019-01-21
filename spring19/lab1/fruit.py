fruits = ['apple', 'banana', 'pineapple', 'mango', 'orange', 'kiwi']
print("Fruits:")
print("\n".join(fruits) + "\n")
idx = int(input("Enter a number between 0 and " + str(len(fruits) - 1) + ": "))
print("You chose " + fruits[idx])
