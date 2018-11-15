#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
from collections import namedtuple, OrderedDict
from functools import wraps

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
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

def run_cmd(subcmd, *args):
    cmd = [
        get_python_binary_name(), '-u', PROGRAM, subcmd, 
    ]
    cmd.extend(map(str, args))
    cmdstr = ' '.join(cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    stdout, stderr = p.communicate()
    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')
    if stderr != '':
        raise StderrException(cmdstr, stderr)
    
    try:
        parsed_json = json.loads(stdout)
    except json.decoder.JSONDecodeError as e:
        return stdout, cmdstr
    
    return parsed_json, cmdstr

def compare_file_lists(list_a, expected_list):
    expected_cleaned_list = [clean_path(x) for x in expected_list]
    
    if expected_cleaned_list == list_a : 
       return PASS
    
    if len(expected_cleaned_list) != len(list_a):
       return "Expected a list with {} elements, but actually got {} elements".format(len(expected_cleaned_list), len(list_a))

    return "Expected list {} but found {} instead!".format(expected_cleaned_list, list_a)
        

def compare_dicts(dict_a, expected_dict):
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
    if list_of_dicts == expected_list_of_dicts:
        return PASS

    #special case test 8 
    if expected_list_of_dicts == "":
        if list_of_dicts != "":
            return "Expected to find no output, but got an output of type {}".format(type(list_of_dicts))

    if list_of_dicts == "":
        return "No output generated!" 

    if not isinstance(list_of_dicts, list):
        return "Expected list but found {}".format(type(list_of_dicts))

    if len(list_of_dicts) != len(expected_list_of_dicts):
        return "Expected {} entries but found {} entries instead!".format(len(expected_list_of_dicts), len(list_of_dicts))

    for i, (dict_a, expected_dict) in enumerate(zip(list_of_dicts, expected_list_of_dicts)):
        ret = compare_dicts(dict_a, expected_dict)
        if ret != PASS:
            return "Mismatch at index {}: {}".format(i, ret)

    return "Expected list {} but found list {} instead!".format(expected_list_of_dicts, list_of_dicts)

def compare_file_with_dict(expected_out):
    filename = expected_out['filename']
    if not os.path.exists(filename) or not os.path.isfile(filename):
        return "Your output file was not found! If your program ran correctly, test.py would generate two files : sample_out.json and full_out.json" 
    content = expected_out['content']
    with open(filename, 'r') as f:
        try:
            parsed_json = json.load(f) 
        except json.decoder.JSONDecodeError:
            return "Your output file is not a valid JSON file!" 
    return compare_list_of_dicts(parsed_json, content)
        
def clean_path(path): 
    comps = path.split("/")
    return os.path.join(*comps)

def build_command_from_test(test_tuple):
    cmd = "python main.py %s " % test_tuple.function_name
    params = [clean_path(x) for x in test_tuple.params]
    cmd += " ".join(params)
    return cmd

###########################################################################
#                         COMMAND LINE TESTS                              #
###########################################################################

test = namedtuple('TEST', 'test_group function_name num_params params')

TESTS = {
    # sample data tests
    1 : test('test_listdir',       'get_list_of_files',  1,     ['sample_data']), 
    2 : test('test_json_in',       'read_json_file',     1,     ['sample_data/1.json']),
    3 : test('test_csv_in',        'read_csv_file',      1,     ['sample_data/1.csv']),
    4 : test('unified_read_test',  'read_all',           1,     ['sample_data']),
    5 : test('clean_all_test',     'read_and_clean_all', 1,     ['sample_data']),
    6 : test('write_test',         'write_json',         2,     ['sample_data', 'out_sample.json']),

    # full data tests
    7  : test('test_listdir_full',       'get_list_of_files',  1,     ['full_data']), 
    8  : test('test_json_in_full',       'read_json_file',     1,     ['full_data/1.json']),
    9  : test('test_csv_in_full',        'read_csv_file',      1,     ['full_data/2.csv']),
    10 : test('unified_read_test_full',  'read_all',           1,     ['full_data']),
    11 : test('clean_all_test_full',     'read_and_clean_all', 1,     ['full_data']),
    12 : test('write_test_full',         'write_json',         2,     ['full_data', 'out_full.json']),
}

TESTS = OrderedDict(sorted(TESTS.items(), key=lambda x : x[0]))

group_weights = {
    'test_listdir'		:	10,  
    'test_json_in'		:	10,  
    'test_csv_in'		:	5,
    'unified_read_test'         :       15, 
    'clean_all_test'		:	10, 
    'write_test'		:	20, 
    'test_listdir_full'		:	5,   
    'test_json_in_full'		:	5, 
    'test_csv_in_full'		:	5,      
    'unified_read_test_full'	:	5,
    'clean_all_test_full'	:	5,  
    'write_test_full'		:	5     
}

assert sum(group_weights.values()) == 100 

all_test_names = [test.test_group for test in TESTS.values()]

TEST_GATE = 6
TEST_GATE_MSG = "Please pass tests 1-{} first".format(TEST_GATE)

def run_all(): 
    results = OrderedDict()
    for test_number, t in TESTS.items():
        test_details = {
            'name' : "TEST %d" % test_number, 
            'command' : build_command_from_test(t)
        }

        assert t.test_group  in group_weights, "{} not in known groups".format(t.test_group)

        # calculate score for this test
        test_details['weight'] = group_weights[t.test_group] / all_test_names.count(t.test_group)

        # should we run this test?
        if test_number > TEST_GATE and not all([results[x]['result'] == PASS for x in range(1, TEST_GATE + 1)]):
                test_details['result'] = TEST_GATE_MSG
                results[test_number] = test_details
                continue

        # check if function exists
        student_fn = STUDENT_FUNCTIONS.get(t.function_name)
        if student_fn is None:
            test_details['result'] = "Cannot find function {}".format(t.function_name)
            results[test_number] = test_details
            continue

        # check if signature is OK
        num_parameters = len(inspect.signature(student_fn).parameters)
        if num_parameters != t.num_params:
            test_details['result'] = "Function {} should take {} parameters instead of {}".format(fname, t.num_params, num_parameters)
            results[test_number] = test_details
            continue
        
        # construct params 
        params = t.params
        params = [clean_path(x) for x in params] 
        # run function 
        try:
            out, cmd = run_cmd(t.function_name, *params)
            expected_out = expected["test%d" % test_number]
            if t.function_name == 'write_json': 
                result = compare_file_with_dict(expected_out)
            elif t.function_name == 'get_list_of_files':
                result = compare_file_lists(out, expected_out)
            else: 
                print(test_number, type(out), type(expected_out))
                result = compare_list_of_dicts(out, expected_out)
            test_details['result'] = result

        except JsonException as e:
            test_details['result'] = FAIL_JSON
            print("Test {}".format(test_number))
            print("Ran cmd: {}".format(e.cmd))
            print("Got non json output - {}".format(e.msg))
            print(e.json_exc)
            print()
        except StderrException as e:
            test_details['result'] = FAIL_STDERR
            print("Test {}".format(test_number))
            print("Ran cmd: {}".format(e.cmd))
            print("Got stderr: {}".format(e.stderr))
            print()
        except TimeoutException as e:
            test_details['result'] = FAIL_TIMEOUT
            print("Test {}".format(test_number))
            print("Ran cmd: {}".format(e.cmd))
            print("Program took too long!")
            print()
        except BadFunctionException as e:
            test_details['result'] = e.msg
            print("Test {}".format(test_number))
            print(e.msg)
            print()
        except MismatchException as e:
            test_details['result'] = "Output mismatch. Please scroll above to see the exact command"
            print("Test {}".format(test_number))
            if e.cmd is not None:
                print("Ran cmd: {}".format(e.cmd))

            print(e.mismatch_str)
            print()
        except Exception as e:
            test_details['result'] = "ERROR. Please scroll above to see what caused this"
            print("Test {}".format(test_number))
            traceback.print_exc()
            print()
        results[test_number] = test_details
    return results

def main():
    results = {}
    results['per_test'] = run_all()
    results['score'] = sum([x['weight'] for x in results['per_test'].values() if x['result'] == PASS])
    results['total'] = 100

    print("RESULTS : \n")

    with open('result.json', 'w') as f: 
        json.dump(results, f, indent=2)

    for test in results['per_test'].values():
        if test['result'] == PASS:
            print('    {} : {}'.format(test['name'], str(test['result'])))
        else:
            fail_string = "FAILED" if test['result'] != TEST_GATE_MSG else "NOT RUN"
            print('    {} : {} : [-{}%]\t [Command tested: {}] \t: {}'.format(test['name'], fail_string, test['weight'], test['command'], str(test['result'])))
            
        
    print("\nScore: {}%".format(results['score']))
    
if __name__ == '__main__':
    ensure_correct_python_version()
    main()
