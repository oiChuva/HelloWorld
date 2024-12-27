import json
import requests
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def consultar_equipamento(numero_serie_input):
    url = 'https://opusmedical.api.neovero.com/api/Equipamentos/query'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8',
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
                    },
                    {
                        "property": "modelo.id",
                        "value": [10, 828],
                        "combineOperator": "OR"
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
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            try:
                equipamentos = response.json()

                if isinstance(equipamentos, list):
                    if equipamentos:
                        for equipamento in equipamentos:
                            numero_serie = equipamento.get("numeroSerie", None)
                            nome = remove_accents(equipamento.get("nome", ""))
                            modelo_nome = remove_accents(equipamento.get("modelo", {}).get("nome", ""))
                            fabricante_nome = remove_accents(equipamento.get("modelo", {}).get("fabricante", {}).get("nome", ""))
                            valor_aquisicao = equipamento.get("valorAquisicao", None)

                            print(f"Número de Série: {numero_serie}")
                            print(f"Nome do Equipamento: {nome}")
                            print(f"Modelo: {modelo_nome}")
                            print(f"Fabricante: {fabricante_nome}")
                            print(f"Valor de Aquisição: {valor_aquisicao}")
                            print("-" * 40)
                    else:
                        print("Nenhum equipamento encontrado.")
                else:
                    print("Resposta inesperada da API:", equipamentos)

            except json.JSONDecodeError:
                print("Erro ao decodificar a resposta da API. Resposta:")
                print(response.text)
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Erro ao realizar a requisição: {e}")

# Exemplo de uso
consultar_equipamento(input("Digite o número de série: "))
