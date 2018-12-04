import sys
import importlib
sys.path = sys.path[1:]
def get(*args, **kwargs):
    url = args[0]
    url = url.replace("https://tyler.caraza-harter.com", "http://172.17.0.1")
    import requests
    importlib.reload(requests)
    return requests.get(*args)
