import requests
import json

def cadastrar_cliente(codigo_cliente):

    # Requisição para a API do Neovero
    neovero_url = 'https://opusmedical.api.neovero.com/api/Clientes/pesquisa'
    neovero_headers = {
        'accept': '/',
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8',  # Substitua pelo novo token válido
        'Content-Type': 'application/json-patch+json'
    }
    neovero_data = {
        "codigo": codigo_cliente,
        "empresaId": 1,
        "ativo": True
    }

    neovero_response = requests.post(neovero_url, headers=neovero_headers, json=neovero_data)

    # Verifica se a resposta do Neovero foi bem-sucedida
    if neovero_response.status_code == 200:
        neovero_data = neovero_response.json()

        # Verifica se há dados na resposta antes de acessar índices
        if neovero_data:
            print("Resposta do Neovero:", json.dumps(neovero_data, indent=4))

            # Verifica se há pelo menos um item na lista de resultados
            if neovero_data and len(neovero_data) > 0:
                neovero_item = neovero_data[0]  # Acessa o primeiro item da lista

                # Passa as variáveis resposta do Neovero para a API do Omie
                omie_url = 'https://app.omie.com.br/api/v1/geral/clientes/'
                omie_headers = {
                    'Content-Type': 'application/json'
                }

                omie_payload = {
                    "call": "IncluirCliente",
                    "app_key": "1826443506888",
                    "app_secret": "c9e60167e96e156e2655a92fdcd77df7",
                    "param": [
                        {
                            "codigo_cliente_integracao": codigo_cliente,
                            "razao_social": neovero_item.get("razaosocial", "")[:60],
                            "nome_fantasia": neovero_item.get("nomefantasia", ""),
                            "cnpj_cpf": neovero_item.get("cnpj", "")  
                        }
                    ]
                }

                omie_response = requests.post(omie_url, headers=omie_headers, json=omie_payload)

                # Verifica se a resposta do Omie foi bem-sucedida
                if omie_response.status_code == 200:
                    omie_data = omie_response.json()
                    print("Resposta do Omie:", json.dumps(omie_data, indent=4))
                else:
                    print(f"Erro na requisição para o Omie: {omie_response.status_code}\n{omie_response.text}")
            else:
                print("Lista de dados do Neovero está vaziad.")
        else:
            print("Resposta do Neovero não encontrada")
    else:
        print(f"Erro na requisição para o Neovero: {neovero_response.status_code}\n{neovero_response.text}")
