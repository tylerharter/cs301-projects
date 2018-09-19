#!/usr/bin/python
import subprocess, json, re, sys
from inspect import getmembers, isfunction
import main

PASS = 'PASS'
PROBLEMS = 20
EPSILON = 0.0001

TESTS_FUNC = [
    ("getMaximumLand", ["Arizona", "California", "Connecticut"], 163694.74),
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2010], 54.13546968775862),
    ("predictPopulation", ["Hawaii", 0.4, 2000, 2010], 66147678.89670547),
    ("calcGrowthRate", ["Hawaii", 2000, 2015], 0.010596535979501064)
]

def runTest(functionName, fn, args, expectedResult):
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

    python_binary = get_python_binary_name()
    version = get_python_version(python_binary)
    print('Your Python version: '+version)

    if version.lower().find('python 3') < 0:
        print('WARNING! Your Python version may not work for this class.')
        print('Please check with us about this.')
        print()

    studentFunctions = dict([func for func in getmembers(main) if isfunction(func[1])])

    for problemNum in range(1, PROBLEMS + 1):
        testCase = TESTS_FUNC[problemNum - 1]
        # run test and record output
        try:
            testResult = runTest(
                testCase[0], studentFunctions.get(testCase[0]), testCase[1], testCase[2])
        except Exception as e:
            testResult = "Got exception {} when running test {}".format(
                str(e), problemNum)
        result['tests'].append({
            'test': problemNum,
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
