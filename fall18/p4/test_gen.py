#!/usr/bin/python
import subprocess, json, re, sys, importlib, random, string
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

PROMPT = 'enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: '


GOOD_NUM = 'good_num'
BAD_NUM = 'bad_num'
GARBAGE = 'garbage'

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

class TestGen:
    def __init__(self):
        self.traces = []
    
    def trace_io(self, in_lines):
        cmd = [PYTHON_BINARY, '-u', PROGRAM]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

        actual_stdout, _ = p.communicate(bytes('\n'.join(in_lines)+'\n', 'utf-8'))
        actual_stdout = str(actual_stdout, 'utf-8')
        actual_stdout = actual_stdout.replace(PROMPT, PROMPT + '\n')

        lines = actual_stdout.split('\n')
        for i,line in enumerate(lines):
            if line.startswith(PROMPT):
                lines[i] += in_lines.pop(0)
        return '\n'.join(lines)

    def gen_test(self, steps=2, choices=['r', 'c', 'a', GOOD_NUM, BAD_NUM, GARBAGE]):
        in_lines = []
        for i in range(steps-1):
            cmd = random.choice(choices)
            if cmd == GOOD_NUM:
                if random.randint(0, 4) == 0:
                    cmd = str(random.randint(0, 100))
                else:
                    cmd = str(random.randint(40, 100))
            elif cmd == BAD_NUM:
                cmd = str(random.randint(101, 1000))
            elif cmd == GARBAGE:
                cmd = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random.randint(2, 10)))
            in_lines.append(cmd)
        in_lines.append('q')
        self.traces.append(self.trace_io(in_lines))

    def gen_tests(self, count=1, steps=2, choices=['r', 'c', 'a', GOOD_NUM, BAD_NUM, GARBAGE]):
        for i in range(count):
            self.gen_test(steps, choices)

    def dump_code(self, start):
        for i, trace in enumerate(self.traces):
            num = (i+start)
            print('def test_%d():' % num)
            print("    print('TEST %d')" % num)
            print("    return generic_test('''")
            print(trace.strip())
            print("'''.strip())")
            print()

def main():
    random.seed(301)
    tests = TestGen()

    # enter one good number and give correct grade (25%)
    tests.gen_tests(1, steps=1, choices=[])
    tests.gen_tests(49, steps=2, choices=[GOOD_NUM])

    # count, and occasionally reset (25%)
    tests.gen_tests(40, steps=5, choices=[GOOD_NUM, 'c'])
    tests.gen_tests(10, steps=8, choices=[GOOD_NUM, 'c', 'r'])

    # average, and occasionally reset (25%)
    tests.gen_tests(40, steps=5, choices=[GOOD_NUM, 'a'])
    tests.gen_tests(10, steps=8, choices=[GOOD_NUM, 'a', 'r'])

    # longer traces, mix of everything (10%)
    tests.gen_tests(20, steps=10, choices=[GOOD_NUM, 'c', 'r', 'a'])

    # tricky inputs (15%)
    tests.gen_tests(6, steps=10, choices=[GOOD_NUM, 'C', 'R', 'A'])
    tests.gen_tests(6, steps=5, choices=[GOOD_NUM, BAD_NUM])
    tests.gen_tests(6, steps=5, choices=[GOOD_NUM, GARBAGE])
    tests.gen_tests(6, steps=10, choices=[GOOD_NUM, BAD_NUM, GARBAGE, 'c', 'r', 'a', 'C', 'R', 'A'])
    tests.gen_tests(6, steps=30, choices=[GOOD_NUM, BAD_NUM, GARBAGE, 'c', 'r', 'a', 'C', 'R', 'A'])
    tests.dump_code(start=1)

if __name__ == '__main__':
    main()
