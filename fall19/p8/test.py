import ast
import os
import re
import sys
import json
import math
import collections

import nbconvert
import nbformat

PASS = "PASS"
TEXT_FORMAT = "text"
PNG_FORMAT = "png"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    #stage 1
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
    #stage 2
    Question(number=21, weight=1, format=TEXT_FORMAT),
    Question(number=22, weight=1, format=TEXT_FORMAT),
    Question(number=23, weight=1, format=TEXT_FORMAT),
    Question(number=24, weight=1, format=TEXT_FORMAT),
    Question(number=25, weight=1, format=TEXT_FORMAT),
    Question(number=26, weight=1, format=TEXT_FORMAT),
    Question(number=27, weight=1, format=TEXT_FORMAT),
    Question(number=28, weight=1, format=PNG_FORMAT),
    Question(number=29, weight=1, format=PNG_FORMAT),
    Question(number=30, weight=1, format=PNG_FORMAT),
    Question(number=31, weight=1, format=PNG_FORMAT),
    Question(number=32, weight=1, format=TEXT_FORMAT),
    Question(number=33, weight=1, format=TEXT_FORMAT),
    Question(number=34, weight=1, format=TEXT_FORMAT),
    Question(number=35, weight=1, format=TEXT_FORMAT),
    Question(number=36, weight=1, format=TEXT_FORMAT),
    Question(number=37, weight=1, format=TEXT_FORMAT),
    Question(number=38, weight=1, format=TEXT_FORMAT),
    Question(number=39, weight=1, format=TEXT_FORMAT),
    Question(number=40, weight=1, format=TEXT_FORMAT),
]

question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": {'nm0000131': 'John Cusack',
                  'nm0000154': 'Mel Gibson',
                  'nm0000163': 'Dustin Hoffman',
                  'nm0000418': 'Danny Glover',
                  'nm0000432': 'Gene Hackman',
                  'nm0000997': 'Gary Busey',
                  'nm0001149': 'Richard Donner',
                  'nm0001219': 'Gary Fleder',
                  'nm0752751': 'Mitchell Ryan',
                  'tt0313542': 'Runaway Jury',
                  'tt0093409': 'Lethal Weapon'},
    "2": 'Mitchell Ryan',
    "3": ['John Cusack','Mel Gibson','Dustin Hoffman','Danny Glover','Gene Hackman','Gary Busey','Richard Donner','Gary Fleder','Mitchell Ryan'],
    "4": ['nm0000997', 'nm0001219'],
    "5":[{'title': 'tt0313542',
  'year': 2003,
  'rating': 7.1,
  'directors': ['nm0001219'],
  'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'tt0093409',
  'year': 1987,
  'rating': 7.6,
  'directors': ['nm0001149'],
  'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
  'genres': ['Action', 'Crime', 'Thriller']}],
    "6":3,
    "7":'nm0752751',
    "8":'Runaway Jury',
    "9":['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
    "10":['Richard Donner'],
    "11":[{'title': 'Runaway Jury',
  'year': 2003,
  'rating': 7.1,
  'directors': ['Gary Fleder'],
  'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'Lethal Weapon',
  'year': 1987,
  'rating': 7.6,
  'directors': ['Richard Donner'],
  'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
  'genres': ['Action', 'Crime', 'Thriller']}],
    "12": [{'title': 'The Big Wedding',
  'year': 2013,
  'rating': 5.6,
  'directors': ['Justin Zackham'],
  'actors': ['Robert De Niro'],
  'genres': ['Comedy', 'Drama', 'Romance']},
 {'title': 'The Affair of the Necklace',
  'year': 2001,
  'rating': 6.1,
  'directors': ['Charles Shyer'],
  'actors': ['Simon Baker', 'Jonathan Pryce', 'Adrien Brody'],
  'genres': ['Drama', 'History', 'Romance']},
 {'title': 'The Barefoot Executive',
  'year': 1971,
  'rating': 6.0,
  'directors': ['Robert Butler'],
  'actors': ['Kurt Russell', 'Joe Flynn', 'Harry Morgan', 'Wally Cox'],
  'genres': ['Comedy', 'Family']}],
    "13": [{'title': 'Fortitude and Glory: Angelo Dundee and His Fighters',
    'year': 2012,
    'rating': 7.2,
    'directors': ['Chris Tasara'],
    'actors': ['Angelo Dundee', 'George Foreman', 'Freddie Roach'],
    'genres': ['Sport']},
    {'title': 'Ivanhoe',
    'year': 1952,
    'rating': 6.8,
    'directors': ['Richard Thorpe'],
    'actors': ['Robert Taylor', 'George Sanders'],
    'genres': ['Adventure', 'Drama', 'History']},
    {'title': 'The Great Gatsby',
    'year': 1949,
    'rating': 6.6,
    'directors': ['Elliott Nugent'],
    'actors': ['Alan Ladd', 'Macdonald Carey'],
  'genres': ['Drama']}],
    "14": [{'title': 'Arizona',
  'year': 1931,
  'rating': 6.0,
  'directors': ['George B. Seitz'],
  'actors': ['John Wayne', 'Forrest Stanley'],
  'genres': ['Drama', 'Romance']},
 {'title': 'City Lights',
  'year': 1931,
  'rating': 8.5,
  'directors': ['Charles Chaplin'],
  'actors': ['Charles Chaplin', 'Harry Myers'],
  'genres': ['Comedy', 'Drama', 'Romance']},
 {'title': 'The Range Feud',
  'year': 1931,
  'rating': 5.8,
  'directors': ['D. Ross Lederman'],
  'actors': ['Buck Jones', 'John Wayne', 'Edward LeSaint'],
  'genres': ['Mystery', 'Western']}],
    "15": [{'title': 'Texas Cyclone',
  'year': 1932,
  'rating': 6.2,
  'directors': ['D. Ross Lederman'],
  'actors': ['Wallace MacDonald', 'Tim McCoy', 'Wheeler Oakman', 'John Wayne'],
  'genres': ['Action', 'Western']},
 {'title': 'Haunted Gold',
  'year': 1932,
  'rating': 5.5,
  'directors': ['Mack V. Wright'],
  'actors': ['Otto Hoffman',
   'John Wayne',
   'Duke',
   'Harry Woods',
   'Erville Alderson'],
  'genres': ['Horror', 'Mystery', 'Western']},
 {'title': 'Girl Crazy',
  'year': 1932,
  'rating': 6.3,
  'directors': ['William A. Seiter'],
  'actors': ['Bert Wheeler', 'Robert Woolsey', 'Eddie Quillan'],
  'genres': ['Comedy']},
 {'title': 'Hot Saturday',
  'year': 1932,
  'rating': 6.6,
  'directors': ['William A. Seiter'],
  'actors': ['Cary Grant', 'Randolph Scott', 'Edward Woods'],
  'genres': ['Drama', 'Romance']},
 {'title': 'Lady and Gent',
  'year': 1932,
  'rating': 5.7,
  'directors': ['Stephen Roberts'],
  'actors': ['Morgan Wallace',
   'George Bancroft',
   'Charles Starrett',
   'James Gleason',
   'John Wayne'],
  'genres': ['Drama', 'Sport']},
 {'title': 'The Big Stampede',
  'year': 1932,
  'rating': 5.8,
  'directors': ['Tenny Wright'],
  'actors': ['John Wayne', 'Noah Beery', 'Paul Hurst'],
  'genres': ['Western']},
 {'title': 'The Shadow of the Eagle',
  'year': 1932,
  'rating': 5.8,
  'directors': ['B. Reeves Eason', 'Ford Beebe'],
  'actors': ['John Wayne', 'Walter Miller', 'Kenneth Harlan'],
  'genres': ['Crime', 'Drama', 'Mystery']},
 {'title': 'Ride Him, Cowboy',
  'year': 1932,
  'rating': 5.4,
  'directors': ['Fred Allen'],
  'actors': ['Otis Harlan', 'John Wayne', 'Duke', 'Henry B. Walthall'],
  'genres': ['Romance', 'Western']},
 {'title': "Smilin' Through",
  'year': 1932,
  'rating': 7.0,
  'directors': ['Sidney Franklin'],
  'actors': ['Fredric March', 'Leslie Howard', 'O.P. Heggie'],
  'genres': ['Drama', 'Romance']},
 {'title': 'The Hurricane Express',
  'year': 1932,
  'rating': 5.6,
  'directors': ['J.P. McGowan', 'Armand Schaefer'],
  'actors': ['Tully Marshall', 'Conway Tearle', 'John Wayne'],
  'genres': ['Action', 'Adventure', 'Crime']}],
    "16": 18,
    "17": 1247,
    "18": 'Shoulder Arms',
    "19": 6.401659528907912,
    "20": 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
    "21": {2018: [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
                    {'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']}],
            2019: [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
                     {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "22": {'short': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
                       {'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']}],
            'long': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
                       {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "23": {'g1': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
                    {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
            'g2': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
                     {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
            'g3': [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
                     {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "24": {'Crime': [{'title': 'Runaway Jury',
                         'year': 2003,
                         'rating': 7.1,
                         'directors': ['Gary Fleder'],
                         'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
                         'genres': ['Crime', 'Drama', 'Thriller']},
                       {'title': 'Lethal Weapon',
                           'year': 1987,
                           'rating': 7.6,
                           'directors': ['Richard Donner'],
                           'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
                           'genres': ['Action', 'Crime', 'Thriller']}],
            'Drama': [{'title': 'Runaway Jury',
                          'year': 2003,
                          'rating': 7.1,
                          'directors': ['Gary Fleder'],
                          'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
                          'genres': ['Crime', 'Drama', 'Thriller']}],
            'Thriller': [{'title': 'Runaway Jury',
                             'year': 2003,
                             'rating': 7.1,
                             'directors': ['Gary Fleder'],
                             'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
                             'genres': ['Crime', 'Drama', 'Thriller']},
                           {'title': 'Lethal Weapon',
                               'year': 1987,
                               'rating': 7.6,
                               'directors': ['Richard Donner'],
                               'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
                               'genres': ['Action', 'Crime', 'Thriller']}],
            'Action': [{'title': 'Lethal Weapon',
                           'year': 1987,
                           'rating': 7.6,
                           'directors': ['Richard Donner'],
                           'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
                           'genres': ['Action', 'Crime', 'Thriller']}]},
    "25": 7,
    "26": 2605,
    "27": {'Comedy': 485,
            'Drama': 1094,
            'Romance': 352,
            'History': 73,
            'Family': 85,
            'Mystery': 121,
            'Thriller': 250,
            'Action': 299,
            'Crime': 357,
            'Adventure': 283,
            'Western': 226,
            'Music': 38,
            'Animation': 45,
            'Sport': 48,
            'Fantasy': 59,
            'War': 99,
            'Sci-Fi': 69,
            'Horror': 85},
    "32": {'Howard Hawks': 42,
            'Charles Chaplin': 34,
            'Henry Hathaway': 36,
            'Stanley Kubrick': 46,
            'Taylor Hackford': 32,
            'Cecil B. DeMille': 30,
            'Lee H. Katzin': 30,
            'Richard Fleischer': 32,
            'Sidney Lumet': 33,
            'George Sherman': 33,
            'John Huston': 30,
            'Robert Siodmak': 30,
            'Eldar Ryazanov': 31,
            'Martin Ritt': 32},
    "33": {'Kurt Russell': 50,
             'Mickey Rooney': 75,
             'Robert Mitchum': 51,
             'Glenn Ford': 52,
             'James Caan': 52,
             'Anthony Quinn': 61,
             'George Burns': 60,
             'Dean Stockwell': 53},
    "34": [{'name': 'Stanley Kubrick', 'span': 46},
            {'name': 'Howard Hawks', 'span': 42},
            {'name': 'Henry Hathaway', 'span': 36},
            {'name': 'Charles Chaplin', 'span': 34},
            {'name': 'Sidney Lumet', 'span': 33},
            {'name': 'George Sherman', 'span': 33},
            {'name': 'Taylor Hackford', 'span': 32},
            {'name': 'Richard Fleischer', 'span': 32},
            {'name': 'Martin Ritt', 'span': 32},
            {'name': 'Eldar Ryazanov', 'span': 31}],
    "35": [{'name': 'Mickey Rooney', 'span': 75},
            {'name': 'Anthony Quinn', 'span': 61},
            {'name': 'George Burns', 'span': 60},
            {'name': 'Dean Stockwell', 'span': 53},
            {'name': 'Glenn Ford', 'span': 52},
            {'name': 'James Caan', 'span': 52},
            {'name': 'Robert Mitchum', 'span': 51},
            {'name': 'Kurt Russell', 'span': 50},
            {'name': 'Robert De Niro', 'span': 49},
            {'name': 'Marlon Brando', 'span': 49}],
    "36": [{'category': 'Animation', 'rating': 7.3, 'count': 45},
            {'category': 'History', 'rating': 6.7, 'count': 73},
            {'category': 'War', 'rating': 6.7, 'count': 99}],
    "37": [{'category': 1921, 'rating': 8.3, 'count': 1},
            {'category': 1925, 'rating': 8.2, 'count': 1},
            {'category': 1919, 'rating': 7.5, 'count': 1},
            {'category': 1923, 'rating': 7.3, 'count': 2},
            {'category': 1962, 'rating': 7.2, 'count': 17},
            {'category': 1964, 'rating': 7.1, 'count': 19},
            {'category': 1957, 'rating': 7.0, 'count': 24},
            {'category': 1985, 'rating': 7.0, 'count': 17},
            {'category': 1976, 'rating': 7.0, 'count': 17},
            {'category': 1963, 'rating': 6.95, 'count': 10}],
    "38": [{'category': 1962, 'rating': 7.2, 'count': 17},
            {'category': 1964, 'rating': 7.1, 'count': 19},
            {'category': 1957, 'rating': 7.0, 'count': 24},
            {'category': 1985, 'rating': 7.0, 'count': 17},
            {'category': 1976, 'rating': 7.0, 'count': 17}],
    "39": [{'category': 'Christopher Nolan', 'rating': 8.5, 'count': 9},
           {'category': 'Leonid Gayday', 'rating': 8.4, 'count': 5},
           {'category': 'Stanley Kubrick', 'rating': 8.3, 'count': 11},
           {'category': 'Sergio Leone', 'rating': 8.3, 'count': 7}],
    "40": [{'category': 'Henry Bergman', 'rating': 8.2, 'count': 5},
            {'category': 'Ioan Gruffudd', 'rating': 8.2, 'count': 6},
            {'category': 'Robert Lindsay', 'rating': 8.2, 'count': 6}],
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
    with open(orig_notebook, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=120, kernel_name='python3')
    try:
        out = ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    except nbconvert.preprocessors.CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % orig_notebook
        msg += 'See notebook "%s" for the traceback.' % new_notebook
        print(msg)
        raise
    finally:
        with open(new_notebook, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    # Note: Here we are saving and reloading, this isn't needed but can help student's debug

    # parse notebook
    with open(new_notebook, encoding='utf-8') as f:
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
    actual = ''.join(actual_lines)
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    # TODO: remove this hack!!!
    if qnum == 34 or qnum == 35:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            a = actual[i-1]["span"]
            b = actual[i]["span"]
            if a < b:
                return "bad sort: found a span of {} before a span of {}".format(a, b)
        expected = sorted(expected, key=lambda row: (-row["span"], row["name"]))
        actual = sorted(actual, key=lambda row: (-row["span"], row["name"]))

    # TODO: remove this hack!!!
    if 36 <= qnum <= 40:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            a = actual[i-1]["rating"]
            b = actual[i]["rating"]
            if a < b:
                return "bad sort: found a rating of {} before a rating of {}".format(a, b)
        expected = sorted(expected, key=lambda row: (-row["rating"], row["category"]))
        actual = sorted(actual, key=lambda row: (-row["rating"], row["category"]))
    
    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try: 
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
        except TypeError:
            # this happens when the list contains dicts.  Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    else:
        if expected != actual:
            expected_mismatch = True
            
    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def check_cell_png(qnum, cell):
    if qnum == 21:
        print('here')
        print(cell)
    for output in cell.get('outputs', []):
        if qnum == 21:
            print(output.get('data', {}).keys())
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
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

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
