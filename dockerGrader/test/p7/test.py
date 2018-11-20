#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
from functools import wraps

PASS = 'PASS'
FAIL_STDERR = 'Program produced stderr - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
FAIL_TIMEOUT = 'Program took too long - please scroll above to see the exact command.'
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

def __fix_order(l, *keys):
    for k in keys:
        l.sort(key=lambda x: x[k])

def ensure_correct_python_version():
    python_binary = get_python_binary_name()
    python_version = get_python_version(python_binary)
    print('Your Python version: ' + python_version)

    if python_version.lower().find('python 3') < 0:
        print('WARNING! Your Python version may not work for this class.')
        print('Please check with us about this.')
        print()

class StderrException(Exception):
    def __init__(self, cmd, stderr):
        self.cmd = cmd
        self.stderr = stderr

class TimeoutException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

class MismatchException(Exception):
    def __init__(self, cmd, mismatch_str):
        self.cmd = cmd
        self.mismatch_str = mismatch_str

class BadFunctionException(Exception):
    def __init__(self, msg):
        self.msg = msg

class JsonException(Exception):
    def __init__(self, cmd, msg, e):
        self.cmd = cmd
        self.msg = msg
        self.json_exc = e

def run_cmd(subcmd, *args, timeout=2):
    cmd = [
        get_python_binary_name(), '-u', PROGRAM, subcmd, "movies.csv", "mapping.csv",
    ]
    cmd.extend(map(str, args))
    cmdstr = ' '.join(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    try:
        stdout, stderr = p.communicate(timeout=timeout * 2)
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        if stderr != '':
            raise StderrException(cmdstr, stderr)

        try:
            parsed_json = json.loads(stdout)
        except json.decoder.JSONDecodeError as e:
            raise JsonException(cmdstr, stdout, e)

        return parsed_json, cmdstr

    except subprocess.TimeoutExpired:
        p.kill()
        raise TimeoutException(cmdstr)

def compare_dicts(dict_a, expected_dict):
    assert isinstance(expected_dict, dict), "This shouldn't have happened. Please contact a TA!"

    if not isinstance(dict_a, dict):
        return "Expected dictionary but found {}".format(type(dict_a))

    if dict_a == expected_dict:
        return PASS

    # try to return a sane error.
    if len(dict_a) != len(expected_dict):
        return "Expected dictionary with {} keys but got dictionary with {} keys!".format(len(expected_dict), len(dict_a))

    dict_a_keys = set(dict_a.keys())
    expected_keys = set(expected_dict.keys())
    extra_keys = dict_a_keys - expected_keys
    missing_keys = expected_keys - dict_a_keys

    if len(missing_keys) > 0:
        return "Key {} is missing from dictionary!".format(missing_keys.pop())

    if len(extra_keys) > 0:
        return "Your dictionary has an extra key {}".format(extra_keys.pop())

    # They have the same keys
    for k,v in expected_dict.items():
        if v != dict_a[k]:
            return "Expected key {} to have value {!r} but found value {!r} instead!".format(k, v, dict_a[k])

    return "Expected dictionary {} but found dictionary {} instead!".format(expected_dict_kv_list, dict_a)

def compare_list_of_dicts(list_of_dicts, expected_list_of_dicts):
    assert isinstance(expected_list_of_dicts, list), "This shouldn't have happened. Please contact a TA!"

    if not isinstance(list_of_dicts, list):
        return "Expected list but found {}".format(type(list_of_dicts))

    if list_of_dicts == expected_list_of_dicts:
        return PASS

    if len(list_of_dicts) != len(expected_list_of_dicts):
        return "Expected {} entries but found {} entries instead!".format(len(expected_list_of_dicts), len(list_of_dicts))

    for i, (dict_a, expected_dict) in enumerate(zip(list_of_dicts, expected_list_of_dicts)):
        ret = compare_dicts(dict_a, expected_dict)
        if ret != PASS:
            return "Mismatch at index {}: {}".format(i, ret)

    return "Expected list {} but found list {} instead!".format(expected_list_of_dicts, list_of_dicts)


###########################################################################
#                         COMMAND LINE TESTS                              #
###########################################################################

group_weights = {
    "test_read_data": 54,
    "test_stats": 16,
    "test_top_n_actors": 10,
    "test_top_n_versatile_actors": 9,
    "test_top_n_directors": 8,
    "test_top_n_actors_extra": 1,
    "test_top_n_versatile_actors_extra": 1,
    "test_top_n_directors_extra": 1,
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
                raise BadFunctionException("Cannot find function {}".format(fname))

            num_parameters = len(inspect.signature(student_fn).parameters)
            if num_parameters != expected_num_params:
                raise BadFunctionException("Function {} should take {} parameters instead of {}".format(fname, expected_num_params, num_parameters))

            return fn()

        fns_by_group[name].add(new_fn)
        new_fn.group_name = name
        new_fn.get_weight = lambda : group_weights[name] / len(fns_by_group[name])
        test_functions.append((new_fn.__name__, new_fn))
        return new_fn

    return deco

@group("test_read_data", fname="get_mapping", expected_num_params=1)
def test_001():
    get_mapping = STUDENT_FUNCTIONS.get('get_mapping')
    small_map = get_mapping('small_mapping.csv')
    result = compare_dicts(small_map, expected['test_001'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_read_data", fname="get_mapping", expected_num_params=1)
def test_002():
    get_mapping = STUDENT_FUNCTIONS.get('get_mapping')
    big_map = get_mapping('mapping.csv')
    result = compare_dicts(big_map, expected['test_002'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_read_data", fname="get_movies", expected_num_params=1)
def test_003():
    get_movies = STUDENT_FUNCTIONS.get('get_movies')
    small_list_of_movies = get_movies('small_movies.csv')
    result = compare_list_of_dicts(small_list_of_movies, expected['test_003'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_read_data", fname="get_movies", expected_num_params=1)
def test_004():
    get_movies = STUDENT_FUNCTIONS.get("get_movies")
    big_list_of_movies = get_movies("movies.csv")
    result = compare_list_of_dicts(big_list_of_movies, expected['test_004'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_read_data", fname="read_data", expected_num_params=2)
def test_005():
    read_data = STUDENT_FUNCTIONS.get("read_data")
    small_list_of_movies = read_data("small_movies.csv", "small_mapping.csv")
    result = compare_list_of_dicts(small_list_of_movies, expected['test_005'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_read_data", fname="read_data", expected_num_params=2)
def test_006():
    read_data = STUDENT_FUNCTIONS.get("read_data")
    big_list_of_movies = read_data("movies.csv", "mapping.csv")
    result = compare_list_of_dicts(big_list_of_movies, expected['test_006'])
    if result != PASS:
        raise MismatchException(None, result)

    return PASS

@group("test_stats", fname='stats', expected_num_params=1)
def test_007():
    stats, cmdstr = run_cmd('stats')
    result = compare_dicts(stats, expected['test_007'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    # TODO check json stdout with expected
    return PASS

@group("test_top_n_actors", fname='top_n_actors', expected_num_params=2)
def test_008():
    top_n_actors, cmdstr = run_cmd('top_n_actors', 0)
    result = compare_list_of_dicts(top_n_actors, expected['test_008'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_actors", fname='top_n_actors', expected_num_params=2)
def test_009():
    top_n_actors, cmdstr = run_cmd('top_n_actors', 6)
    result = compare_list_of_dicts(top_n_actors, expected['test_009'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_actors", fname='top_n_actors', expected_num_params=2)
def test_010():
    # TODO depends on 8 passing first
    # TODO obfuscate this
    top_n_actors, cmdstr = run_cmd('top_n_actors', 10)
    # sorting to make sure ties are always printed in sorted order of name?
    __fix_order(top_n_actors, "actor", "score")
    result = compare_list_of_dicts(top_n_actors, expected['test_010'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_actors", fname='top_n_actors', expected_num_params=2)
def test_011():
    top_n_actors, cmdstr = run_cmd('top_n_actors', 20)
    __fix_order(top_n_actors, "actor", "score")
    result = compare_list_of_dicts(top_n_actors, expected['test_011'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_versatile_actors", fname='top_n_versatile_actors', expected_num_params=2)
def test_012():
    top_n_actors, cmdstr = run_cmd('top_n_versatile_actors', 0)
    result = compare_list_of_dicts(top_n_actors, expected['test_012'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_versatile_actors", fname='top_n_versatile_actors', expected_num_params=2)
def test_013():
    top_n_actors, cmdstr = run_cmd('top_n_versatile_actors', 3)
    __fix_order(top_n_actors, "actor", "score")
    result = compare_list_of_dicts(top_n_actors, expected['test_013'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_versatile_actors", fname='top_n_versatile_actors', expected_num_params=2)
def test_014():
    top_n_actors, cmdstr = run_cmd('top_n_versatile_actors', 15)
    __fix_order(top_n_actors, "actor", "score")
    result = compare_list_of_dicts(top_n_actors, expected['test_014'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_directors", fname='top_n_directors', expected_num_params=2)
def test_015():
    top_n_directors, cmdstr = run_cmd('top_n_directors', 0)
    result = compare_list_of_dicts(top_n_directors, expected['test_015'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_directors", fname='top_n_directors', expected_num_params=2)
def test_016():
    top_n_directors, cmdstr = run_cmd('top_n_directors', 4)
    __fix_order(top_n_directors, "director", "score")
    result = compare_list_of_dicts(top_n_directors, expected['test_016'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_directors", fname='top_n_directors', expected_num_params=2)
def test_017():
    top_n_directors, cmdstr = run_cmd('top_n_directors', 12)
    __fix_order(top_n_directors, "director", "score")
    result = compare_list_of_dicts(top_n_directors, expected['test_017'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_actors_extra", fname='top_n_actors', expected_num_params=2)
def test_018():
    top_n_actors, cmdstr = run_cmd('top_n_actors', 20)
    result = compare_list_of_dicts(top_n_actors, expected['test_018'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_versatile_actors_extra", fname='top_n_versatile_actors', expected_num_params=2)
def test_019():
    top_n_actors, cmdstr = run_cmd('top_n_versatile_actors', 15)
    result = compare_list_of_dicts(top_n_actors, expected['test_019'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS

@group("test_top_n_directors_extra", fname='top_n_directors', expected_num_params=2)
def test_020():
    top_n_directors, cmdstr = run_cmd('top_n_directors', 10)
    result = compare_list_of_dicts(top_n_directors, expected['test_020'])
    if result != PASS:
        raise MismatchException(cmdstr, result)

    return PASS


###########################################################################
#                              RUN TESTS                                  #
###########################################################################

def runTests():
    global test_functions
    results = []
    test_functions = sorted(test_functions, key=lambda x: x[0])

    read_data_test_names = { 'test_%03d' % i for i in range(1, 7) }
    test_to_result = {}

    for name, fn in test_functions:
        test_summary = {
            'test': name, 'result': None, 'weight': fn.get_weight(), 'group': fn.group_name,
        }

        test_to_result[name] = test_summary
        results.append(test_summary)

        if name not in read_data_test_names:
            # ensure that all read_data tests have passed before any other tests
            all_tests_passed = True
            for i in read_data_test_names:
                if test_to_result[i]['result'] != PASS:
                    all_tests_passed = False
                    test_summary['result'] = 'Please pass tests 1 to 6 first'

            if not all_tests_passed:
                continue

        try:
            result = fn()
            test_summary['result'] = result
            # TODO barriers in tests
        except JsonException as e:
            test_summary['result'] = FAIL_JSON
            print("Test {}".format(name))
            print("Ran cmd: {}".format(e.cmd))
            print("Got non json output - {}".format(e.msg))
            print(e.json_exc)
            print()
        except StderrException as e:
            test_summary['result'] = FAIL_STDERR
            print("Test {}".format(name))
            print("Ran cmd: {}".format(e.cmd))
            print("Got stderr: {}".format(e.stderr))
            print()
        except TimeoutException as e:
            test_summary['result'] = FAIL_TIMEOUT
            print("Test {}".format(name))
            print("Ran cmd: {}".format(e.cmd))
            print("Program took too long!")
            print()
        except BadFunctionException as e:
            test_summary['result'] = e.msg
            print("Test {}".format(name))
            print(e.msg)
            print()
        except MismatchException as e:
            test_summary['result'] = "Output mismatch. Please scroll above to see the exact command"
            print("Test {}".format(name))
            if e.cmd is not None:
                print("Ran cmd: {}".format(e.cmd))

            print(e.mismatch_str)
            print()
        except Exception as e:
            test_summary['result'] = "ERROR. Please scroll above to see what caused this"
            print("Test {}".format(name))
            traceback.print_exc()
            print()

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
        print('    {}: {}'.format(test['test'], str(test['result'])))

    print("Score: {}%".format(result['score']))
if __name__ == '__main__':
    ensure_correct_python_version()
    main()
