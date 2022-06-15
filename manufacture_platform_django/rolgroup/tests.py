from django.test import TestCase

import requests


if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/api/lengths_search/'
    headers = {'Authorization': 'Token bdf5958921246977da43b3ae07c7abf53f267ea1'}
    r = requests.post(url, data={"length": 1800}, headers=headers)
    print(r.text)
