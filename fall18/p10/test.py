import os, sys, subprocess, json, re, collections, math
from bs4 import BeautifulSoup

PASS = "PASS"
JSON_FORMAT = "json"
TEXT_FORMAT = "text"
HTML_FORMAT = "html"
PNG_FORMAT = "PNG"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=4, format=TEXT_FORMAT),
    Question(number=2, weight=4, format=TEXT_FORMAT),
    Question(number=3, weight=4, format=TEXT_FORMAT),
    Question(number=4, weight=3, format=JSON_FORMAT),
    Question(number=5, weight=3, format=JSON_FORMAT),
    Question(number=6, weight=3, format=HTML_FORMAT),
    Question(number=7, weight=3, format=HTML_FORMAT),
    Question(number=8, weight=2, format=TEXT_FORMAT),
    Question(number=9, weight=2, format=TEXT_FORMAT),
    Question(number=10, weight=2, format=TEXT_FORMAT),

    Question(number=11, weight=3, format=TEXT_FORMAT),
    Question(number=12, weight=3, format=TEXT_FORMAT),
    Question(number=13, weight=3, format=HTML_FORMAT),
    Question(number=14, weight=3, format=TEXT_FORMAT),
    Question(number=15, weight=3, format=HTML_FORMAT),
    Question(number=16, weight=3, format=HTML_FORMAT),
    Question(number=17, weight=3, format=HTML_FORMAT),
    Question(number=18, weight=3, format=HTML_FORMAT),
    Question(number=19, weight=3, format=HTML_FORMAT),
    Question(number=20, weight=3, format=HTML_FORMAT),

    Question(number=21, weight=4, format=PNG_FORMAT),
    Question(number=22, weight=4, format=PNG_FORMAT),
    Question(number=23, weight=4, format=PNG_FORMAT),
    Question(number=24, weight=4, format=PNG_FORMAT),
    Question(number=25, weight=4, format=HTML_FORMAT),
    Question(number=26, weight=3, format=PNG_FORMAT),
    Question(number=27, weight=3, format=PNG_FORMAT),
    Question(number=28, weight=3, format=PNG_FORMAT),
    Question(number=29, weight=3, format=PNG_FORMAT),
    Question(number=30, weight=8, format=PNG_FORMAT),
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = None
with open('expected.json') as f:
    expected_json = json.load(f)


# returns a dictionary
# key: (row index, column name)
# val: cell values
def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells


# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-301-test.ipynb'

    # re-execute it from the beginning
    cmd = 'jupyter nbconvert --execute {orig} --to notebook --output={new} --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=orig_notebook, new=new_notebook)
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
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines).strip().strip("'")
    expected = expected_json[str(qnum)].strip().strip("'")
    try:
        actual_float = float(actual)
        expected_float = float(expected)
        if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
            return "found {} in {} but expected {}".format(actual, location_name, expected)
    except Exception as e:
        if actual != expected:
            return 'found {} but expected {}'.format(actual, expected)
    return PASS


def check_cell_json(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = normalize_json(''.join(actual_lines))
    expected = normalize_json(expected_json[str(qnum)])
    if actual == expected:
        return PASS
    return 'mismatch'


def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return 'value missing for ' + location_name
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if math.isnan(actual_float) and math.isnan(expected_float):
                return PASS
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                print(type(actual_float), actual_float)
                return "found {} in {} but it was not close to expected {}".format(actual, location_name, expected)
        except Exception as e:
            if actual != expected:
                return "found '{}' in {} but expected '{}'".format(actual, location_name, expected)
    return PASS


def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)


def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == JSON_FORMAT:
        return check_cell_json(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    
    return PASS


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


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    nb = rerun_notebook(orig_notebook)

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
    print(json.dumps(results, indent=2))
    print('TOTAL SCORE: %.2f' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
