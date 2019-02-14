#!/usr/bin/python
import subprocess, json, re, sys, importlib
from inspect import getmembers, isfunction

PASS = 'PASS'
EPSILON = 0.0001

PROGRAM = 'main.py'
if len(sys.argv) == 2:
    PROGRAM = sys.argv[1]

PROMPTS = [
    "How many tries do you want for each question: ",
    "Your answer: "
]

# find python binary
def get_python_binary_name():
    try:
        subprocess.check_output(['python3', '--version'], stderr=subprocess.STDOUT)
        return 'python3'
    except:
        return 'python'

def get_python_version(python_binary):
    try:
        output = subprocess.check_output([python_binary, '--version'],
                                         stderr=subprocess.STDOUT)
        output = str(output, 'utf-8')
    except:
        return 'unknown'
    return output

PYTHON_BINARY = get_python_binary_name()
PYTHON_VERSION = get_python_version(PYTHON_BINARY)
print('Your Python version: '+PYTHON_VERSION)

if PYTHON_VERSION.lower().find('python 3') < 0:
    print('WARNING! Your Python version may not work for this class.')
    print('Please check with us about this.')
    print()

def split_stdin_stdout(expected):
    stdin = []
    stdout = []
    for line in expected.split('\n'):
        line = line.lstrip()
        for prompt in PROMPTS:
            if line.startswith(prompt):
                stdin.append(line[len(prompt):] + '\n')
                stdout.append(line[:len(prompt)] + '\n')
                break
        else:
            stdout.append(line + '\n')
    return ''.join(stdin), ''.join(stdout)

def check_equal_stdout(expected_stdout, actual_stdout):
    expected = [line.strip() for line in expected_stdout.split('\n') if line.strip()]
    actual = [line.strip() for line in actual_stdout.split('\n') if line.strip()]
    return areLinesExpected(actual, expected)

##################################################
# Tests
##################################################

def generic_test(expected):
    print('Expected Behavior:')
    print(expected)
    stdin, stdout = split_stdin_stdout(expected)

    cmd = [PYTHON_BINARY, '-u', PROGRAM]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

    try:
        actual_stdout, actual_stderr = p.communicate(bytes(stdin+'\n', 'utf-8'), timeout=1)
    except subprocess.TimeoutExpired:
        p.kill()
        return 'program timed out after 1 second'
    actual_stderr = str(actual_stderr, 'utf-8')
    if actual_stderr != '':
        print('program produced stderr: "%s"' % actual_stderr)
        return False

    actual_stdout = str(actual_stdout, 'utf-8')
    for prompt in PROMPTS:
        actual_stdout = actual_stdout.replace(prompt, prompt + '\n')
    error = check_equal_stdout(stdout, actual_stdout)
    return error if error else PASS



def test_1():
    print('TEST 1')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_2():
    print('TEST 2')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_3():
    print('TEST 3')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_4():
    print('TEST 4')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     str    

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   True  

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_5():
    print('TEST 5')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_6():
    print('TEST 6')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_7():
    print('TEST 7')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_8():
    print('TEST 8')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_9():
    print('TEST 9')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_10():
    print('TEST 10')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_11():
    print('TEST 11')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_12():
    print('TEST 12')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_13():
    print('TEST 13')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_14():
    print('TEST 14')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_15():
    print('TEST 15')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_16():
    print('TEST 16')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_17():
    print('TEST 17')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_18():
    print('TEST 18')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_19():
    print('TEST 19')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_20():
    print('TEST 20')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_21():
    print('TEST 21')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_22():
    print('TEST 22')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_23():
    print('TEST 23')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_24():
    print('TEST 24')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_25():
    print('TEST 25')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_26():
    print('TEST 26')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_27():
    print('TEST 27')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 0 right.
'''.strip())


def test_28():
    print('TEST 28')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_29():
    print('TEST 29')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_30():
    print('TEST 30')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_31():
    print('TEST 31')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_32():
    print('TEST 32')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_33():
    print('TEST 33')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_34():
    print('TEST 34')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_35():
    print('TEST 35')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_36():
    print('TEST 36')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_37():
    print('TEST 37')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_38():
    print('TEST 38')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_39():
    print('TEST 39')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_40():
    print('TEST 40')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_41():
    print('TEST 41')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_42():
    print('TEST 42')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_43():
    print('TEST 43')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_44():
    print('TEST 44')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_45():
    print('TEST 45')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_46():
    print('TEST 46')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_47():
    print('TEST 47')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_48():
    print('TEST 48')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 0 right.
'''.strip())


def test_49():
    print('TEST 49')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_50():
    print('TEST 50')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_51():
    print('TEST 51')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 1 right.
'''.strip())


def test_52():
    print('TEST 52')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_53():
    print('TEST 53')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_54():
    print('TEST 54')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_55():
    print('TEST 55')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_56():
    print('TEST 56')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_57():
    print('TEST 57')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: none

You answered 'none'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 0 right.
'''.strip())


def test_58():
    print('TEST 58')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_59():
    print('TEST 59')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_60():
    print('TEST 60')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_61():
    print('TEST 61')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_62():
    print('TEST 62')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: true

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_63():
    print('TEST 63')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: FLOAT

You answered 'FLOAT'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_64():
    print('TEST 64')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_65():
    print('TEST 65')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_66():
    print('TEST 66')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: B

You answered 'B'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_67():
    print('TEST 67')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: FLOAT

You answered 'FLOAT'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_68():
    print('TEST 68')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: B

You answered 'B'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_69():
    print('TEST 69')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: B

You answered 'B'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_70():
    print('TEST 70')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: BOOL

You answered 'BOOL'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_71():
    print('TEST 71')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: C

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: STR

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: TRUE

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_72():
    print('TEST 72')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     str    

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   0  

You answered '  0  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_73():
    print('TEST 73')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     str    

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   True  

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_74():
    print('TEST 74')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     str    

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   True  

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_75():
    print('TEST 75')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     float    

You answered '    float    '. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   False  

You answered '  False  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_76():
    print('TEST 76')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       a      

You answered '      a      '. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer:     str    

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   False  

You answered '  False  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_77():
    print('TEST 77')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     int    

You answered '    int    '. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   True  

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_78():
    print('TEST 78')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     bool    

You answered '    bool    '. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   0  

You answered '  0  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_79():
    print('TEST 79')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     int    

You answered '    int    '. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   None  

You answered '  None  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_80():
    print('TEST 80')
    return generic_test('''
How many tries do you want for each question:       1      

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer:       c      

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer:     float    

You answered '    float    '. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer:   None  

You answered '  None  '. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_81():
    print('TEST 81')
    return generic_test('''
How many tries do you want for each question: 1

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_82():
    print('TEST 82')
    return generic_test('''
How many tries do you want for each question: 2

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_83():
    print('TEST 83')
    return generic_test('''
How many tries do you want for each question: 3

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_84():
    print('TEST 84')
    return generic_test('''
How many tries do you want for each question: 4

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_85():
    print('TEST 85')
    return generic_test('''
How many tries do you want for each question: 5

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_86():
    print('TEST 86')
    return generic_test('''
How many tries do you want for each question: 6

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_87():
    print('TEST 87')
    return generic_test('''
How many tries do you want for each question: 7

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_88():
    print('TEST 88')
    return generic_test('''
How many tries do you want for each question: 8

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_89():
    print('TEST 89')
    return generic_test('''
How many tries do you want for each question: 9

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_90():
    print('TEST 90')
    return generic_test('''
How many tries do you want for each question: 10

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_91():
    print('TEST 91')
    return generic_test('''
How many tries do you want for each question: 2

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: c

notice the quotes!
You have this many remaining tries: 1
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: float

Calcuate the right side first. Don't forget != means not equal to.
You have this many remaining tries: 1
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_92():
    print('TEST 92')
    return generic_test('''
How many tries do you want for each question: 2

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

notice the quotes!
You have this many remaining tries: 1
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

Calcuate the right side first. Don't forget != means not equal to.
You have this many remaining tries: 1
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_93():
    print('TEST 93')
    return generic_test('''
How many tries do you want for each question: 2

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

Check the textbook
You have this many remaining tries: 1
Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

Calcuate the right side first. Don't forget != means not equal to.
You have this many remaining tries: 1
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 2 right.
'''.strip())


def test_94():
    print('TEST 94')
    return generic_test('''
How many tries do you want for each question: 3

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: float

notice the quotes!
You have this many remaining tries: 1
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 2
Your answer: 0

Calcuate the right side first. Don't forget != means not equal to.
You have this many remaining tries: 1
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_95():
    print('TEST 95')
    return generic_test('''
How many tries do you want for each question: 3

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_96():
    print('TEST 96')
    return generic_test('''
How many tries do you want for each question: 3

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: bool

notice the quotes!
You have this many remaining tries: 1
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 2
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_97():
    print('TEST 97')
    return generic_test('''
How many tries do you want for each question: 10

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 9
Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: c

You answered 'c'. The correct answer is 'str'.
You have this many remaining tries: 9
Your answer: c

You answered 'c'. The correct answer is 'str'.
You have this many remaining tries: 8
Your answer: e

You answered 'e'. The correct answer is 'str'.
You have this many remaining tries: 7
Your answer: c

You answered 'c'. The correct answer is 'str'.
You have this many remaining tries: 6
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 5
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 4
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 3
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: int

notice the quotes!
You have this many remaining tries: 1
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: int

You answered 'int'. The correct answer is 'True'.
You have this many remaining tries: 9
Your answer: bool

You answered 'bool'. The correct answer is 'True'.
You have this many remaining tries: 8
Your answer: str

You answered 'str'. The correct answer is 'True'.
You have this many remaining tries: 7
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 6
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 5
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 4
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 3
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())


def test_98():
    print('TEST 98')
    return generic_test('''
How many tries do you want for each question: 10

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 9
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 8
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 7
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 6
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 5
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 4
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 3
Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 9
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 8
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 7
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 6
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 5
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 9
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 8
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 3 right.
'''.strip())


def test_99():
    print('TEST 99')
    return generic_test('''
How many tries do you want for each question: 10

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 9
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 8
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 7
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 6
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 5
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 4
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 3
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 2
Your answer: e

Check the textbook
You have this many remaining tries: 1
Your answer: c

Congratulations! You got it right.

What is the type of the following? "1" * 2
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 9
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 8
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 7
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 6
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 5
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 4
Your answer: int

You answered 'int'. The correct answer is 'str'.
You have this many remaining tries: 3
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: bool

notice the quotes!
You have this many remaining tries: 1
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 0

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 9
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 8
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 7
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 6
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 5
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 4
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 3
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 2
Your answer: 0

Calcuate the right side first. Don't forget != means not equal to.
You have this many remaining tries: 1
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 0
You tried 3 questions and got 1 right.
'''.strip())


def test_100():
    print('TEST 100')
    return generic_test('''
How many tries do you want for each question: 10

What is the type of the following? "1.0" + "2.0"
 a) int 
 b) float 
 c) str 
 d) bool
 e) NoneType

Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 9
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 8
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 7
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 6
Your answer: e

You answered 'e'. The correct answer is 'c'.
You have this many remaining tries: 5
Your answer: a

You answered 'a'. The correct answer is 'c'.
You have this many remaining tries: 4
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 3
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 2
Your answer: e

Check the textbook
You have this many remaining tries: 1
Your answer: b

You answered 'b'. The correct answer is 'c'.
You have this many remaining tries: 0

What is the type of the following? "1" * 2
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 9
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 8
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 7
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 6
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 5
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 4
Your answer: bool

You answered 'bool'. The correct answer is 'str'.
You have this many remaining tries: 3
Your answer: float

You answered 'float'. The correct answer is 'str'.
You have this many remaining tries: 2
Your answer: str

Congratulations! You got it right.

What does this expression evaluate to? 
 True != (3 < 2)
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 9
Your answer: None

You answered 'None'. The correct answer is 'True'.
You have this many remaining tries: 8
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 7
Your answer: 1

You answered '1'. The correct answer is 'True'.
You have this many remaining tries: 6
Your answer: 0

You answered '0'. The correct answer is 'True'.
You have this many remaining tries: 5
Your answer: False

You answered 'False'. The correct answer is 'True'.
You have this many remaining tries: 4
Your answer: True

Congratulations! You got it right.
You tried 3 questions and got 2 right.
'''.strip())






def check_answer(expected, actual):
    if expected == actual:
        return PASS
    else:
        return 'expecting %s, but got %s' % (repr(expected), repr(actual))

def clean_lines(lines):
    result = []
    for l in lines:
        if type(l) is str and l.strip() != '':
            result.append(l.strip())
        elif type(l) is int or type(l) is float:
            result.append(l)
    return result

# ignore whitespace and case
def areLinesExpected(actual_lines, expected_lines):
    actual_lines = clean_lines(actual_lines)
    expected_lines = clean_lines(expected_lines)

    if len(actual_lines) < len(expected_lines):
        return 'fewer output lines than expected'
    if len(actual_lines) > len(expected_lines):
        return 'more output lines than expected'
    for a, e in zip(actual_lines, expected_lines):
        if a.lower() != e.lower():
            return 'expected ({}) but found ({})'.format(e, a)
    return None

def check_problem(actual_lines, expected_lines):
    error = areLinesExpected(actual_lines, expected_lines)
    if error != None:
        return error
    return PASS

# these call student functions
def runTests():
    tests = []
    predicate = lambda f: isfunction(f) and f.__module__ == __name__
    fns = [row for row in getmembers(sys.modules[__name__], predicate = predicate) if row[0].startswith('test_')]
    fns.sort(key=lambda row: int(row[0].split('_')[-1]))
    for name, fn in fns:
        try:
            print('='*40)
            result = fn()
            print('\nRESULT: %s\n' % result)
            tests.append({'test': name, 'result': result})
        except Exception as e:
            print('\nTip from 301 instructors: try running just %s() in interactive mode to debug this issue.\n\n' % name)
            raise e
    return tests

def main():
    result = {'score': 0, 'tests': []}
    result['tests'] += runTests()

    # final score
    passing = [t for t in result['tests'] if t['result'] == PASS]
    result['score'] = len(passing) * 100 / len(result['tests'])

    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
    print('RESULTS:')
    for test in result['tests']:
        print('  {}: {}'.format(test['test'], test['result']))
    print('Score: %.1f%%' % result['score'])

if __name__ == '__main__':
    main()
