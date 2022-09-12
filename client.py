import json
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

url_item = URL + 'items/100'
data = {
    'name': 'The item name',
    'price': 0,
    'is_offer': True
}
res = requests.put(url_item, json.dumps(data))
print(res.status_code)
print(res.json())
