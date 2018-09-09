#!/usr/bin/python
import subprocess, json, re

PASS = 'PASS'
PROBLEMS = 20

# ignore whitespace and case
def are_lines_expected(actual_lines, expected_lines):
    actual_lines = [l.strip() for l in actual_lines if l.strip() != '']
    expected_lines = [l.strip() for l in expected_lines if l.strip() != '']
    if len(actual_lines) < len(expected_lines):
        return 'fewer output lines than expected'
    if len(actual_lines) > len(expected_lines):
        return 'more output lines than expected'
    for a,e in zip(actual_lines, expected_lines):
        if a.lower() != e.lower():
            return 'expected (%s) but found (%s)' % (e, a)
    return None

def problem1(lines):
    expected = [
        'one plus one is:',
        '2',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem2(lines):
    expected = [
        'two plus two is:',
        '4',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem3(lines):
    pass

def main():
    result = {'score': 0, 'tests': []}
    output = None
    try:
        output = subprocess.check_output(['python3', 'main.py'])
    except:
        print('Your Python program crashed.  Please fix it to get any points.')

    # did program even run successfully?
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

        # run checker on each section
        for problem_num in range(1, PROBLEMS+1):
            lines = problems.pop(problem_num, None)         # student code
            fn = globals().get('problem%d' % problem_num, None) # our test

            # did student produce output?
            if lines is None:
                result['tests'].append({
                    'test': problem_num,
                    'result': 'Problem %d output missing' % problem_num
                })
                continue

            # did we write the test yet?
            if not fn:
                result['tests'].append({
                    'test': problem_num,
                    'result': 'Test %d not written yet' % problem_num
                })
                continue

            # run test and record output
            test_result = fn(lines)
            result['tests'].append({
                'test': problem_num,
                'result': test_result
            })
        # final score
        passing = [t for t in result['tests'] if t['result'] == PASS]
        result['score'] = len(passing) * 100 / len(result['tests'])

    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
    print('RESULTS:')
    for test in result['tests']:
        print('  Problem %d: %s' % (test['test'], test['result']))
    print('Score: %d' % result['score'])

if __name__ == '__main__':
    main()
