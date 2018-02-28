import requests

__default_headers = {
    'content-type': 'application/json'
}
def post(url, data):
    print(url)
    print(data)
    r = requests.post(url, json=data, headers=__default_headers)
    print(r.text)
    return r.json()
