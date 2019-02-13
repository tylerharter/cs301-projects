# Project 5

## Corrections

## Description

The CS 301 midterm is coming up, so now is a good time to begin to study. A great resource for preparing is to look at the old midterm exam which is available [here](https://github.com/tylerharter/caraza-harter-com/tree/master/tyler/cs301/spring19/materials/old-exams). Since we've been learning about conditionals this week, for this project we'll build an automated study tool program to quiz you on the questions. You'll get practice with conditionals and while loops.

Start by downloading `test.py`. Double check that these files don't get renamed by your browser (by running `ls` in the terminal from your `p4` project directory). You'll do all your work in a new `main.ipynb` notebook that you'll create and hand in when you're done.  You'll test as usual by running `python test.py`.

The lab this week is designed to give you practice with conditionals and while loops, so be sure to do the lab from home (if you missed it) before starting the project.

The project consists of writing code to create an interactive quiz program. We've broken the program down into 10 features you can add one at a time.

Note: This project does not provide you a project.py (you won't be needing it) or a main.py to start from (you can start from scratch). You should hand in main.py file when you are done.


## Requirements

## Questions and Functions

### Feature 1: Ask a question, get an answer

Ask the user:

```
What is the type of the following? 1.0 + 2.0
a. int
b. float
c. str
d. bool
e. NoneType
```
After they have entered input, print out this line:
```
You answered 'a'. The correct answer is 'b'.
```
Where 'a' is whatever the user typed in and 'b' is whatever letter is the right answer.

Be sure the spaces and capitalization is correct to pass this test.

### Feature 2: Check the answer for correctness
Use an If statement to check to see if the answer is correct. If it is, print:
```
Congratulations! You got it right.
```

### Feature 3: Clean the input on text
You may have noticed that if the user inputs a correct answer, but it's capitalization isn't right or it has extra spaces, then Feature 2 will think it's a wrong answer.

Take the user's input and remove any spaces or capitalization using the str.strip() and str.lower() built in functions.

### Feature 4: Tell user when answer is wrong

Use an 'ELSE' statement to tell a user that their answer is wrong:

```
Sorry your answer was incorrect.
```
This should be printed on the line before the text from Feature 2.

### Feature 5: Ask a fill in the blank question
Add this as question 2:

```
What is the type of the following?
"1" * 2
```
Notice there are no multiple choices here!

### Feature 6: Make a function to ask the Questions

Notice how you have had to repeat code to ask question 1 and 2. Let's consolidate this into a function named askQuestion which has 2 parameters, one for the question and one for the answer. Use this function to ask both question 1 and question 2 from the global block.

### Feature 7: Add another question

Add this as question 3:

```
What does this expression evaluate to?
TRUE != (3 < 2)
```
All three questions should use the askQuestion function which is called from the global block.

### Feature 8: Give three tries

Use a 'while' loop to give the user three tries to get the answer right.

If they get it right, they should still see the Feature 2 ("Congratulations!") text.

If they get it wrong, they should see the Feature 4 ("Sorry your answer was incorrect") text, and then on a new line
```
Try again! You have 2 more tries
```
Where the number is the correct number of tries left. They should see the Feature 1 text once they either get it right or use up all 3 tries.

### Feature 9: Give a Hint

Use an Elif to check to see if they are on their last try. If so, give them a hint. You can write the hint text. The hint text will have to be added as another parameter for the AskQuestion function.

Set the default value of the hint parameter to be "Check the textbook".

Add hint text for each of the three questions.

### Feature 10: Keep Score

Use global variables to track the number of questions they have gotten right and how many they have gotten wrong.

After all questions have been asked, print out:
```
You tried 3 questions and got 2 right.
```
Display the correct numbers of right and wrong.
