import requests

URL = 'http://localhost:8000/'

res = requests.get(URL)
print(res.status_code)
print(res.json())

url_item = URL + 'items/100'
params = {
    'q': 'somequery'
}
res = requests.get(url_item, params=params)
print(res.status_code)
print(res.json())
