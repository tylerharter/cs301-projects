# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math, ast
from datetime import datetime

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
    "1": [
         'Argentina',
         'Australia',
         'Austria',
         'Bulgaria',
         'Canada',
         'Chile',
         'Croatia',
         'France',
         'Germany',
         'Greece',
         'Hungary',
         'India',
         'Israel',
         'Italy',
         'Moldova',
         'Morocco',
         'New Zealand',
         'Portugal',
         'Romania',
         'Slovenia',
         'South Africa',
         'Spain',
         'US'
    ],
    "2": 39.407876230661039,
    "3": [
         'Garnacha Blanca',
         'Mencía',
         'Grenache-Syrah',
         'Sherry',
         'Garnacha',
         'Tinta de Toro',
         'Albariño',
         'Godello',
         'Tempranillo Blend',
         'White Blend',
         'Palomino',
         'Sparkling Blend',
         'Monastrell',
         'Red Blend',
         'Tempranillo',
         'Moscatel'
    ],
    "4": ['Andrew Murray',
          'Tetra',
          'Adelaida Cellars',
          'Laird',
          'MCV',
          'Beronia',
          'Hawk Watch Winery',
          'Montes',
          'Château Pégau',
          'Clos La Chance',
          'Sevtap',
          'Fess Parker',
          'Palmeri'],
    "5": ['Heron Hill',
          'Quinta Nova de Nossa Senhora do Carmo',
          'Dr. H. Thanisch (Erben Thanisch)',
          'MCV',
          'Bürgermeister Willi Schweinhardt',
          'Fattoria di Magliano',
          'Domaine Ostertag',
          'Domaine Collotte',
          'Byron',
          'Domaine Allimant-Laugner',
          'Margerum',
          'Sheldrake Point',
          'Benoît Girard',
          'Santa Cruz Mountain Vineyard',
          'Brander',
          'Concha y Toro',
          'Stephen Ross'],
    "6": ['Palacio del Burgo',
          'Val de Los Frailes',
          'Maurodos',
          'Bodega Carmen Rodríguez',
          'Matarromera'],
    "7": ['Cabernet Sauvignon'],
    "8": ['Tempranillo Blend'],
    "9": ['Pinot Noir', 'Cabernet Sauvignon', 'Sauvignon Blanc'],
    "10": ['Tinta de Toro'],
    "11": 2.183421985815603,
    "12": 1.288074888074888,
    "13": 'Felton Road',
    "14": 'Heggies Vineyard',
    "15": 'Burrowing Owl',
    "16": ['Portuguese White', 'Portuguese Rosé', 'Portuguese Red'],
    "17": ['Portuguese Red', 'Portuguese White'],
    "18": ['Touriga Nacional', 'Portuguese Sparkling', 'Portuguese Red'],
    "19": 66.6666666666666,
    "20": 33.3333333333333,
}



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
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
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
    actual = ''.join(actual_lines)
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        extra = set(actual) - set(expected)
        missing = set(expected) - set(actual)
        if extra:
            return "found unexpected entry in list: %s" % repr(list(extra)[0])
        elif missing:
            return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
        elif len(actual) != len(expected):
            return "expected %d entries in the list but found %d" % (len(expected), len(actual))
    else:
        if expected != actual:
            expected_mismatch = True
            
    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

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


def file_age(filename):
    try:
        t = os.path.getmtime(filename)
        return int((datetime.now() - datetime.fromtimestamp(t)).total_seconds())
    except:
        return 0


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # does notebook exist?  Is it fresh?
    if not os.path.exists(orig_notebook):
        print("Could not find file: %s" % orig_notebook)
        return

    age = file_age(orig_notebook)
    if age > 30:
        print()
        print("#"*80)
        print("# " + ("WARNING!  Your notebook file is %d seconds old." % age).ljust(77) + "#")
        print("#" + " "*78 + "#")
        print("# " + ("That's not necessarily bad, but if you were just changing your code, you").ljust(77) + "#")
        print("# " + ("probably forgot to save your work before running the tests.").ljust(77) + "#")
        print("#"*80)
        print()

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

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

