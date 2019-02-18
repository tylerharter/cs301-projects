# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math

PASS = "PASS"
TEXT_FORMAT = "text"
Question = collections.namedtuple("Question", ["number", "weight", "format"])

# group_weights = {
#     "test_remove_nan": 3,
#     "test_calculate_avg": 5,
#     "test_remove_duplicates": 5,
#     "test_filter_description": 7,
#     "test_get_costlist_wine": 8,
#     "test_blackberry_aroma": 5,
#     "test_get_anagram": 7,
#     "test_get_anagram2": 3,
#     "test_best_rated_wine_variety": 5,
#     "test_best_rated_wine_variety2": 5,
#     "test_calculate_ppd": 5,
#     "test_calculate_ppd2": 5,
#     "test_highest_ppd_for_country1": 5,
#     "test_highest_ppd_for_country2": 5,
#     "test_highest_ppd_for_country3": 2,
#     "test_get_wines_produced": 5,
#     "test_get_wines_produced2": 5,
#     "test_get_range": 5,
#     "test_get_range2": 5,
#     "test_challenge": 5
# }



questions = [
    Question(number=1, weight=0.6, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1.4, format=TEXT_FORMAT),
    Question(number=5, weight=1.6, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1.4, format=TEXT_FORMAT),
    Question(number=8, weight=0.6, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=0.4, format=TEXT_FORMAT),
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
    "2": "39.407876230661039",
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
    "4": [
         'Wines & Winemakers',
         'Matarromera',
         'Beaucanon',
         'Substance',
         'Val de Los Frailes',
         'Palacio del Burgo',
         'Maurodos',
         'Bodega Carmen Rodríguez'
    ],
    "5": 'Italy',
    "6": [
         'MissionHill',
         'IGreppi',
         'SanVicente',
         'Rivetto',
         'FrancoM.Martinetti',
         'Palmeri',
         'ChâteauGrandBillard',
         'SanPolo',
         'ChâteauSaint-Didier-Parnac',
         'Ponzi',
         'LunaBeberide',
         'BodegaCarmenRodríguez',
         'ValdeLosFrailes',
         'GrafenNeipperg',
         'Lleiroso',
         'ChâteaudeBensse',
         'Margerum',
         'HawkWatchWinery',
         'Guenoc',
         'AltoMoncayo',
         'Foxen',
         'ChâteauFongalan',
         'Levendi',
         'Primus',
         'GlobalWines',
         'Herencia',
         'AdelaidaCellars',
         'TenutadiTrecciano',
         'Numanthia',
         'MarquésdeCáceres',
         'Speri',
         'RobertHall',
         'HerdadedoRocim',
         'Matchbook',
         'RiosdeChile',
         'Polkura',
         'VieWinery',
         'MedlockAmes',
         'HarneyLane',
         'TerredelMarchesato',
         'Sevtap',
         'Rutini',
         'Westwood',
         'FeudidiSanGregorio',
         'Trisaetum',
         'IlBrunone',
         'TroublemakerbyAustinHope',
         'LaurelGlen',
         'PortaldelMontsant',
         'Piccini',
         'Trinchero',
         "Segal's",
         'HardSixCellars',
         'Carmel',
         'LuigiBosca',
         'JackCreek',
         'NorthGate',
         'RockWall',
         'SantaAlba',
         'Raymond',
         'Peju',
         'EdoardoMiroglio',
         'WinerybytheCreek',
         'SequoiaGrove',
         'BreconEstate',
         'Weninger',
         'Pratesi',
         'Maurodos',
         'PagodeCarraovejas',
         'Piattelli',
         'Viñalba',
         'Amantis',
         'OsoLibre',
         'CameronHughes',
         'FessParker',
         'DeLoach',
         'PatriciaGreenCellars',
         'Substance',
         'MCV',
         'Remelluri',
         'Valduero',
         'Aperture',
         'PedraCancela',
         'MulvaneWineCo.',
         'MonteVolpe',
         'Kessler-Haak',
         'LouisM.Martini',
         'Prospect772',
         'ChâteauPeyfaures',
         'MatiasRiccitelli',
         'ViñaBisquertt',
         'Boëté',
         'QuintaNovadeNossaSenhoradoCarmo',
         'Sinor-LaVallee',
         'Ceralti',
         '3HorseRanchVineyards',
         'Sbragia',
         'DussekFamilyCellars',
         'Easton',
         'Renieri',
         'ChâteauHautSelve',
         'Trefethen',
         'Fenestra',
         'TenutadiTrinoro',
         'Tupun',
         'BernardMagrez',
         'CapanneRicci',
         'RobertBiale',
         'SanPedro',
         'Weinreich',
         'HuntCellars',
         'CastellodiBossi',
         'FreemarkAbbey',
         'NapaCellars',
         'ClosLaChance',
         'AndrewMurray',
         'Hazlitt1852Vineyards',
         'Matarromera',
         'Comartin',
         'Tabor',
         'PascualToso',
         'TwoMountain',
         'Paraduxx',
         'Hunnicutt'
    ],
    "7": ['Cabernet Sauvignon'],
    "8": ['Tempranillo Blend'],
    "9": 'Cabernet Sauvignon',
    "10": 'Tinta de Toro',
    "11": "0.7374517374517374",
    "12": "1.2188841201716738",
    "13": 'Grand Pacific',
    "14": 'Domaine du Touja',
    "15": 'Famiglia Cielo',
    "16": ['Cabernet Sauvignon', 'Rosé'],
    "17": ['Pinot Noir', 'Muscat', 'Pinot Gris'],
    "18": "493.0",
    "19": "11",
    "20": ['Byron', 3.7291666666666665],
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

