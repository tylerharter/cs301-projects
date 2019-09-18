import ast, os, sys, subprocess, json, re, collections, math

PASS = "PASS"
TEXT_FORMAT = "text"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),    
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": "12",
    "2": "55.215007260000014",
    "3": "26.655754419999994",
    "4": "68.06346877",
    "5": "77.87553504",
    "6": "68.06346877",
    "7": "16.96543425",
    "8": "18.371421039999998",
    "9": "27.013047475",
    "10": "52.5162449575",
    "11": "7.224961934351909",
    "12": "3.2706887566666674",
    "13": "4.627587380000023",
    "14": "-0.2148440299999983",
    "15": "20.80494298333333",
    "16": "98.55499483333321",
    "17": "77.95994753999969",
    "18": "-2.0353479350000327",
    "19": "6.149171779999982",
    "20": "1.0848913984858986",
}



# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# find correct python command based on version 
def get_python_cmd():
    cmds = ['py', 'python3', 'python']
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd + ' -V', shell=True, universal_newlines=True)
            m = re.match(r'Python\s+(\d+\.\d+)\.*\d*', out)
            if m:
                if float(m.group(1)) >= 3.6:
                    return cmd
        except subprocess.CalledProcessError:
            pass
    else:
        return ''

# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-301-test.ipynb'

    # re-execute it from the beginning
    py_cmd = get_python_cmd()
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    if py_cmd:
        cmd = py_cmd + ' -m ' + cmd
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook) as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get('text/plain', [])
        if lines:
            actual_lines = lines
            break
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines).strip().strip("'")
    expected = expected_json[str(qnum)].strip().strip("'")
    try:
        actual_float = float(actual)
        expected_float = float(expected)
        if not math.isclose(actual_float, expected_float, rel_tol=1e-06, abs_tol=1e-03):
            return "found {} in {} but expected {}".format(actual, location_name, expected)
    except Exception as e:
        if actual != expected:
            return 'found {} but expected {}'.format(actual, expected)
    return PASS


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)

    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def linter_severe_check(nb):
    issues = []
    func_names = set()
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        code = "\n".join(cell.get('source', []))
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    if name in func_names:
                        issues.append('name <%s> reused for multiple functions' % name)
                    func_names.add(name)
        except Exception as e:
            print('Linter error: ' + str(e))

    return issues


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    if not os.path.exists(orig_notebook):
        print("File not found: " + orig_notebook)
        print("\nIf your file is named something other than main.ipynb, you can specify that by replacing '<notebook.ipynb>' with the name you chose:\n")
        print("python test.py <notebook.ipynb>")
        sys.exit(1)
        
    nb = rerun_notebook(orig_notebook)

    # check for sever linter errors
    issues = linter_severe_check(nb)
    if issues:
        print("\nPlease fix the following, then rerun the tests:")
        for issue in issues:
            print(' - ' + issue)
        print("")
        sys.exit(1)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
