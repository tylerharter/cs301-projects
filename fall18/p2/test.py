#!/usr/bin/python
import subprocess, json, re, sys, importlib
from inspect import getmembers, isfunction
#import main

PASS = 'PASS'
EPSILON = 0.0001

TESTS_FUNC = [
    ("getMaximumLand", ["Arizona", "California", "Connecticut"], 163694.74), #1
    ("getMaximumLand", ["Georgia", "Iowa", "Hawaii"], 59425.15), #2
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2010], 54.13546968775862), #3
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2015], 55.257254791434804), #4
    ("getMinimumPopulationDensity", ["Georgia", "Iowa", "Hawaii", 2000], 52.002450206414075), #5
    ("predictPopulation", ["Wisconsin", 2000, 2010, 0.5], 796039951.1495125), #6
    ("predictPopulation", ["Hawaii", 2000, 2010, 0.4], 66147678.89670547), #7
    ("predictPopulation", ["Georgia", 2000, 2010, 0.5], 1214977351.5747654), #8
    ("predictPopulation", ["Hawaii", 2000, 2010], 3293299.011605786), #9
    ("predictPopulation", ["Hawaii", 2000, 2010], 3293299.011605786), #10
    ("calcGrowthRate", ["Wisconsin", 2000, 2010], 0.005853103209551789), #11
    ("calcGrowthRate", ["Hawaii", 2000, 2015], 0.010596535979501064), #12
    ("calcGrowthRate", ["Georgia", 2010, 2015], 0.008279847004730256), #13
    ("calcGrowthRate", ["Iowa", 2000, 2015], 0.004047253559630651) #14
]

TESTS_PRINT = [
    [None, 65496.38], #1
    [None, 5686986.0], #2
    [None, 86935.83], #3
    [None, 52.002450206414075], #4
    [None, 796039951.1495125], #5
    [None, 0.005853103209551789] #6
]

TESTS_FUNC_NUM = len(TESTS_FUNC)
TESTS_PRINT_NUM = len(TESTS_PRINT)
PROBLEMS = TESTS_FUNC_NUM + TESTS_PRINT_NUM

def clean_lines(lines):
    result = []
    for l in lines:
        if type(l) is str:
            if l.strip() != '':
                result.append(l.strip())
        else:
            result.append(l)
    return result

# ignore whitespace and case
def areLinesExpected(actual_lines, expected_lines):
    actual_lines = clean_lines(actual_lines)
    expected_lines = clean_lines(expected_lines)
    print(actual_lines, expected_lines)
    if len(actual_lines) < len(expected_lines):
        return 'fewer output lines than expected'
    if len(actual_lines) > len(expected_lines):
        return 'more output lines than expected'
    for a, e in zip(actual_lines, expected_lines):
        if not e: 
            continue
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

def runPrintTest(lines, expected):
    error = areLinesExpected(lines, expected)
    return error if error else PASS

def runFuncTest(functionName, fn, args, expectedResult):
    if fn:
        actualResult = fn(*args)
    else:
        return "function %s not found" % functionName
    if abs(actualResult - expectedResult) > EPSILON:
        return "%s(%s) expected return %s but found %s" % (
            functionName, ', '.join([str(arg) for arg in args]), expectedResult, actualResult)
    return PASS

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

def mainFunc():
    result = {'score': 0, 'tests': []}
    program = 'main.py'
    module_name = 'main'
    output = None

    python_binary = get_python_binary_name()
    version = get_python_version(python_binary)
    print('Your Python version: '+version)

    if version.lower().find('python 3') < 0:
        print('WARNING! Your Python version may not work for this class.')
        print('Please check with us about this.')
        print()

    if len(sys.argv) == 2:
        program = sys.argv[1]
        module_name = program.split('.')[0]
    try:
        cmd = [python_binary, program]
        print('Running your program with this command: ' + ' '.join(cmd) + '\n')
        output = subprocess.check_output(cmd)
    except:
        print('Your Python program crashed.  Please fix it to get any points.')

    main_module = importlib.import_module(module_name)
    studentFunctions = dict([func for func in getmembers(main_module) if isfunction(func[1])])
    for problemNum in range(1, TESTS_FUNC_NUM + 1):
        testCase = TESTS_FUNC[problemNum - 1]
        try:
            testResult = runFuncTest(
                testCase[0], studentFunctions.get(testCase[0]), testCase[1], testCase[2])
        except Exception as e:
            testResult = "Got exception {} when running test {}".format(
                str(e), problemNum)
        result['tests'].append({
            'test': "Function test {} ({})".format(problemNum, testCase[0]),
            'result': testResult
        })
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

    for problemNum in range(1, TESTS_PRINT_NUM + 1):
        testCase = TESTS_PRINT[problemNum - 1]
        lines = problems.pop(problemNum, None)         # student code
        # did student produce output?
        if lines is None:
            result['tests'].append({
                'test': "Main function print test (Problem {})".format(problemNum),
                'result': 'Main function print test {} output missing'.format(problemNum)
            })
            continue
        testResult = runPrintTest(lines, testCase)
        result['tests'].append({
            'test': "Main function print test (Problem {})".format(problemNum),
            'result': testResult
        })

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
    mainFunc()
