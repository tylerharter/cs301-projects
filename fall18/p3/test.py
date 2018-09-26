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

def problem_1(actual_lines):
    return check_problem(actual_lines, [
        "The number of records in the DataSet is ",
        529
    ])

def problem_2(actual_lines):
    return check_problem(actual_lines, [
        "The name of the hurricane in the 20th row of the dataset is ",
        "BABE"
    ])

def problem_3(actual_lines):
    return check_problem(actual_lines, [
        "Does the hurricane 'BOB' Exist in the Dataset?",
        "True"
    ])

def problem_4(actual_lines):
    return check_problem(actual_lines, [
        "Does the hurricane 'BRITNEY' Exist in the Dataset?",
        "False"
    ])

def problem_5(actual_lines):
    return check_problem(actual_lines, [
        "Find the hurricane that came at 9.0N Latitude and 157.0W Longitude",
        "JUNE"
    ])

def problem_6(actual_lines):
    return check_problem(actual_lines, [
        "How many hurricanes came from the Pacific?",
        241
    ])

def problem_7(actual_lines):
    return check_problem(actual_lines, [
        "How many hurricanes came from the Atlantic?",
        288
    ])

def problem_8(actual_lines):
    return check_problem(actual_lines, [
        "What is the difference between the max Windspeed and min Windspeed of the dataSet?",
        65
    ])

##################################################
# Tests are based on calling student functions
##################################################

def test_1():
    error = check_has_function('testGetNumRecords')
    if error:
        return error
    expected = 529
    actual = MAIN.testGetNumRecords()
    return check_answer(expected, actual)

def test_2():
    error = check_has_function('testGetName')
    if error:
        return error
    actual = MAIN.testGetName(24)
    return check_answer(expected, actual)

def test_3():
    error = check_has_function('testGetWindSpeed')
    if error:
        return error
    expected = 25
    actual = MAIN.testGetWindSpeed(38)
    return check_answer(expected, actual)

def test_4():
    error = check_has_function('searchHurricane')
    if error:
        return error
    expected = True
    actual = MAIN.searchHurricane("EMILY")
    return check_answer(expected, actual)

def test_5():
    error = check_has_function('searchHurricane')
    if error:
        return error
    expected = False
    actual = MAIN.searchHurricane("Random1")
    return check_answer(expected, actual)

def test_6():
    error = check_has_function('searchHurricane')
    if error:
        return error
    expected = True
    actual = MAIN.searchHurricane("KENNETH")
    return check_answer(expected, actual)

def test_7():
    error = check_has_function('searchHurricane')
    if error:
        return error
    expected = False
    actual = MAIN.searchHurricane("BORA")
    return check_answer(expected, actual)

def test_8():
    error = check_has_function('searchHurricaneByLocation')
    if error:
        return error
    expected = "FAITH"
    actual = MAIN.searchHurricaneByLocation("12.9N", "20.5W")
    return check_answer(expected, actual)

def test_9():
    error = check_has_function('searchHurricaneByLocation')
    if error:
        return error
    expected = "HENRIETTE"
    actual = MAIN.searchHurricaneByLocation("11.2N","95.0W")
    return check_answer(expected, actual)

def test_10():
    error = check_has_function('countHurricane')
    if error:
        return error
    expected = 288
    actual = MAIN.countHurricane("Atlantic")
    return check_answer(expected, actual)

def test_12():
    error = check_has_function('countHurricane')
    if error:
        return error
    expected = 80
    actual = MAIN.maxWindSpeedHurricane()
    return check_answer(expected, actual)

def test_13():
    error = check_has_function('minWindSpeedHurricane')
    if error:
        return error
    expected = 15
    actual = MAIN.minWindSpeedHurricane()
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
