#!/usr/bin/python
import subprocess, json, re, sys, importlib
from inspect import getmembers, isfunction

PASS = 'PASS'
EPSILON = 0.0001

# find student's code and import it as MAIN module
PROGRAM = 'main.py'
MODULE_NAME = 'main'
if len(sys.argv) == 2:
    PROGRAM = sys.argv[1]
    MODULE_NAME = PROGRAM.split('.')[0]
MAIN = importlib.import_module(MODULE_NAME)

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

##################################################
# Problems are based on output of student program
##################################################

##################################################
# Tests are based on calling student functions
##################################################

def test_1():
    error = check_has_function('convertCase')
    if error:
        return error
    expected = "LIBRARY"
    actual = MAIN.main("upper","library")
    return check_answer(expected, actual)

def test_2():
    error = check_has_function('reverseString')
    if error:
        return error
    expected = "kcul drah"
    actual = MAIN.main("reverse","hard luck")
    return check_answer(expected, actual)

def test_3():
    error = check_has_function('checkPalindrome')
    if error:
        return error
    expected = True
    actual = MAIN.main("palindrome,""Malayalam")
    return check_answer(expected, actual)

def test_4():
    error = check_has_function('checkPalindrome')
    if error:
        return error
    expected = False
    actual = MAIN.main("palindrome","Palindrome")
    return check_answer(expected, actual)

def test_5():
    error = check_has_function('findPalindromeMovie()')
    if error:
        return error
    expected = "Elle"
    actual = MAIN.main("find_palin")
    return check_answer(expected, actual)

def test_6():
    error = check_has_function('encodeString')
    if error:
        return error
    expected = "b@ll00ns"
    actual = MAIN.main("encode","balloons")
    return check_answer(expected, actual)

def test_7():
    error = check_has_function('encodeString')
    if error:
        return error
    expected = "!nt!m!d@t!0n"
    actual = MAIN.main("encode","intimidation")
    return check_answer(expected, actual)

def test_8():
    error = check_has_function('countMoviesByDirector')
    if error:
        return error
    expected = 1
    actual = MAIN.main("count_by_director","Adam Leon")
    return check_answer(expected, actual)

def test_9():
    error = check_has_function('findNumSequels')
    if error:
        return error
    expected = 8
    actual = MAIN.main("num_sequels")
    return check_answer(expected, actual)

def test_10():
    error = check_has_function('mainActor')
    if error:
        return error
    expected = "Noomi Rapace"
    actual = MAIN.main("main_actor","Prometheus")
    return check_answer(expected, actual)

def test_11():
    error = check_has_function('countMoviesByActor')
    if error:
        return error
    expected = 5
    actual = MAIN.main("count_by_actor","Noomi Rapace")
    return check_answer(expected, actual)

def test_12():
    error = check_has_function('findHighestRevenue')
    if error:
        return error
    expected = "The Avengers"
    actual = MAIN.processCommands("highest_rev", 2012)
    return check_answer(expected, actual)


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

# these call student functions
def runTests():
    tests = []
    predicate = lambda f: isfunction(f) and f.__module__ == __name__
    fns = [row for row in getmembers(sys.modules[__name__], predicate = predicate) if row[0].startswith('test_')]
    fns.sort(key=lambda row: int(row[0].split('_')[-1]))
    for name, fn in fns:
        try:
            result = fn()
            tests.append({'test': name, 'result': result})
        except Exception as e:
            print('\nTip from 301 instructors: try running just %s() in interactive mode to debug this issue.\n\n' % name)
            raise e
    return tests

# these check output from running student program
def runProblems():
    # collect main() output from student
    problems = getProblemAnswers()
    tests = []

    predicate = lambda f: isfunction(f) and f.__module__ == __name__
    fns = [row for row in getmembers(sys.modules[__name__], predicate = predicate) if row[0].startswith('problem_')]
    fns.sort(key=lambda row: int(row[0].split('_')[-1]))
    for name, fn in fns:
        problem_num = int(name.split('_')[-1])
        output_lines = problems.get(problem_num, [])
        tests.append({'test': name, 'result': fn(output_lines)})
    return tests

def main():
    result = {'score': 0, 'tests': []}
    result['tests'] += runTests()
    result['tests'] += runProblems()

    # final score
    passing = [t for t in result['tests'] if t['result'] == PASS]
    result['score'] = len(passing) * 100 // len(result['tests'])

    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
    print('RESULTS:')
    for test in result['tests']:
        print('  {}: {}'.format(test['test'], test['result']))
    print('Score: %d%%' % result['score'])

if __name__ == '__main__':
    main()
