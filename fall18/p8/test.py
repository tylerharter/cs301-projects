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
# Problems are based on output of student functions
##################################################

def json_pretty(objects):
    return json.dumps(objects, indent=2, sort_keys=True)

def apply_car_filters(path, filters):
    jdata = MAIN.read_json(path)
    if jdata == None:
        return []
    tuples = MAIN.make_namedtuple_list(jdata)
    if jdata == None:
        return []
    tuples = MAIN.filter_cars(tuples, filters)
    if tuples == None:
        return []
    return [str(car) for car in tuples]

def test_1():
    weight = 5
    with open('test.txt') as f:
        expected = json.loads(f.read().split('@')[0])
    actual = MAIN.process_args(["main.py", "small_cars.json", "read_json"])
    return check_answer(json_pretty(expected), json_pretty(actual)), weight

def test_2():
    weight = 5
    with open('test.txt') as f:
        expected = json.loads(f.read().split('@')[1])
    actual = MAIN.process_args(["main.py", "cars.json", "read_json"])
    return check_answer(json_pretty(expected), json_pretty(actual)), weight

def test_3():
    weight = 8
    expected = "False"
    actual = MAIN.process_args(["main.py", "small_cars.json", "get_value", "2", "Hybrid"])
    return check_answer(expected, actual), weight

def test_4():
    weight = 8
    expected = "200"
    actual = MAIN.process_args(["main.py", "cars.json", "get_value", "3", "Horsepower"])
    return check_answer(expected, actual), weight

def test_5():
    weight = 8
    expected = "2011"
    actual = MAIN.process_args(["main.py", "cars.json", "get_value", "16", "Year"])
    return check_answer(expected, actual), weight

def test_6():
    weight = 8
    expected = "21"
    actual = MAIN.process_args(["main.py", "cars.json", "get_value", "3", "City mpg"])
    return check_answer(expected, actual), weight

def test_7():
    weight = 8
    expected = "Chevrolet"
    actual = MAIN.process_args(["main.py", "cars.json", "get_value", "40", "Make"])
    return check_answer(expected, actual), weight

def test_8():
    weight = 5

    # grab data as JSON and list of tuples
    jdata = MAIN.read_json("small_cars.json")
    if jdata == None:
        return "read_json not working", weight
    tuples = MAIN.make_namedtuple_list(jdata)
    if jdata == None:
        return "read_json not working", weight
    elif tuples==None:
        return "make_namedtuple_list not working", weight
    # is it a list of car tuples?
    if type(tuples) != list:
        return "make_namedtuple_list did not return a list", weight
    if type(tuples[0]).__name__ != 'Car':
        return "tuples not of a type named 'Car'", weight

    return PASS, weight

def test_9():
    weight = 5

    # grab data as JSON and list of tuples
    jdata = MAIN.read_json("small_cars.json")
    if jdata == None:
        return "read_json not working", weight
    tuples = MAIN.make_namedtuple_list(jdata)
    if jdata == None:
        return "read_json not working", weight
    elif tuples==None:
        return "make_namedtuple_list not working", weight
    # are there three objects of the same type with correct IDs?
    if len(tuples) == 0 or len(tuples) != len(jdata):
        return 'expected %d tuples'%len(jdata), weight
    for car in tuples:
        if type(car) != type(tuples[0]):
            return 'not all cars were of the same type (are you creating the Car type more than once?)', weight
        if not car.id in jdata:
            return 'car did not have a correct ID: '+str(car), weight

    return PASS, weight

def test_10():
    weight = 5

    # grab data as JSON and list of tuples
    jdata = MAIN.read_json("small_cars.json")
    if jdata == None:
        return "read_json not working", weight
    tuples = MAIN.make_namedtuple_list(jdata)
    if jdata == None:
        return "read_json not working", weight
    elif tuples==None:
        return "make_namedtuple_list not working", weight
    # do the cars have the correct data?
    if len(tuples) == 0 or len(tuples) != len(jdata):
        return 'expected %d tuples'%len(jdata), weight
    for car in tuples:
        car_dict = jdata[car.id]
        if (car.make != car_dict['Build']['Make'] or
            car.model != car_dict['Build']['Model'] or
            car.year != car_dict['Build']['Year'] or
            json_pretty(car.transmission) != json_pretty(car_dict['Config']['Transmission'])):
            
            return 'bad car: '+str(car), weight

    return PASS, weight

def test_11():
    weight = 5

    # same as previous test, but with whole dataset
    
    # grab data as JSON and list of tuples
    jdata = MAIN.read_json("cars.json")
    if jdata == None:
        return "read_json not working", weight
    tuples = MAIN.make_namedtuple_list(jdata)
    if jdata == None:
        return "read_json not working", weight
    elif tuples==None:
        return "make_namedtuple_list not working", weight
    # do the cars have the correct data?
    if len(tuples) == 0 or len(tuples) != len(jdata):
        return 'expected %d tuples'%len(jdata), weight
    for car in tuples:
        car_dict = jdata[car.id]
        if (car.make != car_dict['Build']['Make'] or
            car.model != car_dict['Build']['Model'] or
            car.year != car_dict['Build']['Year'] or
            json_pretty(car.transmission) != json_pretty(car_dict['Config']['Transmission'])):
            
            return 'bad car: '+str(car), weight

    return PASS, weight

def test_12():
    weight = 5
    with open('test.txt') as f:
        expected = f.read().split('@')[6].strip().split('\n')
    actual = apply_car_filters('small_cars.json', {'year': '2011'})
    if len(actual) > len(expected):
        return 'found more cars than expected', weight
    elif len(actual) < len(expected):
        return 'found fewer cars than expected', weight

    for a,e in zip(sorted(actual), sorted(expected)):
        if a.split('transmission')[0] != e.split('transmission')[0]:
            return ('found %s but expected %s' % (str(a), str(e))), weight
    
    return PASS, weight

def test_13():
    weight = 5
    with open('test.txt') as f:
        expected = f.read().split('@')[7].strip().split('\n')
    actual = apply_car_filters('small_cars.json', {'year': '2009'})
    if len(actual) > len(expected):
        return 'found more cars than expected', weight
    elif len(actual) < len(expected):
        return 'found fewer cars than expected', weight

    for a,e in zip(sorted(actual), sorted(expected)):
        if a.split('transmission')[0] != e.split('transmission')[0]:
            return ('found %s but expected %s' % (str(a), str(e))), weight
    
    return PASS, weight

def test_14():
    weight = 5
    with open('test.txt') as f:
        expected = f.read().split('@')[3].strip().split('\n')
    actual = apply_car_filters('cars.json', {'make': 'Audi'})
    if len(actual) > len(expected):
        return 'found more cars than expected', weight
    elif len(actual) < len(expected):
        return 'found fewer cars than expected', weight

    for a,e in zip(sorted(actual), sorted(expected)):
        if a.split('transmission')[0] != e.split('transmission')[0]:
            return ('found %s but expected %s' % (str(a), str(e))), weight
    
    return PASS, weight

def test_15():
    weight = 5
    with open('test.txt') as f:
        expected = f.read().split('@')[4].strip().split('\n')
    actual = apply_car_filters('cars.json', {'year': '2010'})
    if len(actual) > len(expected):
        return 'found more cars than expected', weight
    elif len(actual) < len(expected):
        return 'found fewer cars than expected', weight

    for a,e in zip(sorted(actual), sorted(expected)):
        if a.split('transmission')[0] != e.split('transmission')[0]:
            return ('found %s but expected %s' % (str(a), str(e))), weight
    
    return PASS, weight

def test_16():
    weight = 10   
    with open('test.txt') as f:
        expected = f.read().split('@')[5].strip().split('\n')
    actual = apply_car_filters('cars.json', {'year': '2010', 'make': 'Chevrolet'})
    if len(actual) > len(expected):
        return 'found more cars than expected', weight
    elif len(actual) < len(expected):
        return 'found fewer cars than expected', weight

    for a,e in zip(sorted(actual), sorted(expected)):
        if a.split('transmission')[0] != e.split('transmission')[0]:
            return ('found %s but expected %s' % (str(a), str(e))), weight
    
    return PASS, weight


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
        result, weight = fn()
        if len(result) > 200:
            result = result[:190] + '...'
        tests.append({'test': name, 'result': result, 'weight':weight})
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
    score = sum([t['weight'] for t in result['tests'] if t['result'] == PASS])
    total = sum([t['weight'] for t in result['tests']])
    if total != 100:
        print("Weights dont add up to 100, add up to", total)
    result['score'] = score

    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
    print('RESULTS:')
    for test in result['tests']:
        print('  {} ({}%): {}'.format(test['test'], test['weight'], test['result']))
    print('Score: %d%%' % result['score'])

if __name__ == '__main__':
    main()
