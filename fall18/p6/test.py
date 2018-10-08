#!/usr/bin/env python

import importlib
import json
import os
import subprocess
import sys
from inspect import getmembers, isfunction

PASS = 'PASS'
EPSILON = 0.0001
PROGRAM = "main.py"
# find student's code and import it as MAIN module
if not os.path.exists(PROGRAM):
    print("WARNING: could not find {}".format(PROGRAM))
    sys.exit()

MAIN = importlib.import_module('main')

##################################################
# Tests are based on calling student functions
##################################################

def test_1():
    """ tests results of read_csv """
    fp = open("sample.csv")
    # TODO write sample.csv
    fp.close()
    result = MAIN.read_csv("sample.csv")
    # TODO compare results and return score
    return check_answer(1, 1)

def check_python_version():
    # NOTE not using get_python_version since I'm importing the code into the
    # current interpreter
    version = sys.version.split()[0]
    if not version.startswith('3'):
        print("WARNING! Your Python version may not work for this class.")
        print("Please check with us about this.")

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

def get_fns(prefix):
    def is_test_fn(f):
        if not isfunction(f):
            return False

        if f.__module__ != __name__:
            return False

        if not f.__name__.startswith(prefix):
            return False

        return True

    fns = getmembers(sys.modules[__name__], predicate=is_test_fn)
    fns.sort(key=lambda x: int(x[0].split('_')[-1]))
    return fns

def check_has_function(function_name):
    for name, member in getmembers(MAIN):
        if name == function_name and isfunction(member):
            return None
    return 'missing function ' + function_name

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
        if type(e) is float or type(e) is int:
            try:
                answer = float(a)
                if abs(answer - e) < EPSILON:
                    continue
                else:
                    return 'expected ({}) but found ({})'.format(e, a)
            except:
                return 'expected ({}) but found ({})'.format(e, a)
        elif a.lower() != e.lower():
            return 'expected ({}) but found ({})'.format(e, a)
    return None

def check_problem(actual_lines, expected_lines):
    error = areLinesExpected(actual_lines, expected_lines)
    if error != None:
        return error
    return PASS

def getProblemAnswers():
    try:
        cmd = [PYTHON_BINARY, PROGRAM]
        print('Running your program with this command: ' + ' '.join(cmd) + '\n')
        output = subprocess.check_output(cmd)
    except Exception as e:
        print('Your Python program crashed.  Please fix it to get any points.')
        raise e

    problems = dict() # key:problem number, val: list of lines
    if output:
        # normalize windows => unix, as a string (not bytes)
        output = str(output, 'utf-8')
        output = output.replace('\r\n', '\n')

        # chuck output lines by problem
        problem_number = None
        for line in output.split('\n'):
            m = re.match(r'Problem (\d+)$', line)
            if m:
                problem_number = int(m.group(1))
                problems[problem_number] = []
            elif problem_number:
                problems[problem_number].append(line)

    return problems

def runTests():
    tests = []
    for name, fn in get_fns('test_'):
        try:
            result, weight = fn()
            tests.append({'test': name, 'result': result, 'weight': weight})
        except Exception as e:
            # TODO a message to run their main.py and test that function?
            raise e
    return tests

def runProblems():
    problems = getProblemAnswers()
    tests = []
    for name, fn in get_fns('problem_'):
        problem_num = int(name.split('_')[-1])
        output_lines = problems.get(problem_num, [])
        tests.append({'test': name, 'result': fn(output_lines)})
    return tests

def main():
    result = { 'score': 0, 'tests': [] }
    result['tests'] += runTests()
    result['tests'] += runProblems()

    # final score
    score = sum([t['weight'] for t in result['tests'] if t['result'] == PASS])
    total = sum([t['weight'] for t in result['tests']])
    if total != 100:
        print("WARNING: Weights add up to {} instead of 100".format(total))

    result['score'] = score
    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))

    print('RESULTS:')
    for test in result['tests']:
        print('   {} ({}%): {}'.format(test['test'], test['weight'], test['result']))

    print('Score: {}%%'.format(result['score']))

if __name__ == '__main__':
    check_python_version()
    main()
