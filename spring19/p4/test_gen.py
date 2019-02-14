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

    def gen_test(self, tries, has_mistakes, f_apply):
        in_lines = [str(tries)]
        correct = ["c", "str", "True"]
        wrong = [["a", "b", "c", "e"],
                 ["float", "int", "bool"],
                 ["False", "1", "0", "None"]]

        for i in range(len(correct)):
            mistakes = random.randint(0, tries) if has_mistakes else 0
            in_lines += [random.choice(wrong[i]) for _ in range(mistakes)]
            if mistakes != tries:
                in_lines += [correct[i]]
            if f_apply:
                in_lines = [f_apply(x) for x in in_lines]

        self.traces.append(self.trace_io(in_lines))

    def gen_tests(self, count=1, tries=1, has_mistakes=True, f_apply=None):
        for i in range(count):
            self.gen_test(tries, has_mistakes, f_apply)

    def dump_code(self, start=1):
        for i, trace in enumerate(self.traces):
            num = (i+start)
            print('def test_%d():' % num)
            print("    print('TEST %d')" % num)
            print("    return generic_test('''")
            print(trace.strip())
            print("'''.strip())")
            print("\n")

def main():
    random.seed(301)
    tests = TestGen()

    tests.gen_tests(1, has_mistakes=False)
    tests.gen_tests(1, has_mistakes=False, f_apply=str.lower)
    tests.gen_tests(1, has_mistakes=False, f_apply=str.upper)
    tests.gen_tests(1, has_mistakes=False, f_apply=lambda x: '  '+x+'  ')
    tests.gen_tests(49, has_mistakes=True)
    tests.gen_tests(9, has_mistakes=True, f_apply=str.lower)
    tests.gen_tests(9, has_mistakes=True, f_apply=str.upper)
    tests.gen_tests(9, has_mistakes=True, f_apply=lambda x: '  '+x+'  ')
    for i in range(1, 11):
        tests.gen_tests(1, tries=i, has_mistakes=False)
    tests.gen_tests(3, tries=2, has_mistakes=True)
    tests.gen_tests(3, tries=3, has_mistakes=True)
    tests.gen_tests(4, tries=10, has_mistakes=True)
    tests.dump_code()

if __name__ == '__main__':
    main()
