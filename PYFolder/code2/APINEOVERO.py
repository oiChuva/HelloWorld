import requests
import time
from arq_remove_accents import remove_accents

def consultar_equipamento(numero_serie_input):
    max_attempts = 5  # Número máximo de tentativas
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
                        },
                        {
                            "property": "modelo.id",
                            "value": [10, 828],
                            "combineOperator": "OR"
                        }
                    ]
                },
                {
                    "combineOperator": "OR",
                    "filters": [
                        {
                            "property": "modelo.nome",
                            "value": "",
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

                    data = filtered_items[0]
                    numero_serie = data.get("numeroSerie", None)
                    patrimonio = data.get("patrimonio", None)
                    modelo_nome = data.get("modelo", {}).get("nome", None)
                    fabricante_nome = data.get("modelo", {}).get("fabricante", {}).get("nome", None)
                    familia_nome = data.get("modelo", {}).get("familia", {}).get("nome", None)
                    valor_aquisicao = data.get("valorAquisicao", None)
                    cliente_id = data.get("clienteId", None)
                    empresa_id = data.get("empresa", {}).get("id", None)

                    if modelo_nome:
                        modelo_nome = remove_accents(modelo_nome)
                    if fabricante_nome:
                        fabricante_nome = remove_accents(fabricante_nome)
                    if familia_nome:
                        familia_nome = remove_accents(familia_nome)

                    resposta_desejada = {
                        "numeroSerie": numero_serie,
                        "patrimonio": patrimonio,
                        "modelo": {
                            "nome": modelo_nome,
                            "fabricante": {
                                "nome": fabricante_nome
                            },
                            "familia": {
                                "nome": familia_nome
                            }
                        },
                        "valorAquisicao": valor_aquisicao,
                        "clienteId": cliente_id,
                        "empresaId": empresa_id
                    }

                    print(resposta_desejada)
                    nome = (familia_nome + " | " + modelo_nome + " ("+ fabricante_nome +")")
                    print(nome)
        except requests.exceptions.RequestException as e:
                    print(f"Erro de requisição: {e}")
                    return {"error": f"Erro de requisição: {e}"}
                
        except ValueError as e:
            print(f"Resposta não é um JSON válido: {e}")
            return {"error": f"Resposta não é um JSON válido: {e}"}
        
        except Exception as e:
            print(f"Erro não esperado: {e}")
            return {"error": f"Erro não esperado: {e}"}
        
    else:
        # Incrementa a tentativa
        attempt += 1
        print(f"Tentativa {attempt} de consulta.")
        time.sleep(5)  # Espera 5 segundos antes de tentar novamente

    # Se todas as tentativas falharem
    print("Erro ao acessar a API após várias tentativas.")
    return {"error": "Erro ao acessar a API após várias tentativas"}

# Número de série de exemplo
numero_serie_teste = "TE90141"

# Chamando a função com o número de série
resultado = consultar_equipamento(numero_serie_teste)

# Exibindo o resultado
print("Resultado da consulta:", resultado)