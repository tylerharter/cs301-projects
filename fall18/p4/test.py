#!/usr/bin/python
import subprocess, json, re, sys, importlib
from inspect import getmembers, isfunction

PASS = 'PASS'
EPSILON = 0.0001

PROGRAM = 'main.py'
if len(sys.argv) == 2:
    PROGRAM = sys.argv[1]

PROMPT = 'enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: '

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

def split_stdin_stdout(expected):
    stdin = []
    stdout = []
    for line in expected.split('\n'):
        line = line.lstrip()
        if line.startswith(PROMPT):
            stdin.append(line[len(PROMPT):] + '\n')
            stdout.append(line[:len(PROMPT)] + '\n')
        else:
            stdout.append(line + '\n')
    return ''.join(stdin), ''.join(stdout)

def check_equal_stdout(expected_stdout, actual_stdout):
    expected = [line.strip() for line in expected_stdout.split('\n') if line.strip()]
    actual = [line.strip() for line in actual_stdout.split('\n') if line.strip()]
    return areLinesExpected(actual, expected)

##################################################
# Tests
##################################################

def generic_test(expected):
    print('Expected Behavior:')
    print(expected)
    stdin, stdout = split_stdin_stdout(expected)

    cmd = [PYTHON_BINARY, '-u', PROGRAM]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

    try:
        actual_stdout, actual_stderr = p.communicate(bytes(stdin+'\n', 'utf-8'), timeout=1)
    except subprocess.TimeoutExpired:
        p.kill()
        return 'program timed out after 1 second'
    actual_stderr = str(actual_stderr, 'utf-8')
    if actual_stderr != '':
        print('program produced stderr: "%s"' % actual_stderr)
        return False

    actual_stdout = str(actual_stdout, 'utf-8')
    actual_stdout = actual_stdout.replace(PROMPT, PROMPT + '\n')
    error = check_equal_stdout(stdout, actual_stdout)
    return error if error else PASS

def test_1():
    print('TEST 1')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_2():
    print('TEST 2')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 74
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_3():
    print('TEST 3')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 100
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_4():
    print('TEST 4')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 31
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_5():
    print('TEST 5')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_6():
    print('TEST 6')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_7():
    print('TEST 7')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 92
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_8():
    print('TEST 8')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_9():
    print('TEST 9')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_10():
    print('TEST 10')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_11():
    print('TEST 11')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_12():
    print('TEST 12')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_13():
    print('TEST 13')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_14():
    print('TEST 14')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 44
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_15():
    print('TEST 15')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 45
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_16():
    print('TEST 16')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_17():
    print('TEST 17')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 89
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_18():
    print('TEST 18')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_19():
    print('TEST 19')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_20():
    print('TEST 20')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_21():
    print('TEST 21')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_22():
    print('TEST 22')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_23():
    print('TEST 23')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 49
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_24():
    print('TEST 24')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_25():
    print('TEST 25')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_26():
    print('TEST 26')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_27():
    print('TEST 27')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 38
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_28():
    print('TEST 28')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 100
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_29():
    print('TEST 29')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_30():
    print('TEST 30')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_31():
    print('TEST 31')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_32():
    print('TEST 32')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_33():
    print('TEST 33')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_34():
    print('TEST 34')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_35():
    print('TEST 35')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_36():
    print('TEST 36')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_37():
    print('TEST 37')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_38():
    print('TEST 38')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 93
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_39():
    print('TEST 39')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_40():
    print('TEST 40')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 87
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_41():
    print('TEST 41')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_42():
    print('TEST 42')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_43():
    print('TEST 43')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 99
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_44():
    print('TEST 44')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_45():
    print('TEST 45')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 65
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_46():
    print('TEST 46')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_47():
    print('TEST 47')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_48():
    print('TEST 48')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 79
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_49():
    print('TEST 49')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 77
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_50():
    print('TEST 50')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_51():
    print('TEST 51')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 69
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_52():
    print('TEST 52')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 87
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_53():
    print('TEST 53')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_54():
    print('TEST 54')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_55():
    print('TEST 55')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 70
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_56():
    print('TEST 56')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 14
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_57():
    print('TEST 57')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_58():
    print('TEST 58')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 92
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_59():
    print('TEST 59')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_60():
    print('TEST 60')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 71
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_61():
    print('TEST 61')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 53
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 13
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_62():
    print('TEST 62')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 96
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_63():
    print('TEST 63')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_64():
    print('TEST 64')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 88
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_65():
    print('TEST 65')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_66():
    print('TEST 66')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_67():
    print('TEST 67')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 51
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_68():
    print('TEST 68')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 55
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_69():
    print('TEST 69')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_70():
    print('TEST 70')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 87
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_71():
    print('TEST 71')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_72():
    print('TEST 72')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 87
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 63
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_73():
    print('TEST 73')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 77
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_74():
    print('TEST 74')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 53
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 96
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_75():
    print('TEST 75')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 82
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 24
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_76():
    print('TEST 76')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 97
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_77():
    print('TEST 77')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 97
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_78():
    print('TEST 78')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 28
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_79():
    print('TEST 79')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 42
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_80():
    print('TEST 80')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_81():
    print('TEST 81')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 69
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_82():
    print('TEST 82')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_83():
    print('TEST 83')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_84():
    print('TEST 84')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_85():
    print('TEST 85')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_86():
    print('TEST 86')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 77
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_87():
    print('TEST 87')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_88():
    print('TEST 88')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_89():
    print('TEST 89')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_90():
    print('TEST 90')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 82
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_91():
    print('TEST 91')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_92():
    print('TEST 92')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 20
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_93():
    print('TEST 93')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 100
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_94():
    print('TEST 94')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 53
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_95():
    print('TEST 95')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 93
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_96():
    print('TEST 96')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 65
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 85
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_97():
    print('TEST 97')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_98():
    print('TEST 98')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 31
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 74
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_99():
    print('TEST 99')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_100():
    print('TEST 100')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 82
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 77
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_101():
    print('TEST 101')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
76.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
76.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_102():
    print('TEST 102')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
47.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 69
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_103():
    print('TEST 103')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
90.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_104():
    print('TEST 104')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 89
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
89.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
89.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
89.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_105():
    print('TEST 105')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
91.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_106():
    print('TEST 106')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 49
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
49.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
49.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_107():
    print('TEST 107')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 51
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
61.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
61.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_108():
    print('TEST 108')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
76.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_109():
    print('TEST 109')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 0
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_110():
    print('TEST 110')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
80.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_111():
    print('TEST 111')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 49
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_112():
    print('TEST 112')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 12
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_113():
    print('TEST 113')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 79
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
79.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_114():
    print('TEST 114')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 42
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
42.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
42.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 92
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_115():
    print('TEST 115')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
46.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
46.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
46.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_116():
    print('TEST 116')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
50.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
50.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_117():
    print('TEST 117')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 22
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 100
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
61.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_118():
    print('TEST 118')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_119():
    print('TEST 119')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 23
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
23.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_120():
    print('TEST 120')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 55
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 100
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 99
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_121():
    print('TEST 121')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 45
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 32
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
38.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_122():
    print('TEST 122')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 87
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 65
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_123():
    print('TEST 123')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 17
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
17.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_124():
    print('TEST 124')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 5
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
5.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
5.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_125():
    print('TEST 125')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 51
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
52.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 71
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_126():
    print('TEST 126')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_127():
    print('TEST 127')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
67.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_128():
    print('TEST 128')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 44
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 70
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_129():
    print('TEST 129')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 45
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
45.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
45.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
45.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_130():
    print('TEST 130')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_131():
    print('TEST 131')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 79
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
75.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
75.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_132():
    print('TEST 132')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 70
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_133():
    print('TEST 133')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 36
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
36.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_134():
    print('TEST 134')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_135():
    print('TEST 135')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 45
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
45.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_136():
    print('TEST 136')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 77
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_137():
    print('TEST 137')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 94
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
74.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 54
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_138():
    print('TEST 138')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
75.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
75.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 74
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_139():
    print('TEST 139')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 58
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 19
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_140():
    print('TEST 140')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
71.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
71.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_141():
    print('TEST 141')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
46.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 14
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_142():
    print('TEST 142')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 56
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_143():
    print('TEST 143')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
41.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_144():
    print('TEST 144')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_145():
    print('TEST 145')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 89
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
89.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_146():
    print('TEST 146')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
48.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_147():
    print('TEST 147')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 85
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_148():
    print('TEST 148')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 85
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
85.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
59.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
59.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_149():
    print('TEST 149')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 66
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 69
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
69.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_150():
    print('TEST 150')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
84.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_151():
    print('TEST 151')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 74
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
60.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_152():
    print('TEST 152')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 41
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 51
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 90
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_153():
    print('TEST 153')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 26
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
26.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
26.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
26.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_154():
    print('TEST 154')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_155():
    print('TEST 155')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 80
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
80.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_156():
    print('TEST 156')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
40.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
59.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 93
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_157():
    print('TEST 157')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 59
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.33333333333333
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
3
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_158():
    print('TEST 158')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 19
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 73
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 95
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
95.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
95.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_159():
    print('TEST 159')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 70
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 92
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_160():
    print('TEST 160')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 42
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 49
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 92
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_161():
    print('TEST 161')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 23
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 72
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 74
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
62.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_162():
    print('TEST 162')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_163():
    print('TEST 163')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
76.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_164():
    print('TEST 164')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
86.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_165():
    print('TEST 165')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 71
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
77.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_166():
    print('TEST 166')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 66
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
70.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_167():
    print('TEST 167')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 17
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_168():
    print('TEST 168')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 45
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_169():
    print('TEST 169')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 66
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
66.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_170():
    print('TEST 170')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
83.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_171():
    print('TEST 171')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
61.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_172():
    print('TEST 172')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 97
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 99
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 86
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_173():
    print('TEST 173')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 43
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_174():
    print('TEST 174')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_175():
    print('TEST 175')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
84.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 40
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_176():
    print('TEST 176')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 85
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_177():
    print('TEST 177')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 58
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 82
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 97
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_178():
    print('TEST 178')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 48
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 167
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 42
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 55
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_179():
    print('TEST 179')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 89
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 644
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 671
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_180():
    print('TEST 180')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 63
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 810
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 277
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 50
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_181():
    print('TEST 181')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 529
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 516
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_182():
    print('TEST 182')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 270
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 81
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 251
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 89
B
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_183():
    print('TEST 183')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: kuykszo
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: dte
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 65
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: k7r8ma27j2
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_184():
    print('TEST 184')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 6a3ouze
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: xp1yex
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_185():
    print('TEST 185')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 68
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 16
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 19
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_186():
    print('TEST 186')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 66
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 47
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: humyt
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 5
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_187():
    print('TEST 187')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 98fkxxdq
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: vq35fim
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 61
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_188():
    print('TEST 188')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: mkdatzjbh
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: zjf2d
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: cpt
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 76
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_189():
    print('TEST 189')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: ht5
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: v8o5yy1ym
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_190():
    print('TEST 190')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 464
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: uatpx1z
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_191():
    print('TEST 191')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 339
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 57
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 583
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_192():
    print('TEST 192')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 871
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: tzc
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 197
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_193():
    print('TEST 193')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 55
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
55.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
55.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_194():
    print('TEST 194')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 381
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: w2rzf49mrp
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 381
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 407
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 60
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_195():
    print('TEST 195')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: gk2n5
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 912
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 140
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
52.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 614
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 452
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 1ht9
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 471
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_196():
    print('TEST 196')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 627
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: yq4
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 64
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: tyqo1twy4
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 871
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 129
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
64.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 75
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 46
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
60.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 865
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 78
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
78.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 91
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 83kmjo99u
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
84.5
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_197():
    print('TEST 197')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 4hflp2
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 264
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
52.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
52.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 353
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: cg3npsvyf7
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: l52wdv
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 708
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 7nr
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_198():
    print('TEST 198')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 907
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: ex3qe4
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 99
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 65
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
65.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 67
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 62
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: wrnnin
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
64.66666666666667
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_199():
    print('TEST 199')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: ag
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 197
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: c
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 312
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 14
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
14.0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 283
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 63
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: gg4wd
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 49
F
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

def test_200():
    print('TEST 200')
    return generic_test('''
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: ryimjh12i
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 422
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: a
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 79
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 429
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 97
A
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
0
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 470
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 931
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 840
out of range
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 52
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: r
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: A
no scores entered
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: R
reset
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 51
D
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
1
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: 84
C
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: m1jf
bad input
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: C
2
enter 0 to 100, or a special command [q:quit, r:reset, c:count, a:average]: q
done
'''.strip())

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

# these call student functions
def runTests():
    tests = []
    predicate = lambda f: isfunction(f) and f.__module__ == __name__
    fns = [row for row in getmembers(sys.modules[__name__], predicate = predicate) if row[0].startswith('test_')]
    fns.sort(key=lambda row: int(row[0].split('_')[-1]))
    for name, fn in fns:
        try:
            print('='*40)
            result = fn()
            print('\nRESULT: %s\n' % result)
            tests.append({'test': name, 'result': result})
        except Exception as e:
            print('\nTip from 301 instructors: try running just %s() in interactive mode to debug this issue.\n\n' % name)
            raise e
    return tests

def main():
    result = {'score': 0, 'tests': []}
    result['tests'] += runTests()

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
    main()
