#!/usr/bin/python
import subprocess, json, re, sys
from inspect import getmembers, isfunction
import main

PASS = 'PASS'
EPSILON = 0.0001

TESTS_FUNC = [
    ("getMaximumLand", ["Arizona", "California", "Connecticut"], 163694.74), #1
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2010], 54.13546968775862), #2
    ("predictPopulation", ["Hawaii", 2000, 2010, 0.4], 66147678.89670547), #3
    ("predictPopulation", ["Hawaii", 2000, 2010], 3293299.011605786), #4
    ("calcGrowthRate", ["Hawaii", 2000, 2015], 0.010596535979501064) #5
]

TESTS_PRINT = [
    ["The area of Wisconsin is ", 65496.38], #1
    ["The population of Wisconsin in 2010 is ", 5686986.0], #2
    ["Maximum land area among Wisconsin, Iowa, Minnesota is ", 86935.83], #3
    ["Minimum population density among Wisconsin, Iowa, Minnesota is ", 52.002450206414075], #4
    ["The predicted population for Wisconsin in year 2010 is (assume start yearA is 2000, growth rate is 0.5) ", 796039951.1495125], #5
    ["The growth rate for Wisconsin between year 2000 and 2010 is ", 0.005853103209551789] #6
]

TESTS_FUNC_NUM = len(TESTS_FUNC)
TESTS_PRINT_NUM = len(TESTS_PRINT)
PROBLEMS = TESTS_FUNC_NUM + TESTS_PRINT_NUM

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
            functionName, ', '.join([str(arg) for arg in args]), actualResult, expectedResult)
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
    try:
        cmd = [python_binary, program]
        print('Running your program with this command: ' + ' '.join(cmd) + '\n')
        output = subprocess.check_output(cmd)
    except:
        print('Your Python program crashed.  Please fix it to get any points.')

    studentFunctions = dict([func for func in getmembers(main) if isfunction(func[1])])

    for problemNum in range(1, TESTS_FUNC_NUM + 1):
        testCase = TESTS_FUNC[problemNum - 1]
        try:
            testResult = runFuncTest(
                testCase[0], studentFunctions.get(testCase[0]), testCase[1], testCase[2])
        except Exception as e:
            testResult = "Got exception {} when running test {}".format(
                str(e), problemNum)
        result['tests'].append({
            'test': problemNum,
            'result': testResult
        })

    if output:
        # normalize windows => unix, as a string (not bytes)
        output = str(output, 'utf-8')
        output = output.replace('\r\n', '\n')

        # chuck output lines by problem
        problem_number = None
        problems = dict() # key:problem number, val: list of lines
        for line in output.split('\n'):
            m = re.match(r'Problem (\d+)$', line)
            if m:
                problem_number = int(m.group(1))
                problems[problem_number] = []
            elif problem_number:
                problems[problem_number].append(line)

        for problemNum in range(6, 12):
            testCase = TESTS_PRINT[problemNum - 6]
            lines = problems.pop(problemNum, None)         # student code
            # did student produce output?
            if lines is None:
                result['tests'].append({
                    'test': problem_num,
                    'result': 'Problem %d output missing' % problem_num
                })
                continue
            testResult = runPrintTest(lines, testCase)
            result['tests'].append({
                'test': problemNum + TESTS_FUNC_NUM,
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
        print('  Problem %d: %s' % (test['test'], test['result']))
    print('Score: %d%%' % result['score'])

if __name__ == '__main__':
    mainFunc()
