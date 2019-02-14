#!/usr/bin/python
import subprocess, json, re, sys, importlib, random, string
from inspect import getmembers, isfunction

PASS = 'PASS'
EPSILON = 0.0001

# find student's code and import it as MAIN module
PROGRAM = 'correct.py'
MODULE_NAME = 'correct'
if len(sys.argv) == 2:
    PROGRAM = sys.argv[1]
    MODULE_NAME = PROGRAM.split('.')[0]

PROMPTS = [
    "How many tries do you want for each question: ",
    "Your answer: "
]

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
        for prompt in PROMPTS:
            actual_stdout = actual_stdout.replace(prompt, prompt + '\n')

        lines = actual_stdout.split('\n')
        for i,line in enumerate(lines):
            for prompt in PROMPTS:
                if line.startswith(prompt):
                    lines[i] += in_lines.pop(0)
        return '\n'.join(lines)

    def gen_test(self, tries=1):
        in_lines = ["1", "d", "str", "True"]
        self.traces.append(self.trace_io(in_lines))

    def gen_tests(self, count=1, tries=1):
        for i in range(count):
            self.gen_test(tries)

    def dump_code(self, start=1):
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
    tests.gen_tests(1)
    tests.dump_code()

if __name__ == '__main__':
    main()
