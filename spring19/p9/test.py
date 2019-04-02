#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
import re, ast, math
from collections import namedtuple, OrderedDict
from functools import wraps

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Tweet"
obfuscate2 = ['tweet_id', 'username', 'num_liked']
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = namedtuple("Question", ["number", "weight", "format"])
Tweet = namedtuple(obfuscate1, obfuscate2)

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
    Question(number=25, weight=1, format=TEXT_FORMAT),
    Question(number=26, weight=1, format=TEXT_FORMAT),
    Question(number=27, weight=1, format=TEXT_FORMAT),
    Question(number=28, weight=1, format=TEXT_FORMAT),
    Question(number=29, weight=1, format=TEXT_FORMAT),
    Question(number=30, weight=1, format=TEXT_FORMAT),
    Question(number=31, weight=1, format=TEXT_FORMAT),
    Question(number=32, weight=1, format=TEXT_FORMAT)

]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": sorted(['1.csv', '2.csv', '1.json', '2.json'], reverse=True),
    "2": sorted([os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','1.json'),
                 os.path.join('sample_data','2.csv'),
                 os.path.join('sample_data','2.json')], reverse=True),
    "3": sorted([os.path.join('full_data','1.csv'),
                 os.path.join('full_data','1.json'),
                 os.path.join('full_data','2.csv'),
                 os.path.join('full_data','2.json'),
                 os.path.join('full_data','3.csv'),
                 os.path.join('full_data','3.json'),
                 os.path.join('full_data','4.csv'),
                 os.path.join('full_data','4.json'),
                 os.path.join('full_data','5.csv'),
                 os.path.join('full_data','5.json'),
                 os.path.join('full_data','agency_info'),
                 os.path.join('full_data','meta.info')], reverse=True),
    "4": sorted([os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','1.json'),
                 os.path.join('sample_data','2.csv'),
                 os.path.join('sample_data','2.json')], reverse=True),
    "5": sorted([os.path.join('full_data','1.csv'),
                 os.path.join('full_data','1.json'),
                 os.path.join('full_data','2.csv'),
                 os.path.join('full_data','2.json'),
                 os.path.join('full_data','3.csv'),
                 os.path.join('full_data','3.json'),
                 os.path.join('full_data','4.csv'),
                 os.path.join('full_data','4.json'),
                 os.path.join('full_data','5.csv'),
                 os.path.join('full_data','5.json')], reverse=True),
    "6": [Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882),
          Tweet(tweet_id='1467811592', username='USERID_8', num_liked=2676),
          Tweet(tweet_id='1467811594', username='USERID_9', num_liked=2182),
          Tweet(tweet_id='1467811795', username='USERID_1', num_liked=7791),
          Tweet(tweet_id='1467812025', username='USERID_1', num_liked=8149)],
    "7": [Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340),
          Tweet(tweet_id='1467812964', username='USERID_10', num_liked=3684),
          Tweet(tweet_id='1467813137', username='USERID_5', num_liked=6816),
          Tweet(tweet_id='1467813579', username='USERID_1', num_liked=1348),
          Tweet(tweet_id='1467813782', username='USERID_1', num_liked=4770)],
    "8":[Tweet(tweet_id='1467844540', username='USERID_9', num_liked=6366),
         Tweet(tweet_id='1467844907', username='USERID_3', num_liked=8770),
         Tweet(tweet_id='1467845095', username='USERID_4', num_liked=8567),
         Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761),
         Tweet(tweet_id='1467852031', username='USERID_2', num_liked=4565),
         Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594),
         Tweet(tweet_id='1467852789', username='USERID_10', num_liked=686),
         Tweet(tweet_id='1467853135', username='USERID_1', num_liked=6515),
         Tweet(tweet_id='1467853356', username='USERID_10', num_liked=3192),
         Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936),
         Tweet(tweet_id='1467853479', username='USERID_9', num_liked=4939),
         Tweet(tweet_id='1467854062', username='USERID_10', num_liked=9346),
         Tweet(tweet_id='1467854345', username='USERID_9', num_liked=7959),
         Tweet(tweet_id='1467854706', username='USERID_1', num_liked=8972),
         Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741),
         Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728),
         Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806),
         Tweet(tweet_id='1467855981', username='USERID_2', num_liked=6455),
         Tweet(tweet_id='1467856044', username='USERID_7', num_liked=1442),
         Tweet(tweet_id='1467856352', username='USERID_3', num_liked=523),
         Tweet(tweet_id='1467856426', username='USERID_6', num_liked=8675),
         Tweet(tweet_id='1467856497', username='USERID_7', num_liked=3105),
         Tweet(tweet_id='1467856632', username='USERID_1', num_liked=1724),
         Tweet(tweet_id='1467856821', username='USERID_6', num_liked=5145),
         Tweet(tweet_id='1467856919', username='USERID_4', num_liked=3887),
         Tweet(tweet_id='1467857221', username='USERID_5', num_liked=3589),
         Tweet(tweet_id='1467857297', username='USERID_1', num_liked=736),
         Tweet(tweet_id='1467857378', username='USERID_4', num_liked=9459),
         Tweet(tweet_id='1467857511', username='USERID_7', num_liked=3713),
         Tweet(tweet_id='1467857722', username='USERID_8', num_liked=9072),
         Tweet(tweet_id='1467857975', username='USERID_9', num_liked=4893),
         Tweet(tweet_id='1467858363', username='USERID_10', num_liked=4263),
         Tweet(tweet_id='1467858627', username='USERID_3', num_liked=8400),
         Tweet(tweet_id='1467858869', username='USERID_10', num_liked=1609),
         Tweet(tweet_id='1467859025', username='USERID_4', num_liked=5618),
         Tweet(tweet_id='1467859066', username='USERID_9', num_liked=99),
         Tweet(tweet_id='1467859408', username='USERID_5', num_liked=2878),
         Tweet(tweet_id='1467859436', username='USERID_7', num_liked=8001),
         Tweet(tweet_id='1467859558', username='USERID_1', num_liked=8732),
         Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158),
         Tweet(tweet_id='1467859820', username='USERID_10', num_liked=7921),
         Tweet(tweet_id='1467859922', username='USERID_6', num_liked=3955),
         Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055),
         Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851),
         Tweet(tweet_id='1467861095', username='USERID_10', num_liked=7191),
         Tweet(tweet_id='1467861522', username='USERID_1', num_liked=2742),
         Tweet(tweet_id='1467861571', username='USERID_1', num_liked=7095),
         Tweet(tweet_id='1467862213', username='USERID_2', num_liked=2455),
         Tweet(tweet_id='1467862313', username='USERID_10', num_liked=3256),
         Tweet(tweet_id='1467862355', username='USERID_3', num_liked=4110)],
    "9": [Tweet(tweet_id='1467876711', username='USERID_10', num_liked=1117),
          Tweet(tweet_id='1467877496', username='USERID_1', num_liked=2062),
          Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270),
          Tweet(tweet_id='1467877865', username='USERID_1', num_liked=5899),
          Tweet(tweet_id='1467878057', username='USERID_6', num_liked=703),
          Tweet(tweet_id='1467878557', username='USERID_6', num_liked=5814),
          Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351),
          Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238),
          Tweet(tweet_id='1467878983', username='USERID_8', num_liked=4860),
          Tweet(tweet_id='1467879480', username='USERID_4', num_liked=1345),
          Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694),
          Tweet(tweet_id='1467880085', username='USERID_4', num_liked=2478),
          Tweet(tweet_id='1467880431', username='USERID_3', num_liked=9407),
          Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125),
          Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226),
          Tweet(tweet_id='1467880692', username='USERID_6', num_liked=4989),
          Tweet(tweet_id='1467881131', username='USERID_10', num_liked=732),
          Tweet(tweet_id='1467881373', username='USERID_6', num_liked=8615),
          Tweet(tweet_id='1467881376', username='USERID_4', num_liked=4378),
          Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119),
          Tweet(tweet_id='1467881686', username='USERID_5', num_liked=8136),
          Tweet(tweet_id='1467881809', username='USERID_4', num_liked=1797),
          Tweet(tweet_id='1467881897', username='USERID_5', num_liked=2314),
          Tweet(tweet_id='1467881920', username='USERID_3', num_liked=4101),
          Tweet(tweet_id='1467882140', username='USERID_8', num_liked=5320),
          Tweet(tweet_id='1467882491', username='USERID_10', num_liked=3512),
          Tweet(tweet_id='1467882592', username='USERID_10', num_liked=1887),
          Tweet(tweet_id='1467882902', username='USERID_3', num_liked=4646),
          Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089),
          Tweet(tweet_id='1467888732', username='USERID_7', num_liked=2800),
          Tweet(tweet_id='1467888953', username='USERID_3', num_liked=3951),
          Tweet(tweet_id='1467889231', username='USERID_5', num_liked=1320),
          Tweet(tweet_id='1467889334', username='USERID_5', num_liked=8495),
          Tweet(tweet_id='1467889574', username='USERID_1', num_liked=4696),
          Tweet(tweet_id='1467889791', username='USERID_5', num_liked=4027),
          Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394),
          Tweet(tweet_id='1467890079', username='USERID_8', num_liked=2556),
          Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227),
          Tweet(tweet_id='1467890723', username='USERID_1', num_liked=96),
          Tweet(tweet_id='1467891826', username='USERID_9', num_liked=2021),
          Tweet(tweet_id='1467891880', username='USERID_7', num_liked=6847),
          Tweet(tweet_id='1467892075', username='USERID_6', num_liked=2816),
          Tweet(tweet_id='1467892515', username='USERID_5', num_liked=917),
          Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270),
          Tweet(tweet_id='1467892720', username='USERID_3', num_liked=3227)],
    "10": [Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315),
           Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298),
           Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533),
           Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650),
           Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101)],
    "11": [Tweet(tweet_id='1467812416', username='USERID_9', num_liked=5278),
           Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700),
           Tweet(tweet_id='1467812723', username='USERID_3', num_liked=5414),
           Tweet(tweet_id='1467812771', username='USERID_8', num_liked=2190),
           Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667)],
    "12":[Tweet(tweet_id='1467944581', username='USERID_1', num_liked=7216),
          Tweet(tweet_id='1467944654', username='USERID_7', num_liked=2838),
          Tweet(tweet_id='1467944871', username='USERID_1', num_liked=9393),
          Tweet(tweet_id='1467945476', username='USERID_10', num_liked=9246),
          Tweet(tweet_id='1467945704', username='USERID_1', num_liked=526),
          Tweet(tweet_id='1467945787', username='USERID_9', num_liked=8850),
          Tweet(tweet_id='1467945885', username='USERID_4', num_liked=9403),
          Tweet(tweet_id='1467946026', username='USERID_1', num_liked=2861),
          Tweet(tweet_id='1467946137', username='USERID_1', num_liked=5470),
          Tweet(tweet_id='1467946559', username='USERID_6', num_liked=987),
          Tweet(tweet_id='1467946592', username='USERID_3', num_liked=9085),
          Tweet(tweet_id='1467946749', username='USERID_4', num_liked=3381),
          Tweet(tweet_id='1467946810', username='USERID_4', num_liked=5338),
          Tweet(tweet_id='1467947005', username='USERID_7', num_liked=6974),
          Tweet(tweet_id='1467947104', username='USERID_6', num_liked=5847),
          Tweet(tweet_id='1467947557', username='USERID_9', num_liked=8449),
          Tweet(tweet_id='1467947713', username='USERID_7', num_liked=7444),
          Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578),
          Tweet(tweet_id='1467948169', username='USERID_1', num_liked=4545),
          Tweet(tweet_id='1467948434', username='USERID_9', num_liked=770),
          Tweet(tweet_id='1467948521', username='USERID_4', num_liked=8276),
          Tweet(tweet_id='1467948526', username='USERID_3', num_liked=7010),
          Tweet(tweet_id='1467948979', username='USERID_10', num_liked=9209),
          Tweet(tweet_id='1467949047', username='USERID_3', num_liked=7231),
          Tweet(tweet_id='1467949516', username='USERID_3', num_liked=4787),
          Tweet(tweet_id='1467949681', username='USERID_5', num_liked=5318),
          Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383),
          Tweet(tweet_id='1467949969', username='USERID_3', num_liked=1177),
          Tweet(tweet_id='1467950027', username='USERID_10', num_liked=8575),
          Tweet(tweet_id='1467950029', username='USERID_1', num_liked=7362),
          Tweet(tweet_id='1467950217', username='USERID_7', num_liked=1241),
          Tweet(tweet_id='1467950510', username='USERID_7', num_liked=5002),
          Tweet(tweet_id='1467950588', username='USERID_4', num_liked=589),
          Tweet(tweet_id='1467950600', username='USERID_3', num_liked=5951),
          Tweet(tweet_id='1467950649', username='USERID_7', num_liked=9449),
          Tweet(tweet_id='1467950687', username='USERID_3', num_liked=3464),
          Tweet(tweet_id='1467950866', username='USERID_4', num_liked=122),
          Tweet(tweet_id='1467950975', username='USERID_3', num_liked=6793),
          Tweet(tweet_id='1467951016', username='USERID_5', num_liked=7795),
          Tweet(tweet_id='1467951035', username='USERID_9', num_liked=3477),
          Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515),
          Tweet(tweet_id='1467951422', username='USERID_6', num_liked=2520),
          Tweet(tweet_id='1467951568', username='USERID_8', num_liked=39),
          Tweet(tweet_id='1467951850', username='USERID_8', num_liked=1170),
          Tweet(tweet_id='1467951931', username='USERID_4', num_liked=5320),
          Tweet(tweet_id='1467952069', username='USERID_7', num_liked=399),
          Tweet(tweet_id='1467952100', username='USERID_1', num_liked=2754),
          Tweet(tweet_id='1467952123', username='USERID_9', num_liked=9222),
          Tweet(tweet_id='1467952985', username='USERID_4', num_liked=6256),
          Tweet(tweet_id='1467953090', username='USERID_2', num_liked=1896)],
    "13": [],
    "14": os.path.join('sample_data','2.csv'),
    "15": False,
    "16": os.path.join('full_data','3.csv'),
    "17": [os.path.join('sample_data','2.json'),
           os.path.join('sample_data','2.csv'),
           os.path.join('sample_data','1.csv')],
    "18": [Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315),
           Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298),
           Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533),
           Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650),
           Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101),
           Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882),
           Tweet(tweet_id='1467811592', username='USERID_8', num_liked=2676),
           Tweet(tweet_id='1467811594', username='USERID_9', num_liked=2182),
           Tweet(tweet_id='1467811795', username='USERID_1', num_liked=7791),
           Tweet(tweet_id='1467812025', username='USERID_1', num_liked=8149),
           Tweet(tweet_id='1467812416', username='USERID_9', num_liked=5278),
           Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700),
           Tweet(tweet_id='1467812723', username='USERID_3', num_liked=5414),
           Tweet(tweet_id='1467812771', username='USERID_8', num_liked=2190),
           Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667),
           Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340),
           Tweet(tweet_id='1467812964', username='USERID_10', num_liked=3684),
           Tweet(tweet_id='1467813137', username='USERID_5', num_liked=6816),
           Tweet(tweet_id='1467813579', username='USERID_1', num_liked=1348),
           Tweet(tweet_id='1467813782', username='USERID_1', num_liked=4770)],
    "19": [Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700),
           Tweet(tweet_id='1467812025', username='USERID_1', num_liked=8149),
           Tweet(tweet_id='1467811795', username='USERID_1', num_liked=7791),
           Tweet(tweet_id='1467813137', username='USERID_5', num_liked=6816),
           Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882),
           Tweet(tweet_id='1467812723', username='USERID_3', num_liked=5414),
           Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298),
           Tweet(tweet_id='1467812416', username='USERID_9', num_liked=5278),
           Tweet(tweet_id='1467813782', username='USERID_1', num_liked=4770),
           Tweet(tweet_id='1467812964', username='USERID_10', num_liked=3684),
           Tweet(tweet_id='1467812799', username='USERID_7', num_liked=3340),
           Tweet(tweet_id='1467811592', username='USERID_8', num_liked=2676),
           Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667),
           Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650),
           Tweet(tweet_id='1467812771', username='USERID_8', num_liked=2190),
           Tweet(tweet_id='1467811594', username='USERID_9', num_liked=2182),
           Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101),
           Tweet(tweet_id='1467813579', username='USERID_1', num_liked=1348),
           Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533),
           Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315)],
    "20": [Tweet(tweet_id='1467894593', username='USERID_2', num_liked=869000000),
           Tweet(tweet_id='1467894600', username='USERID_8', num_liked=915000),
           Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936),
           Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891),
           Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851),
           Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830),
           Tweet(tweet_id='1467895048', username='USERID_10', num_liked=9822),
           Tweet(tweet_id='1467966646', username='USERID_7', num_liked=9821),
           Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728),
           Tweet(tweet_id='1467898078', username='USERID_10', num_liked=9705),
           Tweet(tweet_id='1467928300', username='USERID_9', num_liked=9681),
           Tweet(tweet_id='1467917177', username='USERID_3', num_liked=9678),
           Tweet(tweet_id='1467923235', username='USERID_9', num_liked=9662),
           Tweet(tweet_id='1467964211', username='USERID_4', num_liked=9618),
           Tweet(tweet_id='1467873980', username='USERID_5', num_liked=9608),
           Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594),
           Tweet(tweet_id='1467863633', username='USERID_9', num_liked=9549),
           Tweet(tweet_id='1467953733', username='USERID_4', num_liked=9526),
           Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465),
           Tweet(tweet_id='1467954070', username='USERID_8', num_liked=9462)],
    "21": 445,
    "22": 10,
    "23": 1964182.7747747747,
    "24": '1467894593',
    "25": '1467894593',
    "26": 55,
    "27": 52,
    "28": 'USERID_2',
    "29": 'USERID_2',
    "30": [],
    "31": ['USERID_2',
           'USERID_8',
           'USERID_7',
           'USERID_10',
           'USERID_9',
           'USERID_6',
           'USERID_1',
           'USERID_5',
           'USERID_3'],
    "32": ['play/ls/lu.txt',
           'play/ls/mf.py',
           'play/ls/qwe/iuqwe.json',
           'play/ls/qwe/usun.pdf',
           'play/ou/a',
           'play/ou/b',
           'play/ou/quap/aoq/aqnsa',
           'play/ou/quap/aoq/qsonj',
           'play/ou/quap/qonxu.txt',
           'play/ou/quap/uikwe',
           'play/ou/v',
           'play/rb/ppt.ppt',
           'play/rb/rb9/12.xls',
           'play/rb/rb9/89.csv']
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
    jbn = [6,7,8,9,10, 11,12, 18,19,20]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        actual = ast.literal_eval(actual)
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
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
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
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
