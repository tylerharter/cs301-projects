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
    "1": 'O. Pérez',
    "2": 'L. Messi',
    "3": 'Neymar Jr',
    "4": 'Paris Saint-Germain',
    "5": ['Argentina', 'Portugal', 'Brazil', 'Spain', 'Belgium'],
    "6": ['A. Abang', 'A. Abdellaoui', 'A. Abdennour', 'A. Abdi', 'A. Abdu Jaber'],
    "7": 2410695.8861976163,
    "8": 25.122205745043114,
    "9": 322,
    "10": 827,
    "11": "England",
    "12": {'Id': '20801',
            'Name': 'Cristiano Ronaldo',
            'Age': 33.0,
            'Nationality': 'Portugal',
            'Overall': 94.0,
            'Club': 'Juventus',
            'Value': '€77M',
            'Wage': '€405K',
            'Preferred Foot': 'Right',
            'Jersey Number': '7',
            'Height': "6'2",
            'Weight': '183lbs'},
    "13": {'Id': '190871',
            'Name': 'Neymar Jr',
            'Age': 26.0,
            'Nationality': 'Brazil',
            'Overall': 92.0,
            'Club': 'Paris Saint-Germain',
            'Value': '€118.5M',
            'Wage': '€290K',
            'Preferred Foot': 'Right',
            'Jersey Number': '10',
            'Height': "5'9",
            'Weight': '150lbs'},
    "14": {'Id': '158023',
            'Name': 'L. Messi',
            'Age': 31.0,
            'Nationality': 'Argentina',
            'Overall': 94.0,
            'Club': 'FC Barcelona',
            'Value': '€110.5M',
            'Wage': '€565K',
            'Preferred Foot': 'Left',
            'Jersey Number': '10',
            'Height': "5'7",
            'Weight': '159lbs'},
    "15": {'Id': '192985',
            'Name': 'K. De Bruyne',
            'Age': 27.0,
            'Nationality': 'Belgium',
            'Overall': 91.0,
            'Club': 'Manchester City',
            'Value': '€102M',
            'Wage': '€355K',
            'Preferred Foot': 'Right',
            'Jersey Number': '7',
            'Height': "5'11",
            'Weight': '154lbs'},
    "16": {'Argentina': 937,
            'Portugal': 322,
            'Brazil': 827,
            'Spain': 1072,
            'Belgium': 260,
            'Croatia': 126,
            'Uruguay': 149,
            'Slovenia': 55,
            'Poland': 350,
            'Germany': 1198,
            'France': 914,
            'England': 1662,
            'Italy': 702,
            'Egypt': 31,
            'Colombia': 618,
            'Denmark': 336,
            'Gabon': 15,
            'Wales': 129,
            'Senegal': 130,
            'Costa Rica': 30,
            'Slovakia': 54,
            'Netherlands': 453,
            'Bosnia Herzegovina': 61,
            'Morocco': 85,
            'Serbia': 126,
            'Algeria': 60,
            'Austria': 298,
            'Greece': 102,
            'Chile': 391,
            'Sweden': 397,
            'Korea Republic': 335,
            'Finland': 67,
            'Guinea': 31,
            'Montenegro': 23,
            'Armenia': 10,
            'Switzerland': 220,
            'Norway': 341,
            'Czech Republic': 100,
            'Scotland': 286,
            'Ghana': 114,
            'Central African Rep.': 3,
            'DR Congo': 52,
            'Ivory Coast': 100,
            'Russia': 79,
            'Ukraine': 73,
            'Iceland': 47,
            'Mexico': 366,
            'Jamaica': 32,
            'Albania': 40,
            'Venezuela': 67,
            'Japan': 478,
            'Turkey': 303,
            'Ecuador': 43,
            'Paraguay': 85,
            'Mali': 43,
            'Nigeria': 121,
            'Cameroon': 90,
            'Dominican Republic': 2,
            'Israel': 14,
            'Kenya': 10,
            'Hungary': 38,
            'Republic of Ireland': 368,
            'Romania': 54,
            'United States': 353,
            'Cape Verde': 19,
            'Australia': 236,
            'Peru': 37,
            'Togo': 12,
            'Syria': 9,
            'Zimbabwe': 13,
            'Angola': 15,
            'Burkina Faso': 16,
            'Iran': 17,
            'Estonia': 13,
            'Tunisia': 32,
            'Equatorial Guinea': 5,
            'New Zealand': 44,
            'FYR Macedonia': 20,
            'United Arab Emirates': 1,
            'China PR': 392,
            'Guinea Bissau': 15,
            'Bulgaria': 32,
            'Kosovo': 33,
            'South Africa': 71,
            'Madagascar': 12,
            'Georgia': 26,
            'Tanzania': 3,
            'Gambia': 15,
            'Cuba': 4,
            'Belarus': 4,
            'Uzbekistan': 2,
            'Benin': 15,
            'Congo': 25,
            'Mozambique': 4,
            'Honduras': 16,
            'Canada': 64,
            'Northern Ireland': 80,
            'Cyprus': 8,
            'Saudi Arabia': 340,
            'Curacao': 14,
            'Moldova': 5,
            'Bolivia': 30,
            'Trinidad & Tobago': 4,
            'Sierra Leone': 6,
            'Zambia': 9,
            'Chad': 2,
            'Philippines': 2,
            'Haiti': 10,
            'Comoros': 6,
            'Libya': 4,
            'Panama': 15,
            'São Tomé & Príncipe': 1,
            'Eritrea': 2,
            'Oman': 1,
            'Iraq': 7,
            'Burundi': 3,
            'Fiji': 1,
            'New Caledonia': 1,
            'Lithuania': 8,
            'Luxembourg': 8,
            'Korea DPR': 4,
            'Liechtenstein': 3,
            'St Kitts Nevis': 3,
            'Latvia': 6,
            'Suriname': 4,
            'Uganda': 6,
            'El Salvador': 5,
            'Bermuda': 2,
            'Kuwait': 1,
            'Antigua & Barbuda': 4,
            'Thailand': 5,
            'Mauritius': 1,
            'Guatemala': 3,
            'Liberia': 1,
            'Kazakhstan': 4,
            'Niger': 3,
            'Mauritania': 4,
            'Montserrat': 4,
            'Namibia': 3,
            'Azerbaijan': 5,
            'Guam': 1,
            'Faroe Islands': 6,
            'India': 30,
            'Nicaragua': 2,
            'Barbados': 3,
            'Lebanon': 1,
            'Palestine': 1,
            'Guyana': 3,
            'Sudan': 3,
            'St Lucia': 1,
            'Ethiopia': 1,
            'Puerto Rico': 1,
            'Grenada': 1,
            'Jordan': 1,
            'Rwanda': 1,
            'Qatar': 1,
            'Afghanistan': 4,
            'Hong Kong': 2,
            'Andorra': 1,
            'Malta': 1,
            'Belize': 1,
            'South Sudan': 1,
            'Indonesia': 1,
            'Botswana': 1},
    "17": {'10': 593,
            '7': 604,
            '1': 566,
            '9': 577,
            '15': 501,
            '8': 612,
            '21': 536,
            '13': 419,
            '22': 531,
            '5': 579,
            '3': 547,
            '14': 542,
            '12': 390,
            '11': 590,
            '2': 519,
            '23': 546,
            '26': 390,
            '6': 586,
            '17': 554,
            '18': 545,
            '4': 573,
            '19': 545,
            '31': 280,
            '25': 409,
            '37': 135,
            '30': 371,
            '44': 74,
            '29': 358,
            '24': 425,
            '20': 568,
            '16': 517,
            '33': 287,
            '28': 357,
            '27': 423,
            '77': 77,
            '47': 28,
            '38': 102,
            '40': 114,
            '92': 10,
            '36': 145,
            '87': 14,
            '34': 207,
            '32': 250,
            '83': 6,
            '70': 29,
            '35': 183,
            '89': 15,
            '56': 17,
            '99': 70,
            '57': 8,
            '91': 21,
            '86': 4,
            '45': 47,
            '63': 4,
            '39': 107,
            '43': 41,
            '42': 54,
            '93': 14,
            '72': 7,
            '71': 10,
            '88': 44,
            '55': 35,
            '80': 16,
            '50': 42,
            '66': 27,
            '60': 10,
            '73': 6,
            '67': 5,
            '74': 2,
            '69': 6,
            '76': 4,
            '41': 53,
            '90': 26,
            '46': 29,
            '75': 6,
            '79': 2,
            '62': 6,
            '81': 5,
            '61': 7,
            '49': 19,
            '95': 12,
            '53': 11,
            '96': 13,
            '97': 16,
            '68': 4,
            '98': 21,
            '94': 11,
            '58': 5,
            '78': 5,
            '': 60,
            '48': 17,
            '52': 10,
            '54': 11,
            '84': 4,
            '82': 5,
            '65': 4,
            '64': 2,
            '51': 7,
            '59': 5,
            '85': 1},
    "18": {'10': 70.38617200674537,
            '7': 68.87251655629139,
            '1': 68.35689045936395,
            '9': 69.28769497400347,
            '15': 66.53493013972056,
            '8': 68.83006535947712,
            '21': 66.2723880597015,
            '13': 66.90214797136038,
            '22': 66.31638418079096,
            '5': 68.49740932642487,
            '3': 67.38939670932358,
            '14': 66.9870848708487,
            '12': 65.43076923076923,
            '11': 68.3406779661017,
            '2': 67.58766859344894,
            '23': 66.46886446886447,
            '26': 64.04358974358975,
            '6': 68.19283276450511,
            '17': 66.9115523465704,
            '18': 66.45688073394496,
            '4': 67.76614310645724,
            '19': 66.63669724770642,
            '31': 63.06785714285714,
            '25': 64.59413202933985,
            '37': 61.785185185185185,
            '30': 63.1644204851752,
            '44': 64.70270270270271,
            '29': 63.92178770949721,
            '24': 64.65411764705883,
            '20': 66.7306338028169,
            '16': 66.08510638297872,
            '33': 63.29965156794425,
            '28': 63.943977591036415,
            '27': 64.36170212765957,
            '77': 66.1038961038961,
            '47': 63.57142857142857,
            '38': 61.77450980392157,
            '40': 61.51754385964912,
            '92': 68.9,
            '36': 60.5448275862069,
            '87': 68.35714285714286,
            '34': 62.072463768115945,
            '32': 62.152,
            '83': 67.66666666666667,
            '70': 64.72413793103448,
            '35': 60.92896174863388,
            '89': 65.4,
            '56': 65.11764705882354,
            '99': 64.35714285714286,
            '57': 68.125,
            '91': 66.76190476190476,
            '86': 64.0,
            '45': 62.0,
            '63': 69.0,
            '39': 62.52336448598131,
            '43': 60.048780487804876,
            '42': 62.5,
            '93': 67.28571428571429,
            '72': 65.0,
            '71': 64.5,
            '88': 66.5,
            '55': 63.0,
            '80': 63.4375,
            '50': 62.30952380952381,
            '66': 63.77777777777778,
            '60': 64.1,
            '73': 64.33333333333333,
            '67': 64.6,
            '74': 67.5,
            '69': 68.66666666666667,
            '76': 68.0,
            '41': 61.37735849056604,
            '90': 65.61538461538461,
            '46': 60.206896551724135,
            '75': 66.5,
            '79': 71.5,
            '62': 62.0,
            '81': 65.0,
            '61': 61.57142857142857,
            '49': 59.68421052631579,
            '95': 65.25,
            '53': 62.45454545454545,
            '96': 64.53846153846153,
            '97': 62.4375,
            '68': 67.0,
            '98': 60.904761904761905,
            '94': 66.72727272727273,
            '58': 62.8,
            '78': 65.6,
            '': 61.63333333333333,
            '48': 61.470588235294116,
            '52': 61.8,
            '54': 61.0,
            '84': 63.75,
            '82': 59.8,
            '65': 58.5,
            '64': 62.5,
            '51': 58.0,
            '59': 57.2,
            '85': 57.0},
    "19": '79',
    "20": 'Real Madrid',
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
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
