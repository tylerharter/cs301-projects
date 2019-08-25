n = 13
print("This game is called Take-Away!")
print("There are {} dollars and one exclamation mark.".format(n-1))
print("The goal is to take dollars but not take the '!'.")
print("You and the computer will take turns taking between 1 and 3 dollars.")
print("If there are no dollars left and you take the '!', you lose.")
print("You start:")

def show_state():
    print("Status: " + "$"*(n-1) + "! (%d remaining)" % n)

while True:
    show_state()

    # input
    choice = input("choose between 1 and 3 (or type 'q' to quit): ")
    if choice.strip() == "q":
        print("quiting early")
        break
    choice = int(choice)
    assert(1 <= choice <= 3)

    # human play
    n -= choice
    if n <= 0:
        print("You took the '!' and lost.")
        break
    show_state()

    # computer play
    choice = 4 - choice
    print("program takes {}".format(choice))
    n -= choice
    if n <= 0:
        print("Program took the '!' and lost.")
        break
