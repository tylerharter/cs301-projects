# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math

PASS = "PASS"
TEXT_FORMAT = "text"
Question = collections.namedtuple("Question", ["number", "weight", "format"])

# group_weights = {
#     "test_get_value": 5,
#     "test_get_value": 2,
#     "test_get_highest_paid": 5,
#     "test_get_highest_worth": 5,
#     "test_get_column": 5,
#     "test_get_sorted": 3,
#     "test_avg_networth": 3,
#     "test_least_avg_age": 6,
#     "test_player_count": 4,
#     "test_max_players": 8,
#     "test_age_limit": 5,
#     "test_compare_clubs": 6,
#     "test_compare_clubs": 3,
#     "test_get_dictionary": 5,
#     "test_get_unique_element_list": 6,
#     "test_high_paying_clubs": 6,
#     "test_output_nat_club": 5,
#     "test_club_List": 5,
#     "test_best_scores_players": 8,
#     "test_find_savings": 5
# }



questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=0.4, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=0.6, format=TEXT_FORMAT),
    Question(number=7, weight=0.6, format=TEXT_FORMAT),
    Question(number=8, weight=1.2, format=TEXT_FORMAT),
    Question(number=9, weight=0.8, format=TEXT_FORMAT),
    Question(number=10, weight=1.6, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1.2, format=TEXT_FORMAT),
    Question(number=13, weight=0.6, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1.2, format=TEXT_FORMAT),
    Question(number=16, weight=1.2, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1.6, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),    
]
question_nums = set([q.number for q in questions])


# JSON and plaintext values
expected_json = {
    "1": 'Argentina',
    "2": 'out_of_bounds',
    "3": 'Cristiano Ronaldo',
    "4": ('Neymar', '190871'),
    "5": ['Portugal', 'Argentina', 'Brazil', 'Uruguay', 'Germany'],
    "6": ['A. Abbas', 'A. Abbas', 'A. Abdallah', 'A. Abdennour', 'A. Abdi'],
    "7": "2407282.6149178543",
    "8": 'Belgium',
    "9": '355',
    "10": ('England', 1582),
    "11": [
        'C. Pulisic',
 'J. González',
 'C. Carter-Vickers',
 'T. Redding',
 'D. Acosta',
 'T. Adams',
 'J. Glad',
 'S. Moore',
 'E. Palmer-Brown',
 'B. Lennon',
 'G. Zelalem',
 'D. Jones',
 'J. Yueill',
 'P. Pomykal',
 'M. Farfan',
 'B. Vazquez',
 'B. Jamieson IV',
 'W. McKennie',
 'A. Carleton',
 'M. Robinson',
 'O. Gaines',
 'J. Lewis',
 'P. Da Silva',
 'J. Torres',
 'J. Klinsmann',
 'A. Obinwa',
 'H. Wright',
 'J. Ebobisse',
 'B. Swanson',
 'S. Saucedo',
 'K. Scott',
 'I. Young',
 'C. Craft',
 'C. Calvert',
 'A. Trusty',
 'D. Mihailovic',
 'J. Soñora',
 'R. Cannon',
 'C. Durkin',
 'H. Arellano',
 'L. de la Torre',
 'C. Fernandez',
 'C. Goslin',
 'E. Sabbi',
 'C. Lucatero',
 'B. Scott'],
    "12": 'FC Barcelona',
    "13": 'Chelsea',
    "14": [
        {'name': 'Cristiano Ronaldo',
  'club': 'Real Madrid CF',
  'nationality': 'Portugal',
  'networth': 95500000.0},
 {'name': 'L. Messi',
  'club': 'FC Barcelona',
  'nationality': 'Argentina',
  'networth': 105000000.0},
 {'name': 'Neymar',
  'club': 'Paris Saint-Germain',
  'nationality': 'Brazil',
  'networth': 123000000.0},
 {'name': 'L. Suárez',
  'club': 'FC Barcelona',
  'nationality': 'Uruguay',
  'networth': 97000000.0},
 {'name': 'M. Neuer',
  'club': 'FC Bayern Munich',
  'nationality': 'Germany',
  'networth': 61000000.0},
 {'name': 'R. Lewandowski',
  'club': 'FC Bayern Munich',
  'nationality': 'Poland',
  'networth': 92000000.0},
 {'name': 'De Gea',
  'club': 'Manchester United',
  'nationality': 'Spain',
  'networth': 64500000.0},
 {'name': 'E. Hazard',
  'club': 'Chelsea',
  'nationality': 'Belgium',
  'networth': 90500000.0},
 {'name': 'T. Kroos',
  'club': 'Real Madrid CF',
  'nationality': 'Germany',
  'networth': 79000000.0},
 {'name': 'G. Higuaín',
  'club': 'Juventus',
  'nationality': 'Argentina',
  'networth': 77000000.0}
    ],
    "15": ['Spanish Primera División',
 'French Ligue 1',
 'German Bundesliga',
 'English Premier League',
 'Italian Serie A',
 'Turkish Süper Lig',
 'Portuguese Primeira Liga',
 'USA Major League Soccer',
 'Russian Premier League',
 'Ukrainian Premier League',
 'Holland Eredivisie',
 'Mexican Liga MX',
 'Argentinian Superliga',
 'Japanese J1 League',
 'Belgian First Division A',
 'Czech Liga',
 'Saudi Professional League',
 'Greek Super League',
 'Swiss Super League',
 'Colombian Primera A',
 'English Championship',
 'Spanish Segunda División',
 'Chilian Primera División',
 'Campeonato Brasileiro Série A',
 'Swedish Allsvenskan',
 'South African PSL',
 'French Ligue 2',
 'Scottish Premiership',
 'Australian A-League',
 'German 2. Bundesliga',
 'Austrian Bundesliga',
 'Polish Ekstraklasa',
 'Italian Serie B',
 'Korean K League Classic',
 'Danish Superliga',
 'Norwegian Eliteserien',
 'English League One',
 'German 3. Liga',
 'English League Two',
 'Finnish Veikkausliiga',
 'Rep. Ireland Premier Division'],
    "16": ['Real Madrid CF',
 'FC Barcelona',
 'Paris Saint-Germain',
 'FC Bayern Munich',
 'Manchester United',
 'Chelsea',
 'Juventus',
 'Manchester City',
 'Arsenal',
 'Atlético Madrid',
 'Borussia Dortmund',
 'Milan',
 'Tottenham Hotspur'],
    "17": {'nationalities': 163, 'clubs': 647},
    "18": ['FC Bayern Munich',
 'Borussia Dortmund',
 'Bayer 04 Leverkusen',
 'FC Köln',
 'FC Schalke 04',
 'RB Leipzig',
 'Borussia Mönchengladbach',
 'TSG 1899 Hoffenheim',
 'SV Werder Bremen',
 'VfL Wolfsburg',
 'Hertha BSC Berlin',
 'Eintracht Frankfurt',
 'Hannover 96',
 'FC Augsburg',
 'VfB Stuttgart',
 'Hamburger SV',
 'FSV Mainz 05',
 'SC Freiburg'],
    "19": ['E. Hazard'],
    "20": "4941040.0"}
           
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
    expected = expected_json[str(qnum)]
    try:
        import ast
        # Handling homogenous list of elements
        sorted_actual = sorted(ast.literal_eval(actual))
        sorted_expected = sorted(expected)
        if sorted_actual != sorted_expected:
            return "found {} but expected {}".format(sorted_actual, sorted_expected)
    except Exception as e:
        try:
            # Handling float value test cases
            actual_float = float(actual)
            expected_float = float(expected)
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                return "found {} in {} but expected {}".format(actual, location_name, expected)
        except:
            try:
                # Handling heterogenous list of elements
                actual_list = ast.literal_eval(actual)
                if actual_list[:-1] == expected[:-1] and actual_list != expected:
                    # Special case for #q20 handled:
                    if not math.isclose(actual_list[-1], expected[-1], rel_tol=1e-02, abs_tol=1e-02):
                        return 'found {} but expected {}'.format(actual, expected)  
            except:
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
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
