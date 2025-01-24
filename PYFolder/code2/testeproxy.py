import requests
import json

url = 'https://192.168.88.72:5000/NotaFiscal'
data = {
    'numNF': '3637'
    }

response = requests.post(url, json=data, verify=False)

print(f'Status Code: {response.status_code}')
try:
    response_json = response.json()
    print(json.dumps(response_json, indent=4))
except json.JSONDecodeError:
    print('A resposta não está em formato JSON.')