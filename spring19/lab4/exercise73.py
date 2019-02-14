import math

def eval_loop():
    lastInput = ""
    while True:
        userInput = input("Give me some math!")
        if userInput == "done":
            return eval(lastInput)
        else:
            lastInput = userInput


print(eval_loop())
