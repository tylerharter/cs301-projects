# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math, ast

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
    "1": 'B. Richardson',
    "2": 'Cristiano Ronaldo',
    "3": 'Neymar',
    "4": 'Paris Saint-Germain',
    "5": ['Portugal', 'Argentina', 'Brazil', 'Uruguay', 'Germany'],
    "6": ['A. Abbas', 'A. Abbas', 'A. Abdallah', 'A. Abdennour', 'A. Abdi'],
    "7": 2407282.6149178543,
    "8": 25.133264640219817,
    "9": 355,
    "10": 800,
    "11": "England",
    "12": {'Id': '20801',
            'name': 'Cristiano Ronaldo',
            'Age': 32.0,
            'nationality': 'Portugal',
            'club': 'Real Madrid CF',
            'league': 'Spanish Primera División',
            'euro_wage': 565000.0,
            'networth': 95500000.0,
            'score_of_100': 94.0},
    "13": {'Id': '190871',
            'name': 'Neymar',
            'Age': 25.0,
            'nationality': 'Brazil',
            'club': 'Paris Saint-Germain',
            'league': 'French Ligue 1',
            'euro_wage': 280000.0,
            'networth': 123000000.0,
            'score_of_100': 92.0},
    "14": {'Id': '158023',
            'name': 'L. Messi',
            'Age': 30.0,
            'nationality': 'Argentina',
            'club': 'FC Barcelona',
            'league': 'Spanish Primera División',
            'euro_wage': 565000.0,
            'networth': 105000000.0,
            'score_of_100': 93.0},
    "15": {'Id': '192985',
            'name': 'K. De Bruyne',
            'Age': 26.0,
            'nationality': 'Belgium',
            'club': 'Manchester City',
            'league': 'English Premier League',
            'euro_wage': 285000.0,
            'networth': 83000000.0,
            'score_of_100': 89.0},
    "16": {'Portugal': 355,
            'Argentina': 948,
            'Brazil': 800,
            'Uruguay': 150,
            'Germany': 1132,
            'Poland': 332,
            'Spain': 995,
            'Belgium': 260,
            'Chile': 367,
            'Croatia': 107,
            'Wales': 122,
            'Italy': 792,
            'Slovenia': 62,
            'France': 962,
            'Gabon': 12,
            'Sweden': 366,
            'Netherlands': 425,
            'Denmark': 343,
            'Slovakia': 64,
            'England': 1582,
            'Colombia': 589,
            'Austria': 262,
            'Greece': 95,
            'Czech Republic': 63,
            'Costa Rica': 29,
            'Armenia': 14,
            'Bosnia Herzegovina': 55,
            'Ivory Coast': 94,
            'Senegal': 126,
            'Switzerland': 228,
            'Morocco': 77,
            'Guinea': 25,
            'Egypt': 20,
            'Algeria': 56,
            'Cameroon': 78,
            'Serbia': 132,
            'Japan': 469,
            'Turkey': 288,
            'Ecuador': 25,
            'Montenegro': 25,
            'Korea Republic': 316,
            'Kenya': 7,
            'Iceland': 52,
            'Mexico': 360,
            'Norway': 329,
            'DR Congo': 57,
            'Ukraine': 49,
            'Russia': 305,
            'Finland': 60,
            'Republic of Ireland': 408,
            'United States': 379,
            'Venezuela': 41,
            'Ghana': 113,
            'Uzbekistan': 5,
            'Nigeria': 126,
            'Canada': 49,
            'Paraguay': 60,
            'Romania': 49,
            'Albania': 35,
            'Burkina Faso': 14,
            'Cape Verde': 22,
            'New Zealand': 30,
            'Northern Ireland': 85,
            'Syria': 4,
            'Scotland': 291,
            'Bulgaria': 20,
            'Peru': 16,
            'Angola': 15,
            'Australia': 222,
            'South Africa': 62,
            'Jamaica': 37,
            'Tunisia': 31,
            'Mozambique': 3,
            'Iran': 17,
            'Mali': 46,
            'Cuba': 2,
            'Hungary': 24,
            'Belarus': 9,
            'Saudi Arabia': 321,
            'Israel': 12,
            'Benin': 14,
            'Georgia': 31,
            'Dominican Republic': 3,
            'Lithuania': 12,
            'Kosovo': 32,
            'Moldova': 6,
            'Togo': 8,
            'FYR Macedonia': 17,
            'Guinea Bissau': 15,
            'Honduras': 13,
            'Congo': 21,
            'Chad': 2,
            'Curacao': 11,
            'Sierra Leone': 9,
            'Gambia': 15,
            'Iraq': 8,
            'Trinidad & Tobago': 9,
            'Zimbabwe': 10,
            'Cyprus': 11,
            'Niger': 3,
            'Liechtenstein': 3,
            'Oman': 1,
            'Tanzania': 2,
            'Zambia': 7,
            'Libya': 2,
            'Haiti': 14,
            'Madagascar': 4,
            'Estonia': 8,
            'Guatemala': 1,
            'New Caledonia': 2,
            'Korea DPR': 6,
            'Bermuda': 4,
            'Comoros': 9,
            'Panama': 16,
            'Palestine': 4,
            'Latvia': 6,
            'Equatorial Guinea': 6,
            'Eritrea': 1,
            'Luxembourg': 8,
            'Kuwait': 2,
            'Suriname': 3,
            'Uganda': 4,
            'Mauritania': 2,
            'El Salvador': 2,
            'Central African Rep.': 4,
            'Azerbaijan': 7,
            'St Kitts Nevis': 3,
            'Fiji': 1,
            'Guam': 1,
            'Lebanon': 5,
            'Qatar': 6,
            'Philippines': 3,
            'China PR': 4,
            'Somalia': 1,
            'Kazakhstan': 3,
            'Bolivia': 2,
            'Montserrat': 4,
            'Ethiopia': 2,
            'Mauritius': 1,
            'Liberia': 2,
            'Puerto Rico': 2,
            'Namibia': 2,
            'Faroe Islands': 6,
            'Guyana': 5,
            'Thailand': 2,
            'Barbados': 1,
            'Antigua & Barbuda': 4,
            'Gibraltar': 2,
            'São Tomé & Príncipe': 1,
            'Grenada': 1,
            'Belize': 1,
            'Burundi': 1,
            'Turkmenistan': 1,
            'Swaziland': 1,
            'Malta': 3,
            'St Lucia': 1,
            'Sudan': 2,
            'Vietnam': 1,
            'Afghanistan': 3,
            'Sri Lanka': 1,
            'Kyrgyzstan': 1,
            'San Marino': 1,
            'Hong Kong': 1},
    "17": {'Spanish Primera División': 582,
            'French Ligue 1': 589,
            'German Bundesliga': 523,
            'English Premier League': 634,
            'Italian Serie A': 554,
            'Turkish Süper Lig': 493,
            'Portuguese Primeira Liga': 503,
            'USA Major League Soccer': 624,
            'Russian Premier League': 447,
            'Ukrainian Premier League': 24,
            'Holland Eredivisie': 484,
            'Mexican Liga MX': 515,
            'Argentinian Superliga': 771,
            'Japanese J1 League': 518,
            'Belgian First Division A': 430,
            'Czech Liga': 27,
            'Saudi Professional League': 405,
            'Greek Super League': 109,
            'Swiss Super League': 257,
            'Colombian Primera A': 551,
            'English Championship': 706,
            'Spanish Segunda División': 624,
            'Chilian Primera División': 320,
            'Campeonato Brasileiro Série A': 320,
            'Swedish Allsvenskan': 385,
            'South African PSL': 51,
            'French Ligue 2': 535,
            'Scottish Premiership': 310,
            'Australian A-League': 226,
            'German 2. Bundesliga': 509,
            'Austrian Bundesliga': 255,
            'Polish Ekstraklasa': 414,
            'Italian Serie B': 618,
            'Korean K League Classic': 322,
            'Danish Superliga': 362,
            'Norwegian Eliteserien': 392,
            'English League One': 641,
            'German 3. Liga': 513,
            'English League Two': 615,
            'Finnish Veikkausliiga': 27,
            'Rep. Ireland Premier Division': 284},
    "18": {'Spanish Primera División': 37104.810996563574,
            'French Ligue 1': 20843.803056027165,
            'German Bundesliga': 31177.820267686424,
            'English Premier League': 58705.047318611985,
            'Italian Serie A': 35981.94945848375,
            'Turkish Süper Lig': 16582.150101419877,
            'Portuguese Primeira Liga': 7570.576540755467,
            'USA Major League Soccer': 4052.8846153846152,
            'Russian Premier League': 19612.97539149888,
            'Ukrainian Premier League': 1000.0,
            'Holland Eredivisie': 6842.975206611571,
            'Mexican Liga MX': 14885.436893203883,
            'Argentinian Superliga': 6832.684824902723,
            'Japanese J1 League': 3030.8880308880307,
            'Belgian First Division A': 8953.488372093023,
            'Czech Liga': 1000.0,
            'Saudi Professional League': 8928.395061728395,
            'Greek Super League': 1000.0,
            'Swiss Super League': 6774.31906614786,
            'Colombian Primera A': 1916.5154264972778,
            'English Championship': 16702.54957507082,
            'Spanish Segunda División': 5915.0641025641025,
            'Chilian Primera División': 4800.0,
            'Campeonato Brasileiro Série A': 15515.625,
            'Swedish Allsvenskan': 2218.181818181818,
            'South African PSL': 1000.0,
            'French Ligue 2': 3330.841121495327,
            'Scottish Premiership': 7154.8387096774195,
            'Australian A-League': 3092.920353982301,
            'German 2. Bundesliga': 7766.2082514734775,
            'Austrian Bundesliga': 6054.901960784314,
            'Polish Ekstraklasa': 3190.8212560386473,
            'Italian Serie B': 3788.0258899676373,
            'Korean K League Classic': 3043.478260869565,
            'Danish Superliga': 5102.209944751381,
            'Norwegian Eliteserien': 1936.2244897959183,
            'English League One': 3663.0265210608422,
            'German 3. Liga': 1136.4522417153996,
            'English League Two': 3068.2926829268295,
            'Finnish Veikkausliiga': 1000.0,
            'Rep. Ireland Premier Division': 1049.2957746478874},
    "19": {'Spanish Primera División': 25.015463917525775,
            'French Ligue 1': 24.31239388794567,
            'German Bundesliga': 24.137667304015295,
            'English Premier League': 24.832807570977916,
            'Italian Serie A': 25.21119133574007,
            'Turkish Süper Lig': 26.4868154158215,
            'Portuguese Primeira Liga': 25.05765407554672,
            'USA Major League Soccer': 26.009615384615383,
            'Russian Premier League': 25.55704697986577,
            'Ukrainian Premier League': 25.958333333333332,
            'Holland Eredivisie': 23.264462809917354,
            'Mexican Liga MX': 25.833009708737865,
            'Argentinian Superliga': 25.325551232166017,
            'Japanese J1 League': 26.65057915057915,
            'Belgian First Division A': 24.05581395348837,
            'Czech Liga': 27.333333333333332,
            'Saudi Professional League': 25.760493827160495,
            'Greek Super League': 25.339449541284402,
            'Swiss Super League': 24.136186770428015,
            'Colombian Primera A': 25.76043557168784,
            'English Championship': 24.923512747875353,
            'Spanish Segunda División': 25.05128205128205,
            'Chilian Primera División': 28.975,
            'Campeonato Brasileiro Série A': 28.975,
            'Swedish Allsvenskan': 24.97142857142857,
            'South African PSL': 26.80392156862745,
            'French Ligue 2': 24.82429906542056,
            'Scottish Premiership': 24.625806451612902,
            'Australian A-League': 25.52654867256637,
            'German 2. Bundesliga': 24.557956777996072,
            'Austrian Bundesliga': 24.094117647058823,
            'Polish Ekstraklasa': 25.70048309178744,
            'Italian Serie B': 25.042071197411005,
            'Korean K League Classic': 26.267080745341616,
            'Danish Superliga': 24.26795580110497,
            'Norwegian Eliteserien': 24.252551020408163,
            'English League One': 24.279251170046802,
            'German 3. Liga': 24.142300194931774,
            'English League Two': 24.357723577235774,
            'Finnish Veikkausliiga': 23.59259259259259,
            'Rep. Ireland Premier Division': 24.010563380281692},
    "20": "Chilian Primera División",
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
