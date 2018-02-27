import requests

__default_headers = {
    'content-type': 'application/json'
}
def post(url, data):
    return requests.post(url, data=data, headers=__default_headers).json()
