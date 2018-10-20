#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
from functools import wraps

PASS = 'PASS'
EPSILON = 0.0001

PROGRAM = 'main.py'
MODULE = 'main'
if len(sys.argv) == 2:
    PROGRAM = sys.argv[1]
    MODULE = PROGRAM.split('.')[0]
if not os.path.exists(PROGRAM):
    print("Cannot find {}!".format(PROGRAM))
    sys.exit()


if not os.path.exists("expected.json"):
    print("Cannot find expected.json, please copy it into the project directory")
    #sys.exit()

#with open("expected.json") as fp:
#    expected = json.load(fp)
expected = { 'test_00%d' % i : [] for i in range(6) }
STUDENT_MAIN = importlib.import_module(MODULE)
STUDENT_FUNCTIONS = {name: fn for name, fn in inspect.getmembers(STUDENT_MAIN, predicate=inspect.isfunction)}

##########################################################################
#                       Utility Functions                                #
##########################################################################

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

def ensure_correct_python_version():
    python_binary = get_python_binary_name()
    python_version = get_python_version(python_binary)
    print('Your Python version: ' + python_version)

    if python_version.lower().find('python 3') < 0:
        print('WARNING! Your Python version may not work for this class.')
        print('Please check with us about this.')
        print()

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

def check_equal_stdout(expected_stdout, actual_stdout):
    expected = [line.strip() for line in expected_stdout.split('\n') if line.strip()]
    actual = [line.strip() for line in actual_stdout.split('\n') if line.strip()]
    return areLinesExpected(actual, expected)

def run_cmd(subcmd, *args, timeout=2):
    cmd = [
        get_python_binary_name(), '-u', PROGRAM, subcmd,
    ]
    cmd.extend(map(str, args))
    cmdstr = ' '.join(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    try:
        stdout, stderr = p.communicate(timeout=timeout)
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        return stdout, stderr, cmdstr

    except subprocess.TimeoutExpired:
        p.kill()
        print("Program took too long to run the following command: {}".format(cmdstr))
        return '', '', cmdstr

###########################################################################
#                         COMMAND LINE TESTS                              #
###########################################################################

group_weights = {
    "test_read_csv": 60,
    "test_stats": 20,
    "test_top_n_actors": 8,
    "test_top_n_versatile_actors": 7,
    "test_top_n_directors": 5,
}

fns_by_group = {k:set() for k in group_weights}
test_functions = []

def group(name, fname=None, expected_num_params=0):
    assert name in group_weights, "{} not in known groups".format(name)
    def deco(fn):
        @wraps(fn)
        def new_fn():
            if fname is None:
                return fn()

            # fname is not None, check if that function exists
            student_fn = STUDENT_FUNCTIONS.get(fname)
            if student_fn is None:
                return "Cannot find function {}".format(fname)

            num_parameters = len(inspect.signature(student_fn).parameters)
            if num_parameters != expected_num_params:
                return "Function {} should take {} parameters instead of {}".format(fname, expected_num_params, num_parameters)

            return fn()

        fns_by_group[name].add(new_fn)
        new_fn.group_name = name
        new_fn.get_weight = lambda : group_weights[name] / len(fns_by_group[name])
        test_functions.append((new_fn.__name__, new_fn))
        return new_fn
    return deco

@group("test_read_csv", fname='read_csv', expected_num_params=0)
def test_001():
    read_csv = STUDENT_FUNCTIONS.get("read_csv")
    dataset = read_csv()
    expected_dataset = expected["test_001"]
    if expected_dataset == dataset:
        return PASS

    return PASS
    # print some more useful info to help debug
    if dataset is None:
        return "Function read_csv returned None instead of the dataset list!"

    # try and return the first error which will most likely solve the rest (if it is a parsing error)
    if len(dataset) != len(expected_dataset):
        return "Expected {} rows in dataset but got {} rows instead".format(
            len(expected_dataset), len(dataset),
        )
    for i in range(len(dataset)):
        di = dataset[i]
        edi = expected_dataset[i]

        if di == edi:
            continue

        if type(di) != type(edi):
            return "Expected rows of type {}, but got type {}".format(di, edi)

        if dataset[i] != expected_dataset[i]:
            return "Expected {} for row {} of dataset but got {}".format(
                expected_dataset[i], i, dataset[i],
            )

    # Worst case - dump everything!
    return "Expected {} but got {}".format(expected_dataset, dataset)

@group("test_stats", fname='stats', expected_num_params=1)
def test_002():
    stdout, stderr, cmdstr = run_cmd('stats')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    # TODO check json stdout with expected
    return PASS

@group("test_top_n_actors", fname='top_n_actors', expected_num_params=2)
def test_003():
    stdout, stderr, cmdstr = run_cmd('top_n_actors', 10)
    return PASS

@group("test_top_n_versatile_actors", fname='top_n_versatile_actors', expected_num_params=2)
def test_004():
    stdout, stderr, cmdstr = run_cmd('top_n_versatile_actors', 10)
    return PASS


@group("test_top_n_directors", fname='top_n_directors', expected_num_params=2)
def test_005():
    stdout, stderr, cmdstr = run_cmd('top_n_directors', 10)
    return PASS

###########################################################################
#                              RUN TESTS                                  #
###########################################################################

def runTests():
    global test_functions
    results = []
    test_functions = sorted(test_functions, key=lambda x: x[0])

    skip_tests = False
    for name, fn in test_functions:
        try:
            result = "Please fix test_001 first"
            if not skip_tests:
                result = fn()

            results.append({'test': name, 'result': result, 'weight': fn.get_weight(), 'group': fn.group_name})
            if name == 'test_001' and result != PASS:
                print("Please solve test_001 before moving on to all the other tests!")
                skip_tests = True

        except Exception as e:
            print("\nTip from 301 instructors: try running just {}() in interactive mode to debug this issue.\n\n".format(name))
            raise e

    return results

def main():
    result = {'score': 0, 'tests': []}
    result['tests'] += runTests()

    score = round(sum([t['weight'] for t in result['tests'] if t['result'] == PASS]), 2)
    total = round(sum([t['weight'] for t in result['tests']]), 2)
    assert total == 100, "Total should add up to 100, not {}".format(total)
    result['score'] = score

    with open('result.json', 'w') as fp:
        fp.write(json.dumps(result, indent=2))

    print('RESULTS:')
    for test in result['tests']:
        suffix = ""
        if test['result'] is False:
            suffix = "... (your program may have an error, please see above for more information)"
        elif test['result'] != PASS and isinstance(test['result'], str) and test['result'].startswith('expected'):
            suffix = "... (please see above for more information)"
        print('    {}: {} {}'.format(test['test'], str(test['result'])[:100], suffix))

    print("Score: {}%".format(result['score']))

if __name__ == '__main__':
    ensure_correct_python_version()
    main()
