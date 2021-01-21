import requests
from _settings import *


def getPage(url, prms=None):
    page = requests.get(url, params=prms, headers=HEADERS)

    if page.status_code == 200:
        return page
    else:
        return None