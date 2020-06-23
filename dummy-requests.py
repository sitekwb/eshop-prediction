import json

import requests

url = "http://127.0.0.1:8000/predict/"
headers = {
    'Content-Type': 'application/json'
}

N = 500

payload = {'user_id': 1, 'price': '1'}
for i in range(N):
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    discount = json.loads(response.text.encode('utf8'))['discount']
