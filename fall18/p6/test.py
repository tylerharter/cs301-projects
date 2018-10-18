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
    sys.exit()

with open("expected.json") as fp:
    expected = json.load(fp)

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

def run_cmd(subcmd, csvfile, *args, timeout=2):
    cmd = [
        get_python_binary_name(), '-u', PROGRAM, subcmd, csvfile,
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
    "test_read_csv": 15,
    "test_sample": 10,
    "test_get_cell": 5,
    "test_get_fastest": 10,
    "test_get_column": 15,
    "test_names_alphabetical": 5,
    "test_avg_windspeed": 5,
    "test_filter_on_col": 10,
    "test_num_in_ocean": 5,
    "test_cmp_avg_windspeed_by_ocean": 15,
    "test_unknown_command": 5,
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

@group("test_read_csv", fname='read_csv', expected_num_params=1)
def test_001():
    read_csv = STUDENT_FUNCTIONS.get("read_csv")
    dataset = read_csv("hurricanes.csv")
    expected_dataset = expected["test_001"]
    if expected_dataset == dataset:
        return PASS

    # print some more useful info to help debug
    if dataset is None:
        return "Function read_csv returned None instead of the dataset list!"

    # try and return the first error which will most likely solve the rest (if it is a parsing error)
    if len(dataset) != len(expected_dataset):
        return "Expected {} rows in dataset but got {} rows instead".format(
            len(dataset), len(expected_dataset),
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

@group("test_sample", fname='sample', expected_num_params=3)
def test_002():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 0, 'start')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_002"], stdout)
    if error:
        print("Test test_002 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_002"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_003():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 0, 'end')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_003"], stdout)
    if error:
        print("Test test_003 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_003"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_004():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 0, 'nothing')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_004"], stdout)
    if error:
        print("Test test_004 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_004"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_005():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 0, 'startend')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_005"], stdout)
    if error:
        print("Test test_005 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_005"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_006():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 1, 'start')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_006"], stdout)
    if error:
        print("Test test_006 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_006"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_007():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 1, 'end')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_007"], stdout)
    if error:
        print("Test test_007 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_007"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_008():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 1, 'nothing')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_008"], stdout)
    if error:
        print("Test test_008 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_008"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_009():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 1, 'startend')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_009"], stdout)
    if error:
        print("Test test_009 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_009"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_010():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 5, 'start')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_010"], stdout)
    if error:
        print("Test test_010 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_010"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_011():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 5, 'end')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_011"], stdout)
    if error:
        print("Test test_011 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_011"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_012():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 5, 'nothing')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_012"], stdout)
    if error:
        print("Test test_012 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_012"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_013():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 5, 'startend')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_013"], stdout)
    if error:
        print("Test test_013 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_013"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_014():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 10, 'start')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_014"], stdout)
    if error:
        print("Test test_014 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_014"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_015():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 10, 'end')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_015"], stdout)
    if error:
        print("Test test_015 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_015"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_016():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 10, 'nothing')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_016"], stdout)
    if error:
        print("Test test_016 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_016"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_017():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 10, 'startend')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_017"], stdout)
    if error:
        print("Test test_017 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_017"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_018():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 20, 'start')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_018"], stdout)
    if error:
        print("Test test_018 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_018"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_019():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 20, 'end')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_019"], stdout)
    if error:
        print("Test test_019 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_019"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_020():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 20, 'nothing')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_020"], stdout)
    if error:
        print("Test test_020 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_020"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_sample", fname='sample', expected_num_params=3)
def test_021():
    stdout, stderr, cmdstr = run_cmd('sample', "hurricanes.csv", 20, 'startend')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_021"], stdout)
    if error:
        print("Test test_021 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_021"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_022():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 0, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_022"], stdout)
    if error:
        print("Test test_022 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_022"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_023():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 0, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_023"], stdout)
    if error:
        print("Test test_023 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_023"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_024():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 0, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_024"], stdout)
    if error:
        print("Test test_024 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_024"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_025():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 0, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_025"], stdout)
    if error:
        print("Test test_025 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_025"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_026():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 10, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_026"], stdout)
    if error:
        print("Test test_026 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_026"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_027():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 10, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_027"], stdout)
    if error:
        print("Test test_027 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_027"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_028():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 10, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_028"], stdout)
    if error:
        print("Test test_028 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_028"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_029():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 10, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_029"], stdout)
    if error:
        print("Test test_029 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_029"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_030():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 50, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_030"], stdout)
    if error:
        print("Test test_030 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_030"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_031():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 50, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_031"], stdout)
    if error:
        print("Test test_031 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_031"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_032():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 50, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_032"], stdout)
    if error:
        print("Test test_032 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_032"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_033():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 50, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_033"], stdout)
    if error:
        print("Test test_033 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_033"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_034():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 100, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_034"], stdout)
    if error:
        print("Test test_034 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_034"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_035():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 100, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_035"], stdout)
    if error:
        print("Test test_035 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_035"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_036():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 100, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_036"], stdout)
    if error:
        print("Test test_036 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_036"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_037():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 100, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_037"], stdout)
    if error:
        print("Test test_037 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_037"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_038():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 250, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_038"], stdout)
    if error:
        print("Test test_038 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_038"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_039():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 250, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_039"], stdout)
    if error:
        print("Test test_039 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_039"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_040():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 250, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_040"], stdout)
    if error:
        print("Test test_040 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_040"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_041():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 250, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_041"], stdout)
    if error:
        print("Test test_041 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_041"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_042():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 528, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_042"], stdout)
    if error:
        print("Test test_042 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_042"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_043():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 528, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_043"], stdout)
    if error:
        print("Test test_043 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_043"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_044():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 528, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_044"], stdout)
    if error:
        print("Test test_044 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_044"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_045():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", 528, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_045"], stdout)
    if error:
        print("Test test_045 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_045"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_046():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -1, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_046"], stdout)
    if error:
        print("Test test_046 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_046"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_047():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -1, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_047"], stdout)
    if error:
        print("Test test_047 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_047"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_048():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -1, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_048"], stdout)
    if error:
        print("Test test_048 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_048"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_049():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -1, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_049"], stdout)
    if error:
        print("Test test_049 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_049"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_050():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -30, 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_050"], stdout)
    if error:
        print("Test test_050 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_050"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_051():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -30, 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_051"], stdout)
    if error:
        print("Test test_051 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_051"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_052():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -30, 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_052"], stdout)
    if error:
        print("Test test_052 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_052"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_cell", fname='get_cell', expected_num_params=3)
def test_053():
    stdout, stderr, cmdstr = run_cmd('get_cell', "hurricanes.csv", -30, -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_053"], stdout)
    if error:
        print("Test test_053 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_053"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_fastest", fname='get_fastest', expected_num_params=1)
def test_054():
    stdout, stderr, cmdstr = run_cmd('get_fastest', "hurricanes.csv", )
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_054"], stdout)
    if error:
        print("Test test_054 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_054"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_055():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", 0)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_055"], stdout)
    if error:
        print("Test test_055 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_055"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_056():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", 1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_056"], stdout)
    if error:
        print("Test test_056 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_056"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_057():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", 2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_057"], stdout)
    if error:
        print("Test test_057 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_057"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_058():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", -1)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_058"], stdout)
    if error:
        print("Test test_058 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_058"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_059():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", -2)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_059"], stdout)
    if error:
        print("Test test_059 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_059"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_get_column", fname='get_column', expected_num_params=2)
def test_060():
    stdout, stderr, cmdstr = run_cmd('get_column', "hurricanes.csv", -3)
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_060"], stdout)
    if error:
        print("Test test_060 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_060"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_names_alphabetical", fname='names_alphabetical', expected_num_params=1)
def test_061():
    stdout, stderr, cmdstr = run_cmd('names_alphabetical', "hurricanes.csv", )
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_061"], stdout)
    if error:
        print("Test test_061 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_061"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_avg_windspeed", fname='avg_windspeed', expected_num_params=1)
def test_062():
    stdout, stderr, cmdstr = run_cmd('avg_windspeed', "hurricanes.csv", )
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_062"], stdout)
    if error:
        print("Test test_062 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_062"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_063():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'HEIDI')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_063"], stdout)
    if error:
        print("Test test_063 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_063"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_064():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'JIMENA')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_064"], stdout)
    if error:
        print("Test test_064 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_064"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_065():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'AMY')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_065"], stdout)
    if error:
        print("Test test_065 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_065"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_066():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'ELLEN')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_066"], stdout)
    if error:
        print("Test test_066 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_066"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_067():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'SELMA')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_067"], stdout)
    if error:
        print("Test test_067 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_067"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_068():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'PYTHON')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_068"], stdout)
    if error:
        print("Test test_068 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_068"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_069():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 0, 'MELISSA')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_069"], stdout)
    if error:
        print("Test test_069 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_069"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_070():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 2, 'Pacific')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_070"], stdout)
    if error:
        print("Test test_070 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_070"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_071():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 2, 'Atlantic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_071"], stdout)
    if error:
        print("Test test_071 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_071"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_filter_on_col", fname='filter_on_col', expected_num_params=3)
def test_072():
    stdout, stderr, cmdstr = run_cmd('filter_on_col', "hurricanes.csv", 2, 'Artic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_072"], stdout)
    if error:
        print("Test test_072 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_072"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_num_in_ocean", fname='num_in_ocean', expected_num_params=2)
def test_073():
    stdout, stderr, cmdstr = run_cmd('num_in_ocean', "hurricanes.csv", 'Pacific')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_073"], stdout)
    if error:
        print("Test test_073 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_073"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_num_in_ocean", fname='num_in_ocean', expected_num_params=2)
def test_074():
    stdout, stderr, cmdstr = run_cmd('num_in_ocean', "hurricanes.csv", 'Atlantic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_074"], stdout)
    if error:
        print("Test test_074 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_074"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_num_in_ocean", fname='num_in_ocean', expected_num_params=2)
def test_075():
    stdout, stderr, cmdstr = run_cmd('num_in_ocean', "hurricanes.csv", 'Artic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_075"], stdout)
    if error:
        print("Test test_075 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_075"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_cmp_avg_windspeed_by_ocean", fname='cmp_avg_windspeed_by_ocean', expected_num_params=3)
def test_076():
    stdout, stderr, cmdstr = run_cmd('cmp_avg_windspeed_by_ocean', "hurricanes.csv", 'Pacific', 'Pacific')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_076"], stdout)
    if error:
        print("Test test_076 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_076"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_cmp_avg_windspeed_by_ocean", fname='cmp_avg_windspeed_by_ocean', expected_num_params=3)
def test_077():
    stdout, stderr, cmdstr = run_cmd('cmp_avg_windspeed_by_ocean', "hurricanes.csv", 'Pacific', 'Atlantic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_077"], stdout)
    if error:
        print("Test test_077 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_077"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_cmp_avg_windspeed_by_ocean", fname='cmp_avg_windspeed_by_ocean', expected_num_params=3)
def test_078():
    stdout, stderr, cmdstr = run_cmd('cmp_avg_windspeed_by_ocean', "hurricanes.csv", 'Atlantic', 'Pacific')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_078"], stdout)
    if error:
        print("Test test_078 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_078"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_cmp_avg_windspeed_by_ocean", fname='cmp_avg_windspeed_by_ocean', expected_num_params=3)
def test_079():
    stdout, stderr, cmdstr = run_cmd('cmp_avg_windspeed_by_ocean', "hurricanes.csv", 'Atlantic', 'Atlantic')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_079"], stdout)
    if error:
        print("Test test_079 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_079"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_unknown_command")
def test_080():
    stdout, stderr, cmdstr = run_cmd('some_unknown_cmd', "hurricanes.csv", 'blah')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_080"], stdout)
    if error:
        print("Test test_080 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_080"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

@group("test_unknown_command")
def test_081():
    stdout, stderr, cmdstr = run_cmd('another_unknown_cmd', "hurricanes.csv", 'blah', 'blah')
    if stderr != '':
        print("Program produced stderr:")
        print(stderr)
        return False

    error = check_equal_stdout(expected["test_081"], stdout)
    if error:
        print("Test test_081 failed")
        print("Ran cmd: " + cmdstr)
        print("Expected output: ")
        print(expected["test_081"])
        print("Your program output: ")
        print(stdout)

    return error if error else PASS

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

    score = round(sum([t['weight'] for t in result['tests'] if t['result'] == PASS]))
    total = round(sum([t['weight'] for t in result['tests']]))
    assert total == 100, "Total should add up to 100, not {}".format(total)
    result['score'] = score

    with open('result.json', 'w') as fp:
        fp.write(json.dumps(result, indent=2))

    print('RESULTS:')
    for test in result['tests']:
        suffix = ""
        if test['result'] != PASS and test['result'].startswith('expected'):
            suffix = "... (please see above for more information)"
        print('    {}: {} {}'.format(test['test'], str(test['result'])[:100], suffix))

    print("Score: {}%".format(result['score']))

if __name__ == '__main__':
    ensure_correct_python_version()
    main()
