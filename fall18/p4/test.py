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
        "The lowercase version of the string \"The Last Samurai\" is : ",
        "the last samurai"
    ])

def problem_2(actual_lines):
    return check_problem(actual_lines, [
        "The uppercase version of the string \"Fight Club\" is : ",
        "FIGHT CLUB"
    ])

def problem_3(actual_lines):
    return check_problem(actual_lines, [
        "The director of \"La La Land\" is : ",
        "Damien Chazelle"
    ])

def problem_4(actual_lines):
    return check_problem(actual_lines, [
        "\"Sherlock Holmes\" was released in : ",
        2009
    ])

def problem_5(actual_lines):
    return check_problem(actual_lines, [
        "The cast of the movie ranked 320th in the dataset: ",
        "Channing Tatum, Jenna Dewan Tatum, Damaine Radcliff, De\'Shawn Washington"
    ])

def problem_6(actual_lines):
    return check_problem(actual_lines, [
        "Lets reverse the string \"madagascar\". The reversed string is : ",
        "racsagadam"
    ])

def problem_7(actual_lines):
    return check_problem(actual_lines, [
        "The string \"Spacecaps\" is a Palindrome ",
        "True"
    ])

def problem_8(actual_lines):
    return check_problem(actual_lines, [
        "A movie whose name is a palindrome in the given dataset is : ",
        "Elle"
    ])

def problem_9(actual_lines):
    return check_problem(actual_lines, [
        "Encoding the string \"Password Incorrect\" gives: ",
        "P@ssw0rd !nc0rrect"
    ])

def problem_10(actual_lines):
    return check_problem(actual_lines, [
        "The total number of movies in the dataset that are directed by Christopher Nolan are: ",
        5
    ])

def problem_11(actual_lines):
    return check_problem(actual_lines, [
        "The second-highest grossing movie of 2016 had a revenue of: ",
        486.29
    ])

def problem_12(actual_lines):
    return check_problem(actual_lines, [
        "Is \"The Prestige\" a \"Mystery\" movie? ",
        "Yes"
    ])

def problem_13(actual_lines):
    return check_problem(actual_lines, [
        "Is \"Kimi no na wa\" a \"Fantasy\" movie?",
        "Yes"
    ])

def problem_14(actual_lines):
    return check_problem(actual_lines, [
        "The main actor in \"Black Swan\" is:",
        "Natalie Portman"
    ])

def problem_15(actual_lines):
    return check_problem(actual_lines, [
        "The main actor in \"Inception\" is:",
        "Leonardo DiCaprio"
    ])

def problem_16(actual_lines):
    return check_problem(actual_lines, [
        "Find number of movies in dataset which have a sequel called the name of the first movie followed by a 2 (eg. \"Iron Man\" and \"Iron Man 2\")",
        14
    ])



##################################################
# Tests are based on calling student functions
##################################################

def test_1():
    error = check_has_function('reverseString')
    if error:
        return error
    expected = "yrarbil"
    actual = MAIN.reverseString("library")
    return check_answer(expected, actual)

def test_2():
    error = check_has_function('reverseString')
    if error:
        return error
    expected = "kcul drah"
    actual = MAIN.reverseString("hard luck")
    return check_answer(expected, actual)

def test_3():
    error = check_has_function('checkPalindrome')
    if error:
        return error
    expected = True
    actual = MAIN.checkPalindrome("Malayalam")
    return check_answer(expected, actual)

def test_4():
    error = check_has_function('checkPalindrome')
    if error:
        return error
    expected = False
    actual = MAIN.checkPalindrome("Palindrome")
    return check_answer(expected, actual)

def test_5():
    error = check_has_function('encodeString')
    if error:
        return error
    expected = "b@ll00ns"
    actual = MAIN.encodeString("balloons")
    return check_answer(expected, actual)

def test_6():
    error = check_has_function('countMoviesByDirector')
    if error:
        return error
    expected = 1
    actual = MAIN.countMoviesByDirector("Adam Leon")
    return check_answer(expected, actual)

def test_7():
    error = check_has_function('findKeyword')
    if error:
        return error
    expected = 'Yes'
    actual = MAIN.findKeyword("Maudie","Biography")
    return check_answer(expected, actual)

def test_8():
    error = check_has_function('processCommands')
    if error:
        return error
    expected = 195
    actual = MAIN.processCommands("greater_than","7.6")
    return check_answer(expected, actual)

def test_9():
    error = check_has_function('processCommands')
    if error:
        return error
    expected = "An arthritic Nova Scotia woman works as a housekeeper while she hones her skills as an artist and eventually becomes a beloved figure in the community."
    actual = MAIN.processCommands("describe","Maudie")
    return check_answer(expected, actual)

def test_10():
    error = check_has_function('processCommands')
    if error:
        return error
    expected = 4
    actual = MAIN.processCommands("count", "Steven Spielberg")
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
