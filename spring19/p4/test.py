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
What is the type of the following? 1.0 == 2.0
 a) int 
 b) float 
 c) str 
 d) bool 
 e) NoneType 

Your answer: d
Congratulations! You got it right.
The correct answer is d
What is the type of the following? "1" * 2
Your answer: str
Congratulations! You got it right.
The correct answer is str
What does this expression evaluate to? 
 True != (3 < 2)
Your answer: True
Sorry your answer was incorrect.
You have this many remaining tries: 0
The correct answer is True
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
