import requests

__default_headers = {
    'content-type': 'application/json'
}
def post(url, data):
    r = requests.post(url, json=data, headers=__default_headers)
    return r.json()
