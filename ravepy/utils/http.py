from __future__ import absolute_import, unicode_literals

import requests

__default_headers = {
    'Content-Type': 'application/json'
}
def post(url, data, headers=__default_headers):
    r = requests.post(url, json=data, headers=headers)
    return r.json()

def get(url, headers=__default_headers):
    r = request.get(url, headers=headers)
    return r.json()
