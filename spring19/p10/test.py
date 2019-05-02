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
from bs4 import BeautifulSoup
from datetime import datetime

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Tweet"
obfuscate2 = ['tweet_id', 'username', 'num_liked', 'length']
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
HTML_FORMAT = "html"
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
    Question(number=8, weight=1, format=HTML_FORMAT),
    Question(number=9, weight=1, format=HTML_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=HTML_FORMAT),
    Question(number=16, weight=1, format=HTML_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=HTML_FORMAT),
    Question(number=20, weight=1, format=HTML_FORMAT),
    # stage 2
    Question(number=21, weight=1, format=HTML_FORMAT),
    Question(number=22, weight=1, format=PNG_FORMAT),
    Question(number=23, weight=1, format=HTML_FORMAT),
    Question(number=24, weight=1, format=PNG_FORMAT),
    Question(number=25, weight=1, format=HTML_FORMAT),
    Question(number=26, weight=1, format=HTML_FORMAT),
    Question(number=27, weight=1, format=PNG_FORMAT),
    Question(number=28, weight=1, format=HTML_FORMAT),
    Question(number=29, weight=1, format=PNG_FORMAT),
    Question(number=30, weight=1, format=PNG_FORMAT),
    Question(number=31, weight=1, format=HTML_FORMAT),
    Question(number=32, weight=1, format=TEXT_FORMAT),
    Question(number=33, weight=1, format=PNG_FORMAT),
    Question(number=34, weight=1, format=TEXT_FORMAT),
    Question(number=35, weight=1, format=PNG_FORMAT),
    Question(number=36, weight=1, format=TEXT_FORMAT),
    Question(number=37, weight=1, format=PNG_FORMAT),
    Question(number=38, weight=1, format=PNG_FORMAT),
    Question(number=39, weight=1, format=TEXT_FORMAT),
    Question(number=40, weight=1, format=PNG_FORMAT)
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": 127493303,
    "2": "Brazil_Peru.json",
    "3":[{'capital': 'Brasilia',
          'country': 'Brazil',
          'latitude': -15.783333333333333,
          'longitude': -47.916667},
         {'capital': 'Nouakchott',
          'country': 'Mauritania',
          'latitude': 18.066666666666666,
          'longitude': -15.966667000000001},
         {'capital': 'Bern',
          'country': 'Switzerland',
          'latitude': 46.91666666666666,
          'longitude': 7.466667},
         {'capital': 'Zagreb',
          'country': 'Croatia',
          'latitude': 45.8,
          'longitude': 16.0},
         {'capital': 'Cairo',
          'country': 'Egypt',
          'latitude': 30.05,
          'longitude': 31.25},
         {'capital': 'Sanaa',
          'country': 'Yemen',
          'latitude': 15.35,
          'longitude': 44.2},
         {'capital': 'Helsinki',
          'country': 'Finland',
          'latitude': 60.16666666666666,
          'longitude': 24.933332999999998},
         {'capital': 'Addis Ababa',
          'country': 'Ethiopia',
          'latitude': 9.033333333333333,
          'longitude': 38.7},
         {'capital': 'Prague',
          'country': 'Czech Republic',
          'latitude': 50.08333333333334,
          'longitude': 14.466667000000001},
         {'capital': 'Maseru',
          'country': 'Lesotho',
          'latitude': -29.316666666666666,
          'longitude': 27.483333000000002},
         {'capital': 'Antananarivo',
          'country': 'Madagascar',
          'latitude': -18.916666666666668,
          'longitude': 47.516667},
         {'capital': 'Ashgabat',
          'country': 'Turkmenistan',
          'latitude': 37.95,
          'longitude': 58.38333299999999},
         {'capital': 'Tashkent',
          'country': 'Uzbekistan',
          'latitude': 41.31666666666667,
          'longitude': 69.25},
         {'capital': 'Kingstown',
          'country': 'Saint Vincent and the Grenadines',
          'latitude': 13.133333333333333,
          'longitude': -61.216667},
         {'capital': 'Roseau',
          'country': 'Dominica',
          'latitude': 15.3,
          'longitude': -61.4},
         {'capital': 'Tunis',
          'country': 'Tunisia',
          'latitude': 36.8,
          'longitude': 10.183333},
         {'capital': 'Niamey',
          'country': 'Niger',
          'latitude': 13.516666666666667,
          'longitude': 2.1166669999999996},
         {'capital': 'Dublin',
          'country': 'Ireland',
          'latitude': 53.31666666666667,
          'longitude': -6.233333},
         {'capital': 'Port-au-Prince',
          'country': 'Haiti',
          'latitude': 18.53333333333333,
          'longitude': -72.333333},
         {'capital': 'Lima',
          'country': 'Peru',
          'latitude': -12.05,
          'longitude': -77.05},
         {'capital': 'San Salvador',
          'country': 'El Salvador',
          'latitude': 13.7,
          'longitude': -89.2},
         {'capital': 'Sofia',
          'country': 'Bulgaria',
          'latitude': 42.68333333333333,
          'longitude': 23.316667000000002},
         {'capital': 'Guatemala City',
          'country': 'Guatemala',
          'latitude': 14.616666666666667,
          'longitude': -90.516667},
         {'capital': 'Rabat',
          'country': 'Morocco',
          'latitude': 34.016666666666666,
          'longitude': -6.816667},
         {'capital': 'Brussels',
          'country': 'Belgium',
          'latitude': 50.83333333333334,
          'longitude': 4.3333330000000005},
         {'capital': 'Ankara',
          'country': 'Turkey',
          'latitude': 39.93333333333333,
          'longitude': 32.866667},
         {'capital': 'Wellington',
          'country': 'New Zealand',
          'latitude': -41.3,
          'longitude': 174.783333},
         {'capital': 'George Town',
          'country': 'Cayman Islands',
          'latitude': 19.3,
          'longitude': -81.383333},
         {'capital': 'Tripoli',
          'country': 'Libya',
          'latitude': 32.88333333333333,
          'longitude': 13.166667000000002},
         {'capital': "Nuku'alofa",
          'country': 'Tonga',
          'latitude': -21.133333333333333,
          'longitude': -175.2},
         {'capital': 'Yaounde',
          'country': 'Cameroon',
          'latitude': 3.8666666666666663,
          'longitude': 11.516667},
         {'capital': 'Luxembourg',
          'country': 'Luxembourg',
          'latitude': 49.6,
          'longitude': 6.116667},
         {'capital': 'Kigali',
          'country': 'Rwanda',
          'latitude': -1.95,
          'longitude': 30.05},
         {'capital': 'Panama City',
          'country': 'Panama',
          'latitude': 8.966666666666667,
          'longitude': -79.533333},
         {'capital': 'Phnom Penh',
          'country': 'Cambodia',
          'latitude': 11.55,
          'longitude': 104.91666699999999},
         {'capital': 'Kyiv',
          'country': 'Ukraine',
          'latitude': 50.43333333333333,
          'longitude': 30.516666999999998},
         {'capital': 'Asmara',
          'country': 'Eritrea',
          'latitude': 15.333333333333336,
          'longitude': 38.933333000000005},
         {'capital': 'Amman',
          'country': 'Jordan',
          'latitude': 31.95,
          'longitude': 35.933333000000005},
         {'capital': 'Algiers',
          'country': 'Algeria',
          'latitude': 36.75,
          'longitude': 3.05},
         {'capital': 'Jamestown',
          'country': 'Saint Helena',
          'latitude': -15.933333333333335,
          'longitude': -5.716667},
         {'capital': 'Accra',
          'country': 'Ghana',
          'latitude': 5.55,
          'longitude': -0.216667},
         {'capital': 'Georgetown',
          'country': 'Guyana',
          'latitude': 6.8,
          'longitude': -58.15},
         {'capital': 'London',
          'country': 'United Kingdom',
          'latitude': 51.5,
          'longitude': -0.083333},
         {'capital': 'Suva',
          'country': 'Fiji',
          'latitude': -18.133333333333333,
          'longitude': 178.416667},
         {'capital': 'Djibouti',
          'country': 'Djibouti',
          'latitude': 11.583333333333336,
          'longitude': 43.15},
         {'capital': 'Thimphu',
          'country': 'Bhutan',
          'latitude': 27.466666666666665,
          'longitude': 89.633333},
         {'capital': 'Oslo',
          'country': 'Norway',
          'latitude': 59.91666666666666,
          'longitude': 10.75},
         {'capital': 'Bissau',
          'country': 'Guinea-Bissau',
          'latitude': 11.85,
          'longitude': -15.583332999999998},
         {'capital': 'The Valley',
          'country': 'Anguilla',
          'latitude': 18.216666666666665,
          'longitude': -63.05},
         {'capital': 'Damascus',
          'country': 'Syria',
          'latitude': 33.5,
          'longitude': 36.3},
         {'capital': 'Tehran',
          'country': 'Iran',
          'latitude': 35.7,
          'longitude': 51.416667},
         {'capital': 'Vientiane',
          'country': 'Laos',
          'latitude': 17.966666666666665,
          'longitude': 102.6},
         {'capital': 'Malabo',
          'country': 'Equatorial Guinea',
          'latitude': 3.75,
          'longitude': 8.783333},
         {'capital': 'Abu Dhabi',
          'country': 'United Arab Emirates',
          'latitude': 24.466666666666665,
          'longitude': 54.36666700000001},
         {'capital': 'Monrovia',
          'country': 'Liberia',
          'latitude': 6.3,
          'longitude': -10.8},
         {'capital': 'Washington D.C.',
          'country': 'United States',
          'latitude': 38.883333,
          'longitude': -77.0},
         {'capital': 'Santo Domingo',
          'country': 'Dominican Republic',
          'latitude': 18.466666666666665,
          'longitude': -69.9},
         {'capital': 'Praia',
          'country': 'Cape Verde',
          'latitude': 14.916666666666664,
          'longitude': -23.516667},
         {'capital': 'Chisinau',
          'country': 'Moldova',
          'latitude': 47.0,
          'longitude': 28.85},
         {'capital': 'Belmopan',
          'country': 'Belize',
          'latitude': 17.25,
          'longitude': -88.766667},
         {'capital': 'Melekeok',
          'country': 'Palau',
          'latitude': 7.4833333333333325,
          'longitude': 134.633333},
         {'capital': 'Baghdad',
          'country': 'Iraq',
          'latitude': 33.333333333333336,
          'longitude': 44.4},
         {'capital': 'Majuro',
          'country': 'Marshall Islands',
          'latitude': 7.1,
          'longitude': 171.383333},
         {'capital': 'Muscat',
          'country': 'Oman',
          'latitude': 23.61666666666667,
          'longitude': 58.583332999999996},
         {'capital': 'Kabul',
          'country': 'Afghanistan',
          'latitude': 34.516666666666666,
          'longitude': 69.18333299999999},
         {'capital': 'Paramaribo',
          'country': 'Suriname',
          'latitude': 5.833333333333332,
          'longitude': -55.166667000000004},
         {'capital': 'Reykjavik',
          'country': 'Iceland',
          'latitude': 64.15,
          'longitude': -21.95},
         {'capital': 'Madrid',
          'country': 'Spain',
          'latitude': 40.4,
          'longitude': -3.683333},
         {'capital': 'Athens',
          'country': 'Greece',
          'latitude': 37.98333333333333,
          'longitude': 23.733333},
         {'capital': 'Beijing',
          'country': 'China',
          'latitude': 39.91666666666666,
          'longitude': 116.38333300000001},
         {'capital': 'Tokyo',
          'country': 'Japan',
          'latitude': 35.68333333333333,
          'longitude': 139.75},
         {'capital': 'Noumea',
          'country': 'New Caledonia',
          'latitude': -22.266666666666666,
          'longitude': 166.45},
         {'capital': 'San Jose',
          'country': 'Costa Rica',
          'latitude': 9.933333333333334,
          'longitude': -84.083333},
         {'capital': 'Lusaka',
          'country': 'Zambia',
          'latitude': -15.416666666666664,
          'longitude': 28.283333000000002},
         {'capital': 'Abuja',
          'country': 'Nigeria',
          'latitude': 9.083333333333334,
          'longitude': 7.533333},
         {'capital': 'Lisbon',
          'country': 'Portugal',
          'latitude': 38.71666666666667,
          'longitude': -9.133333},
         {'capital': 'Bogota',
          'country': 'Colombia',
          'latitude': 4.6,
          'longitude': -74.083333},
         {'capital': 'Taipei',
          'country': 'Taiwan',
          'latitude': 25.03333333333333,
          'longitude': 121.516667},
         {'capital': 'Bujumbura',
          'country': 'Burundi',
          'latitude': -3.3666666666666667,
          'longitude': 29.35},
         {'capital': 'Montevideo',
          'country': 'Uruguay',
          'latitude': -34.85,
          'longitude': -56.166667000000004},
         {'capital': 'Gaborone',
          'country': 'Botswana',
          'latitude': -24.63333333333333,
          'longitude': 25.9},
         {'capital': 'Riga',
          'country': 'Latvia',
          'latitude': 56.95,
          'longitude': 24.1},
         {'capital': 'Baku',
          'country': 'Azerbaijan',
          'latitude': 40.38333333333333,
          'longitude': 49.866667},
         {'capital': 'Papeete',
          'country': 'French Polynesia',
          'latitude': -17.533333333333335,
          'longitude': -149.566667},
         {'capital': 'Ouagadougou',
          'country': 'Burkina Faso',
          'latitude': 12.366666666666667,
          'longitude': -1.516667},
         {'capital': 'Hanoi',
          'country': 'Vietnam',
          'latitude': 21.03333333333333,
          'longitude': 105.85},
         {'capital': 'Male',
          'country': 'Maldives',
          'latitude': 4.166666666666667,
          'longitude': 73.5},
         {'capital': 'Moroni',
          'country': 'Comoros',
          'latitude': -11.7,
          'longitude': 43.233333},
         {'capital': 'Porto-Novo',
          'country': 'Benin',
          'latitude': 6.4833333333333325,
          'longitude': 2.6166669999999996},
         {'capital': 'Ottawa',
          'country': 'Canada',
          'latitude': 45.41666666666666,
          'longitude': -75.7},
         {'capital': 'Stockholm',
          'country': 'Sweden',
          'latitude': 59.33333333333334,
          'longitude': 18.05},
         {'capital': 'Singapore',
          'country': 'Singapore',
          'latitude': 1.2833333333333332,
          'longitude': 103.85},
         {'capital': 'Windhoek',
          'country': 'Namibia',
          'latitude': -22.566666666666666,
          'longitude': 17.083333},
         {'capital': 'Dhaka',
          'country': 'Bangladesh',
          'latitude': 23.716666666666665,
          'longitude': 90.4},
         {'capital': 'Mogadishu',
          'country': 'Somalia',
          'latitude': 2.066666666666667,
          'longitude': 45.333333},
         {'capital': 'Victoria',
          'country': 'Seychelles',
          'latitude': -4.616666666666667,
          'longitude': 55.45},
         {'capital': 'Rome',
          'country': 'Italy',
          'latitude': 41.9,
          'longitude': 12.483333},
         {'capital': 'Vaduz',
          'country': 'Liechtenstein',
          'latitude': 47.13333333333333,
          'longitude': 9.516667},
         {'capital': 'Maputo',
          'country': 'Mozambique',
          'latitude': -25.95,
          'longitude': 32.583333},
         {'capital': 'Libreville',
          'country': 'Gabon',
          'latitude': 0.38333333333333336,
          'longitude': 9.45},
         {'capital': 'Dakar',
          'country': 'Senegal',
          'latitude': 14.733333333333333,
          'longitude': -17.633333},
         {'capital': 'Port Louis',
          'country': 'Mauritius',
          'latitude': -20.15,
          'longitude': 57.483332999999995},
         {'capital': 'Bridgetown',
          'country': 'Barbados',
          'latitude': 13.1,
          'longitude': -59.61666700000001},
         {'capital': 'Ulaanbaatar',
          'country': 'Mongolia',
          'latitude': 47.91666666666666,
          'longitude': 106.91666699999999},
         {'capital': 'Tbilisi',
          'country': 'Georgia',
          'latitude': 41.68333333333333,
          'longitude': 44.833333},
         {'capital': "Saint George's",
          'country': 'Grenada',
          'latitude': 12.05,
          'longitude': -61.75},
         {'capital': 'Tegucigalpa',
          'country': 'Honduras',
          'latitude': 14.1,
          'longitude': -87.216667},
         {'capital': 'Castries',
          'country': 'Saint Lucia',
          'latitude': 14.0,
          'longitude': -61.0},
         {'capital': 'Hamilton',
          'country': 'Bermuda',
          'latitude': 32.28333333333333,
          'longitude': -64.783333},
         {'capital': 'Kampala',
          'country': 'Uganda',
          'latitude': 0.31666666666666665,
          'longitude': 32.55},
         {'capital': 'Riyadh',
          'country': 'Saudi Arabia',
          'latitude': 24.65,
          'longitude': 46.7},
         {'capital': 'Bishkek',
          'country': 'Kyrgyzstan',
          'latitude': 42.86666666666667,
          'longitude': 74.6},
         {'capital': 'San Juan',
          'country': 'Puerto Rico',
          'latitude': 18.466666666666665,
          'longitude': -66.116667},
         {'capital': 'Vienna',
          'country': 'Austria',
          'latitude': 48.2,
          'longitude': 16.366667},
         {'capital': 'Havana',
          'country': 'Cuba',
          'latitude': 23.11666666666667,
          'longitude': -82.35},
         {'capital': 'Ljubljana',
          'country': 'Slovenia',
          'latitude': 46.05,
          'longitude': 14.516667000000002},
         {'capital': 'Moscow',
          'country': 'Russia',
          'latitude': 55.75,
          'longitude': 37.6},
         {'capital': 'Kuala Lumpur',
          'country': 'Malaysia',
          'latitude': 3.1666666666666665,
          'longitude': 101.7},
         {'capital': 'Amsterdam',
          'country': 'Netherlands',
          'latitude': 52.35,
          'longitude': 4.9166669999999995},
         {'capital': 'Oranjestad',
          'country': 'Aruba',
          'latitude': 12.516666666666667,
          'longitude': -70.033333},
         {'capital': 'Santiago',
          'country': 'Chile',
          'latitude': -33.45,
          'longitude': -70.666667},
         {'capital': 'Warsaw',
          'country': 'Poland',
          'latitude': 52.25,
          'longitude': 21.0},
         {'capital': 'Caracas',
          'country': 'Venezuela',
          'latitude': 10.483333333333333,
          'longitude': -66.866667},
         {'capital': 'Manila',
          'country': 'Philippines',
          'latitude': 14.6,
          'longitude': 120.96666699999999},
         {'capital': 'Manama',
          'country': 'Bahrain',
          'latitude': 26.23333333333333,
          'longitude': 50.566666999999995},
         {'capital': 'Conakry',
          'country': 'Guinea',
          'latitude': 9.5,
          'longitude': -13.7},
         {'capital': 'Harare',
          'country': 'Zimbabwe',
          'latitude': -17.816666666666666,
          'longitude': 31.033333000000002},
         {'capital': 'La Paz',
          'country': 'Bolivia',
          'latitude': -16.5,
          'longitude': -68.15},
         {'capital': 'Kuwait City',
          'country': 'Kuwait',
          'latitude': 29.36666666666667,
          'longitude': 47.966667},
         {'capital': 'Budapest',
          'country': 'Hungary',
          'latitude': 47.5,
          'longitude': 19.083333},
         {'capital': 'Jerusalem',
          'country': 'Israel',
          'latitude': 31.766666666666666,
          'longitude': 35.233333},
         {'capital': 'Paris',
          'country': 'France',
          'latitude': 48.86666666666667,
          'longitude': 2.333333},
         {'capital': 'Tirana',
          'country': 'Albania',
          'latitude': 41.31666666666667,
          'longitude': 19.816667000000002},
         {'capital': 'Yerevan',
          'country': 'Armenia',
          'latitude': 40.16666666666666,
          'longitude': 44.5},
         {'capital': 'Tallinn',
          'country': 'Estonia',
          'latitude': 59.43333333333333,
          'longitude': 24.716667},
         {'capital': 'Dar es Salaam',
          'country': 'Tanzania',
          'latitude': -6.8,
          'longitude': 39.283333},
         {'capital': 'Quito',
          'country': 'Ecuador',
          'latitude': -0.21666666666666667,
          'longitude': -78.5},
         {'capital': 'Copenhagen',
          'country': 'Denmark',
          'latitude': 55.66666666666666,
          'longitude': 12.583333},
         {'capital': 'Bucharest',
          'country': 'Romania',
          'latitude': 44.43333333333333,
          'longitude': 26.1},
         {'capital': 'Lome',
          'country': 'Togo',
          'latitude': 6.116666666666666,
          'longitude': 1.216667},
         {'capital': 'Vilnius',
          'country': 'Lithuania',
          'latitude': 54.68333333333333,
          'longitude': 25.316667000000002},
         {'capital': 'Bangkok',
          'country': 'Thailand',
          'latitude': 13.75,
          'longitude': 100.516667},
         {'capital': 'Kingston',
          'country': 'Jamaica',
          'latitude': 18.0,
          'longitude': -76.8},
         {'capital': 'Mexico City',
          'country': 'Mexico',
          'latitude': 19.433333333333334,
          'longitude': -99.133333},
         {'capital': 'Berlin',
          'country': 'Germany',
          'latitude': 52.51666666666666,
          'longitude': 13.4},
         {'capital': 'New Delhi',
          'country': 'India',
          'latitude': 28.6,
          'longitude': 77.2},
         {'capital': 'Managua',
          'country': 'Nicaragua',
          'latitude': 12.133333333333333,
          'longitude': -86.25},
         {'capital': 'Colombo',
          'country': 'Sri Lanka',
          'latitude': 6.916666666666668,
          'longitude': 79.833333},
         {'capital': 'Hagatna',
          'country': 'Guam',
          'latitude': 13.466666666666667,
          'longitude': 144.73333300000002},
         {'capital': 'Nairobi',
          'country': 'Kenya',
          'latitude': -1.2833333333333332,
          'longitude': 36.816666999999995},
         {'capital': 'Buenos Aires',
          'country': 'Argentina',
          'latitude': -34.583333333333336,
          'longitude': -58.666667000000004},
         {'capital': 'Khartoum',
          'country': 'Sudan',
          'latitude': 15.6,
          'longitude': 32.533333},
         {'capital': 'Canberra',
          'country': 'Australia',
          'latitude': -35.266666666666666,
          'longitude': 149.133333},
         {'capital': 'Doha',
          'country': 'Qatar',
          'latitude': 25.28333333333333,
          'longitude': 51.533333},
         {'capital': 'Mbabane',
          'country': 'Swaziland',
          'latitude': -26.316666666666666,
          'longitude': 31.133333},
         {'capital': 'Port-Vila',
          'country': 'Vanuatu',
          'latitude': -17.733333333333334,
          'longitude': 168.316667},
         {'capital': 'Port Moresby',
          'country': 'Papua New Guinea',
          'latitude': -9.45,
          'longitude': 147.183333},
         {'capital': 'Apia',
          'country': 'Samoa',
          'latitude': -13.816666666666665,
          'longitude': -171.76666699999998},
         {'capital': 'Bamako',
          'country': 'Mali',
          'latitude': 12.65,
          'longitude': -8.0},
         {'capital': 'Kathmandu',
          'country': 'Nepal',
          'latitude': 27.716666666666665,
          'longitude': 85.31666700000001},
         {'capital': "N'Djamena",
          'country': 'Chad',
          'latitude': 12.1,
          'longitude': 15.033332999999999},
         {'capital': 'San Marino',
          'country': 'San Marino',
          'latitude': 43.93333333333333,
          'longitude': 12.416667},
         {'capital': 'Astana',
          'country': 'Kazakhstan',
          'latitude': 51.16666666666666,
          'longitude': 71.416667},
         {'capital': 'Minsk',
          'country': 'Belarus',
          'latitude': 53.9,
          'longitude': 27.566667},
         {'capital': 'Monaco',
          'country': 'Monaco',
          'latitude': 43.73333333333333,
          'longitude': 7.4166669999999995},
         {'capital': 'Pretoria',
          'country': 'South Africa',
          'latitude': -25.7,
          'longitude': 28.216666999999998},
         {'capital': 'Valletta',
          'country': 'Malta',
          'latitude': 35.88333333333333,
          'longitude': 14.5},
         {'capital': 'Lilongwe',
          'country': 'Malawi',
          'latitude': -13.966666666666667,
          'longitude': 33.783333},
         {'capital': 'Freetown',
          'country': 'Sierra Leone',
          'latitude': 8.483333333333333,
          'longitude': -13.233332999999998},
         {'capital': 'Yamoussoukro',
          'country': "Cote d'Ivoire",
          'latitude': 6.816666666666666,
          'longitude': -5.266667},
         {'capital': 'Islamabad',
          'country': 'Pakistan',
          'latitude': 33.68333333333333,
          'longitude': 73.05},
         {'capital': 'Beirut',
          'country': 'Lebanon',
          'latitude': 33.86666666666667,
          'longitude': 35.5},
         {'capital': 'Asuncion',
          'country': 'Paraguay',
          'latitude': -25.266666666666666,
          'longitude': -57.666667000000004},
         {'capital': 'Jakarta',
          'country': 'Indonesia',
          'latitude': -6.166666666666668,
          'longitude': 106.816667},
         {'capital': 'Dushanbe',
          'country': 'Tajikistan',
          'latitude': 38.55,
          'longitude': 68.766667}],
    "4": "Hamilton",
    "5": 'Mozambique',
    "6": ['New Zealand', 'Australia', 'Uruguay', 'Argentina', 'Chile'],
    "7": ['Iceland', 'Finland', 'Norway'],
    "10": 'Belarus',
    "11": 'Chad',
    "12": 'Bolivia',
    "13": 1.433899492072933,
    "14": 8840.574141306946,
    "17": 'Bolivia',
    "18": 'Uruguay',
    "32": 0.40037782919521714,
    "34": 0.8687265678031416,
    "36": -0.20995846867456752,
    "39": (1.8422394400496355e-06, 0.03903504364953538)
        }

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

import ast
from collections import defaultdict, namedtuple

import ast 
from collections import defaultdict, namedtuple

class Linter(ast.NodeVisitor):
    def __init__(self, suppressed=None):
        self.warn = namedtuple('WARN', 'name msg')
        self.forbidden_names = {"set", "list", "dict"}
        self.warnings = defaultdict(list)
        self.suppressed = suppressed if suppressed else [] 
        self.func_names = []

    def is_severe(self):
        for severe_name in ("repeated_function", "keyword_names", "unnnecessary_true"):
            for warning in self.warnings:
                if warning.name == severe_name:
                    return True
        return False

    def show_warnings(self):
        for warning, linenos in self.warnings.items(): 
            if warning.name in self.suppressed:
                continue
            if len(linenos) == 1: 
                print("LINE %s : %s" % (linenos[0], warning.msg))
            else:
                print("LINES %s : %s" % (", ".join(map(str, linenos)), warning.msg))

    def register_warning(self, warning_name, warning_msg, lineno):
        w = self.warn(warning_name, warning_msg)
        self.warnings[w].append(lineno)

    def visit_FunctionDef(self, node): 
        # repeated names
        if node.name in self.func_names: 
            self.register_warning("repeated_function", 
                    "The function %s has more than one definition. Avoid reusing function names" % node.name, 
                    node.lineno)
        else:
            self.func_names.append(node.name) 

        # def BADNAME() 
        if node.name.lower() != node.name: 
            self.register_warning("snake_case", 
                    "The convention in Python is to use lowercase names for function names, with words separated by '_', you used '%s'." % node.name, 
                    node.lineno)

    def visit_Assign(self, node): 
        for target in node.targets:
            if type(target) == ast.Name:
                # a = 10
                if len(target.id) == 1: 
                    self.register_warning("descriptive", 
                            "Consider using more descriptive variable names. You used : '%s'." % target.id, 
                            target.lineno)
                
                # list = [..]
                if target.id.lower() in self.forbidden_names:
                    self.register_warning("keyword_names", 
                            "Do not use '%s' for a variable name; that clobbers the Python type." % target.id, 
                            target.lineno)

                # x = x
                if type(node.value) == ast.Name and node.value.id == target.id: 
                    self.register_warning("self_assign", 
                            "Self assignment : the statement %s = %s is superflous" % (node.value.id, target.id), 
                            target.lineno)

    def visit_Compare(self, node): 
        # a == True
        if len(node.comparators) == 1: 
            if type(node.comparators[0]) == ast.NameConstant and node.comparators[0].value: 
                self.register_warning("unnnecessary_true", 
                        "Instead of doing something like 'if %s == True:', you can simply do, 'if a:'" % node.left.id, 
                        node.lineno)

    def visit_For(self, node): 
        if type(node.body[-1]) == ast.Continue: 
            self.register_warning("bad_continue", 
                    "A continue as the last statement in a loop is unnecessary, as the loop proceeds to the next iteration anyway", 
                    node.body[-1].lineno)

    def visit_Return(self, node): 
        pass 


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
    jbn = [6,7,8,9,10,11,12,18,19,20,30]
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
        if not math.isclose(actual, expected, rel_tol=1e-02, abs_tol=1e-02):
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
            if len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            for i,(a,e) in enumerate(zip(actual, expected)):
                if a != e:
                    return "found %s at position %d but expected %s" % (str(a), i, str(e))            # this happens when the list contains dicts.  Just do a simple comparison
    elif type(expected) == tuple:
        if len(expected) != len(actual):
            expected_mismatch = True
        try:
            for idx in range(len(expected)):
                if not math.isclose(actual[idx], expected[idx], rel_tol=1e-02, abs_tol=1e-02):
                    expected_mismatch = True
        except:
            expected_mismatch = True

    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

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
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number,cell)
    raise Exception("invalid question type")


def lint_cell(cell): 
    code = "\n".join(cell.get('source', []))
    tree = ast.parse(code)
    l = Linter()
    l.visit(tree)
    return l


def grade_answers(cells):
    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            # does it match the expected output?
            status = check_cell(question, cells[question.number])

            # does it pass the linter?
            try:
                l = lint_cell(cell)
                lint_warnings = [k.msg for k in l.warnings.keys()]
                if status == PASS and l.is_severe():
                    status = 'failed due to bad coding style (checkout output at end)'
            except Exception as e:
                lint_warnings = ["Lint Exception: " + str(e)]
            for line in lint_warnings:
                results["lint"].append("q%d: %s" % (question.number, line))

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

    # make sure directories are properly setup

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
        print("  Question %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))

    if len(results["lint"]) > 0:
        print()
        print("!"*80)
        print("AUTO-GENERATED CODING SUGGESTIONS FOR YOUR CONSIDERATION:")
        for line in results["lint"]:
            print(line)
        print("!"*80)


if __name__ == '__main__':
    main()
