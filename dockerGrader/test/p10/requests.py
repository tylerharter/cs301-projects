import sys, os, importlib
sys.path.remove(os.getcwd())
import requests
importlib.reload(requests)
from requests import *

requests_get = get

def get(*args, **kwargs):
    url = args[0]
    url = url.replace("https://tyler.caraza-harter.com", "http://172.17.0.1")
    return requests_get(*args)
