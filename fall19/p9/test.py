#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from functools import wraps

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Review"
obfuscate2 = ["id", "username", "asin", "title", "text", "rating", "do_recommend", "num_helpful", "date"]
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = namedtuple("Question", ["number", "weight", "format"])
Review = namedtuple(obfuscate1, obfuscate2)

questions = [
    # stage 1
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

expected_json = {
    "1": sorted(os.listdir("data"), reverse = True),
    "2": sorted([os.path.join('data','sample_reviews.csv'),
                os.path.join('data','sample_reviews.json'),
                os.path.join('data','review5.csv'),
                os.path.join('data','review5.json'),
                os.path.join('data','review4.csv'),
                os.path.join('data','review4.json'),
                os.path.join('data','review3.csv'),
                os.path.join('data','review3.json'),
                os.path.join('data','review2.csv'),
                os.path.join('data','review2.json'),
                os.path.join('data','review1.csv'),
                os.path.join('data','review1.json'),
                os.path.join('data','products.json')], reverse=True),
    "3": sorted([os.path.join('data','review1.csv'),
                 os.path.join('data','review2.csv'),
                 os.path.join('data','review3.csv'),
                 os.path.join('data','review4.csv'),
                 os.path.join('data','review5.csv'),
                 os.path.join('data','sample_reviews.csv')], reverse=True),
    "4": sorted([os.path.join('data','review1.csv'),
                 os.path.join('data','review1.json'),
                 os.path.join('data','review2.csv'),
                 os.path.join('data','review2.json'),
                 os.path.join('data','review3.csv'),
                 os.path.join('data','review3.json'),
                 os.path.join('data','review4.csv'),
                 os.path.join('data','review4.json'),
                 os.path.join('data','review5.csv'),
                 os.path.join('data','review5.json')], reverse=True),
    "5": {'B00QFQRELG': 'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders',
            'B00ZV9PXP2': 'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers',
            'B01BH83OOM': 'Amazon Tap Smart Assistant Alexa enabled (black) Brand New',
            'B0751RGYJV': 'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping',
            'B00IOY8XWQ': 'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers',
            'B0752151W6': 'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish',
            'B018Y226XO': 'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case',
            'B01ACEKAJY': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black',
            'B01AHB9CYG': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta',
            'B01AHB9CN2': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta',
            'B00VINDBJK': 'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers',
            'B01AHB9C1E': 'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers',
            'B018Y229OU': 'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta'},
    "6": 'It does what it is suppose to. No problems with it...',
    "7": 'I hate amazon app store. Nothing good in there. The tablet is too slow for what I do... it is good for reading only....',
    "8": 'Perfection',
    "9": 'review3.csv',
    "10": {'10101': ['Mikey123456789', 'B00QFQRELG'],
            '99904': ['diamond', 'B00QFQRELG'],
            '89604': ['Pat91', 'B00QFQRELG'],
            '58704': ['Frank', 'B00QFQRELG'],
            '38104': ['LADYD92', 'B00QFQRELG']},
    "11": [Review(id=10101, username='Mikey123456789', asin='B00QFQRELG', title='A charger', text='It seems to work just like any other usb plug in charger.', rating=5, do_recommend=True, num_helpful=0, date='2017-01-02'),
            Review(id=99904, username='diamond', asin='B00QFQRELG', title='amazon power fast usb charger', text='got this for my kindle 7 tablet . Does an excellent job charging the kindle fire 7 a lot faster than the one it came with the kindle fire', rating=5, do_recommend=True, num_helpful=2, date='2016-06-03'),
            Review(id=89604, username='Pat91', asin='B00QFQRELG', title='Amazon powerfast wall charger', text='Best kindle charger ever. Took 30 minutes to being my kindle back to life.', rating=5, do_recommend=True, num_helpful=0, date='2016-11-21'),
            Review(id=58704, username='Frank', asin='B00QFQRELG', title='correct plug for kindle', text='Quickly charges kindle so son can use it. Worked great right out of the package', rating=5, do_recommend=True, num_helpful=0, date='2016-10-14'),
            Review(id=38104, username='LADYD92', asin='B00QFQRELG', title='Fast Charger', text='Bought this charger for the Kindle voyage and its great.', rating=5, do_recommend=True, num_helpful=0, date='2016-09-30')],
    "12": [Review(id=10101, username='Mikey123456789', asin='B00QFQRELG', title='A charger', text='It seems to work just like any other usb plug in charger.', rating=5, do_recommend=True, num_helpful=0, date='2017-01-02'),
            Review(id=99904, username='diamond', asin='B00QFQRELG', title='amazon power fast usb charger', text='got this for my kindle 7 tablet . Does an excellent job charging the kindle fire 7 a lot faster than the one it came with the kindle fire', rating=5, do_recommend=True, num_helpful=2, date='2016-06-03'),
            Review(id=89604, username='Pat91', asin='B00QFQRELG', title='Amazon powerfast wall charger', text='Best kindle charger ever. Took 30 minutes to being my kindle back to life.', rating=5, do_recommend=True, num_helpful=0, date='2016-11-21'),
            Review(id=58704, username='Frank', asin='B00QFQRELG', title='correct plug for kindle', text='Quickly charges kindle so son can use it. Worked great right out of the package', rating=5, do_recommend=True, num_helpful=0, date='2016-10-14'),
            Review(id=38104, username='LADYD92', asin='B00QFQRELG', title='Fast Charger', text='Bought this charger for the Kindle voyage and its great.', rating=5, do_recommend=True, num_helpful=0, date='2016-09-30'),
            Review(id=76407, username='RobT', asin='B00QFQRELG', title='Good charger', text='This wall charger works exactly as described for the Kindle Paperwhite.', rating=5, do_recommend=True, num_helpful=0, date='2016-07-22'),
            Review(id=83810, username='Iodine', asin='B00QFQRELG', title='Great item', text='Have been using this item and it seems to be working quite well.', rating=5, do_recommend=True, num_helpful=0, date='2017-03-15'),
            Review(id=32310, username='Akki', asin='B00QFQRELG', title='Nice one', text='Good one and working without any issues. Slim and portable', rating=5, do_recommend=True, num_helpful=0, date='2016-06-24'),
            Review(id=22010, username='STRIPYGOOSE', asin='B00QFQRELG', title='not any faster', text='it does not charge any faster than regular charger.', rating=3, do_recommend=False, num_helpful=0, date='2016-08-18'),
            Review(id=1410, username='Jk60', asin='B00QFQRELG', title='Satisfied', text='It does what it is suppose to. No problems with it...', rating=4, do_recommend=True, num_helpful=0, date='2016-12-07')],
    "13": [Review(id=25136, username='Angrydagg', asin='B018Y229OU', title='Nice features for the price.', text='For the price this tables does everything I need. so far.', rating=4, do_recommend=True, num_helpful=0, date='2015-12-30'),
            Review(id=84039, username='Appman2015', asin='B018Y229OU', title='Great for xmas', text='So far I have bought three of these of tablets and they love it', rating=4, do_recommend=True, num_helpful=1, date='2015-12-30'),
            Review(id=22239, username='SuzieQ', asin='B018Y229OU', title='great for pre teens', text='i am glad i got them for my grand children they r enjoying them', rating=5, do_recommend=True, num_helpful=0, date='2015-12-31'),
            Review(id=70842, username='Gracie', asin='B018Y229OU', title='Great kindle', text='Purchase was good. Very easy to set up and use. Clear screen. Easy to charge. Would like more storage.', rating=5, do_recommend=True, num_helpful=0, date='2015-12-31'),
            Review(id=60542, username='Jeremyjeepster', asin='B018Y229OU', title='Good entry level tablet reader.', text='His is a very economical entry level tablet. Great for kids or for first time users.', rating=4, do_recommend=True, num_helpful=0, date='2015-12-31'),
            Review(id=9042, username='kinglowe78', asin='B018Y229OU', title='Good Deal', text='Real good deal. Nice present for those who want a tablet', rating=4, do_recommend=True, num_helpful=1, date='2016-01-01'),
            Review(id=98845, username='jamal', asin='B018Y229OU', title='good basic', text='Good gift for basic Internet use browsing emails .', rating=3, do_recommend=True, num_helpful=1, date='2016-01-01'),
            Review(id=37045, username='CaOk', asin='B018Y229OU', title='decent budget tablet that does what it suppose to', text='Nothing fancy. A good budget tablet that does what It suppose to do', rating=4, do_recommend=True, num_helpful=0, date='2016-01-01'),
            Review(id=26745, username='Tablet2', asin='B018Y229OU', title='Affordable tablet', text='Bought tablet for my five year old nephew. Is affordable and has good specs. Easy to use. Camera and video are good. My nephew has no problem using it', rating=4, do_recommend=True, num_helpful=0, date='2016-01-01'),
            Review(id=3248, username='Tims54913', asin='B018Y229OU', title='Great tablet', text='If your connected to amazon the tablet is great to use.', rating=5, do_recommend=True, num_helpful=0, date='2016-01-02')],
    "14": Review(id=84713, username='mmolly1', asin='B01AHB9CN2', title='Great product', text='This product is very user friendly and it is very lightweight', rating=5, do_recommend=True, num_helpful=0, date='2017-01-08'),
    "15": Review(id=42931, username='tbistone', asin='B01BH83OOM', title='Amazing', text='I literally use this thing every single day. Love it.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-20'),
    "16": [Review(id=74, username='Wayne', asin='B01AHB9CN2', title='Kindle upgrade', text='Gave this to my wife for Christmas. Upgraded from the original Kindle. She thoroughly enjoys it.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-31'),
            Review(id=82, username='KKLORRAINE', asin='B01AHB9CN2', title='Good', text='Great for reading and Netflix. Fits nice in purse. Good price.', rating=4, do_recommend=True, num_helpful=0, date='2017-04-07'),
            Review(id=110, username='nell', asin='B00IOY8XWQ', title='I love it', text='Prefect for all reading conditions and environments. I take it everywhere.', rating=5, do_recommend=True, num_helpful=0, date='2016-07-09'),
            Review(id=122, username='apple21man', asin='B01BH83OOM', title='A great assistant', text='It works well it takes time for it to know your vocabulary', rating=5, do_recommend=True, num_helpful=0, date='2017-01-23'),
            Review(id=247, username='rockydon1', asin='B018Y229OU', title='great', text='The Kindle fire is a great product. Will do so many things. Would recommend to anyone.', rating=5, do_recommend=True, num_helpful=0, date='2015-12-29'),
            Review(id=251, username='Cheechu821', asin='B018Y229OU', title='Great product for its price', text='I purchased the tablet as a screen for my drink and it worked just fine', rating=3, do_recommend=True, num_helpful=0, date='2016-02-19'),
            Review(id=263, username='aram58', asin='B018Y229OU', title='love the tablet', text='I would recommend this tablet to anyone that is interested in one. It is just as good as a Samsung one and half the price.', rating=5, do_recommend=True, num_helpful=0, date='2016-07-08'),
            Review(id=271, username='NMGPRO', asin='B018Y229OU', title='Good little tablet', text='I purchased this to have a smaller footprint tablet. Could use more popular apps but still great for keeping the library at the tip of the fingers and a camera to boot.', rating=5, do_recommend=True, num_helpful=0, date='2016-01-21'),
            Review(id=275, username='MikeGA', asin='B018Y229OU', title='Great for Amazon', text='This product is a great entry level tablet. It is limited in both memory and function.', rating=5, do_recommend=True, num_helpful=0, date='2016-01-05'),
            Review(id=327, username='ritter6281', asin='B018Y229OU', title='Awesome tablet.', text='This tablet is better than any other tablet of the same cost range. My son saved up to buy his own tablet and had similar priced tablets break or have software issues. This tablet has a nice quality screen and it is nice to be able to not be forced to do everything through Amazon despite it being an Amazon tablet. The option of a Best Buy replacement plan is handy when getting the tablet for kids.', rating=5, do_recommend=True, num_helpful=0, date='2016-04-09')],
    "17": 165,
    "18": 12,
    "19": 'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta',
    "20": Review(id=85969, username='Beninkc', asin='B018Y229OU', title='5 star device crippled by amazon', text='This device would be the best possible tablet for the money if it had Google Play. However Amazon chose to block access to it. This took their well made tablet with a beautiful screen and great performance from an amazing value to a waste of money. This is my last amazon branded product.If you use a lot of apps or want specific apps shop for another device.', rating=1, do_recommend=False, num_helpful=20, date='2016-02-14')
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
    jbn = [6,7,8,9,10,11,12,13,14,15,16,20]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries in list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            elif sorted(actual) == sorted(expected) and actual != expected:
                return "list not sorted"
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
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
    for output in cell.get('outputs', []):
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

    assert(os.path.exists("data"))

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
