#!/usr/bin/python
import subprocess, json, re, sys
from inspect import getmembers, isfunction
import main

PASS = 'PASS'
PROBLEMS = 20
EPSILON = 0.0001

TESTS = [
    ("getMaximumLand", ["Wisconsin", "Iowa", "Minnesota"], 86935.83), #1-1
    ("getMaximumLand", ["Arizona", "California", "Connecticut"], 163694.74), #1-2
    ("getMaximumLand", ["Georgia", "Iowa", "Hawaii"], 59425.15), #1-3
    ("getMaximumLand", ["Minnesota", "Iowa", "Wisconsin"], 86935.83), #1-4
    ("getMaximumLand", ["Pennsylvania", "West Virginia", "Texas"], 268596.46), #1-5
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2000], 52.002450206414075), #2-1
    ("getMinimumPopulationDensity", ["Georgia", "Iowa", "Hawaii", 2000], 52.002450206414075), #2-2
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2010], 54.13546968775862), #2-3
    ("getMinimumPopulationDensity", ["Connecticut", "California", "Arizona", 2010], 56.07509586341995), #2-4
    ("getMinimumPopulationDensity", ["Wisconsin", "Iowa", "Minnesota", 2015], 55.257254791434804), #2-5
    ("predictPopulation", ["Wisconsin", 0.5, 2000, 2010], 796039951.1495125), #3-1
    ("predictPopulation", ["Georgia", 0.5, 2000, 2010], 1214977351.5747654), #3-2
    ("predictPopulation", ["Wisconsin", 0.4, 2000, 2010], 292846732.3790249), #3-3
    ("predictPopulation", ["Hawaii", 0.4, 2000, 2010], 66147678.89670547), #3-4
    ("predictPopulation", ["California", 0.6, 2010, 2015], 748265708.7728088), #3-5
    ("calcGrowthRate", ["Wisconsin", 2000, 2010], 0.005853103209551789), #4-1
    ("calcGrowthRate", ["Georgia", 2010, 2015], 0.008279847004730256), #4-2
    ("calcGrowthRate", ["Hawaii", 2000, 2015], 0.010596535979501064), #4-3
    ("calcGrowthRate", ["California", 2000, 2010], 0.009517981825461748), #4-4
    ("calcGrowthRate", ["Iowa", 2000, 2015], 0.004047253559630651) #4-5
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
        testCase = TESTS[problemNum - 1]
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
