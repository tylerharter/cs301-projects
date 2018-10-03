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

PROMPT = 'enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: '

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
        if line.startswith(PROMPT):
            stdin.append(line[len(PROMPT):] + '\n')
            stdout.append(line[:len(PROMPT)] + '\n')
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
    stdin, stdout = split_stdin_stdout(expected)

    cmd = [PYTHON_BINARY, '-u', PROGRAM]
    print('Running your program with this command: ' + ' '.join(cmd) + '\n')
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
    actual_stdout = actual_stdout.replace(PROMPT, PROMPT + '\n')
    error = check_equal_stdout(stdout, actual_stdout)
    return error if error else PASS

def test_1():
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
added score
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
added score
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
55.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

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

def main():
    result = {'score': 0, 'tests': []}
    result['tests'] += runTests()

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
