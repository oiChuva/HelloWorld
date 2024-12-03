import requests
import unicodedata
import time
import json

# Função para remover acentos
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Função para consultar o equipamento
def consultar_equipamento(numero_serie_input):
    max_attempts = 3  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        url = 'https://opusmedical.api.neovero.com/api/Equipamentos/query'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8',  # Substitua pelo seu token
            'Content-Type': 'application/json-patch+json'
        }
        data = {
            "limit": 100,
            "offset": 0,
            "filterGroups": [
                {
                    "combineOperator": "AND",
                    "filters": [
                        {
                            "property": "numeroSerie",
                            "value": numero_serie_input,
                            "combineOperator": "AND"
                        }
                    ]
                }
            ],
            "orderBy": [
                {
                    "column": "modelo.nome",
                    "ascending": True
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)  # Timeout em 10 segundos
            print(f"Attempt {attempt + 1}: Status Code: {response.status_code}")

            if response.status_code == 200:
                response_json = response.json()

                if isinstance(response_json, dict) and isinstance(response_json.get('records'), list):
                    records = response_json['records']
                    filtered_items = [item for item in records if item.get("numeroSerie") == numero_serie_input]

                    if not filtered_items:
                        print(f"Equipamento com número de série {numero_serie_input} não encontrado.")
                        return {"error": "Equipamento não encontrado"}

                    # Retorna o JSON cru do item encontrado
                    return filtered_items[0]
                else:
                    print("Erro ao acessar a API. Código de status: {}".format(response.status_code))
                    return {"error": "Erro ao acessar a API"}
        except ValueError:
            print("Resposta não é um JSON válido")
            return {"error": "Resposta não é um JSON válido"}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        # Incrementa a tentativa
        attempt += 1
        print(f"Tentativa {attempt} de consulta.")
        time.sleep(5)  # Espera 5 segundos antes de tentar novamente

    # Se todas as tentativas falharem
    print("Erro ao acessar a API após várias tentativas.")
    return {"error": "Erro ao acessar a API após várias tentativas"}

# Exemplo de uso da função
numero_serie_input = input('Digite o número de série: ')
resultado = consultar_equipamento(numero_serie_input)
print(json.dumps(resultado, indent=4, ensure_ascii=False))
