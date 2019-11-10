#!/usr/bin/python

import ast
import os
import re
import sys
import json
import math
import collections
from collections import namedtuple

import nbconvert
import nbformat

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
    # stage 2
    Question(number=21, weight=1, format=TEXT_FORMAT),
    Question(number=22, weight=1, format=TEXT_FORMAT),
    Question(number=23, weight=1, format=TEXT_FORMAT),
    Question(number=24, weight=1, format=TEXT_FORMAT),
    Question(number=25, weight=1, format=PNG_FORMAT),
    Question(number=26, weight=1, format=PNG_FORMAT),
    Question(number=27, weight=1, format=PNG_FORMAT),
    Question(number=28, weight=1, format=PNG_FORMAT),
    Question(number=29, weight=1, format=TEXT_FORMAT),
    Question(number=30, weight=1, format=PNG_FORMAT),
    Question(number=31, weight=1, format=TEXT_FORMAT),
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
    "20": Review(id=85969, username='Beninkc', asin='B018Y229OU', title='5 star device crippled by amazon', text='This device would be the best possible tablet for the money if it had Google Play. However Amazon chose to block access to it. This took their well made tablet with a beautiful screen and great performance from an amazing value to a waste of money. This is my last amazon branded product.If you use a lot of apps or want specific apps shop for another device.', rating=1, do_recommend=False, num_helpful=20, date='2016-02-14'),
    "21": 3798,
    "22": {'Dave': 5,
            'Missy': 4,
            '1234': 4,
            'Steve': 4,
            'Chris': 4,
            'Angie': 4,
            'Mike': 4,
            'Susan': 4,
            'Manny': 3,
            'Michael': 3,
            'Susie': 3,
            'Bill': 3,
            'Charles': 3,
            'Dani': 3,
            'mike': 3,
            'Rick': 3,
            'Kindle': 3,
            'Mimi': 3,
            'Jojo': 3,
            'Charlie': 3,
            'Anonymous': 3,
            'kcladyz': 3,
            'David': 3,
            'Josh': 3,
            'Pete': 3,
            'John': 3,
            'Richard': 3,
            'Bubba': 3,
            'Grandma': 3,
            'Frank': 3},
    "23": {'Beninkc': 20,
            'Roberto002007': 7,
            'Dick': 5,
            'CarlosEA': 10,
            'EricO': 7,
            'Junior': 7,
            'TerrieT': 5,
            'LadyEsco702': 8,
            'safissad': 8,
            'Quasimodo': 5,
            'iMax': 5,
            'mysixpack': 6,
            'Deejay': 8,
            'stephfasc22': 5,
            'AshT': 5,
            'fenton': 6,
            'Rodge': 6,
            'Ellen': 10,
            'Karch': 5,
            'FrankW': 5,
            'Kime': 5,
            'Mark': 5,
            '1Briansapp': 5,
            'trouble': 5,
            'Stuartc': 8,
            'Earthdog': 27},
    "24": {'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta': 4.490408673894913,
            'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta': 4.6,
            'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers': 4.866666666666666,
            'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta': 4.574468085106383,
            'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers': 3.8333333333333335,
            'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers': 4.590163934426229,
            'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders': 4.7272727272727275,
            'Amazon Tap Smart Assistant Alexa enabled (black) Brand New': 4.6909090909090905,
            'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping': 5.0,
            'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers': 4.666666666666667,
            'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish': 5.0,
            'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case': 4.603448275862069,
            'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black': 4.583333333333333},
    "29": 4.607549120992761,
    "31": {'i': 1317,
             'for': 1800,
             'my': 1146,
             'to': 1442,
             'it': 1286,
             'this': 1016,
             'the': 1740,
             'a': 1134,
             'and': 1818},
    "32": {'great': 1093,
             'tablet': 681,
             'fire': 104,
             'for': 617,
             'the': 231,
             'my': 138,
             'kindle': 142,
             'to': 106,
             'good': 212,
             'price': 149,
             'gift': 105,
             'it': 137,
             'a': 143,
             'love': 158,
             'kids': 132,
             'awesome': 108,
             'product': 179},
    "33": {'not': 8,
             'very': 3,
             'disappointed': 2,
             'poor': 2,
             'does': 2,
             'amazon': 5,
             'a': 5,
             'great': 2,
             '5': 2,
             'work': 2,
             'to': 2,
             'use': 2,
             'and': 2,
             'kindle': 2,
             'tablet': 4,
             'for': 2,
             'good': 2,
             'really': 2,
             'with': 2},
    "34": {'tablet': 51,
             'the': 18,
             'great': 37,
             'good': 42,
             'for': 60,
             'price': 18,
             'ok': 18,
             'a': 17,
             'not': 13},
    "35": [os.path.join('broken_file', 'rating5', 'helpful', 'helpful.json')],
    "36": [os.path.join('broken_file', 'rating4', 'very_helpful', 'very_helpful.json'),
            os.path.join('broken_file', 'rating4', 'others', 'short', 'short.json'),
            os.path.join('broken_file', 'rating4', 'others', 'others', 'others.json'),
            os.path.join('broken_file', 'rating4', 'not_helpful.json')],
    "37": [os.path.join('broken_file', 'rating5', 'others.json'),
            os.path.join('broken_file', 'rating5', 'helpful', 'helpful.json'),
            os.path.join('broken_file', 'rating4', 'very_helpful', 'very_helpful.json'),
            os.path.join('broken_file', 'rating4', 'others', 'short', 'short.json'),
            os.path.join('broken_file', 'rating4', 'others', 'others', 'others.json'),
            os.path.join('broken_file', 'rating4', 'not_helpful.json'),
            os.path.join('broken_file', 'rating3', 'others', 'others.json'),
            os.path.join('broken_file', 'rating3', 'long', 'long.json'),
            os.path.join('broken_file', 'others.json')],
    "38": 1,
    "39": 4992,
    "40": 0.31190229022053717,
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
