import requests
import json

def cadastrar_cliente(codigo_cliente):
    # Requisição para a API do Neovero
    neovero_url = 'https://opusmedical.api.neovero.com/api/Clientes/pesquisa'
    neovero_headers = {
        'accept': '*/*',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xhbG9jYWxob3N0IiwiYXVkIjoiZTZiMGY5M2I2MDI1NDQwODlkMzQzNmZhYmM1YjRhYjAifQ.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8',
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
        print("Resposta do Neovero:", json.dumps(neovero_data, indent=4))

        # Passa as variáveis resposta do Neovero para a API do Omie
        omie_url = 'https://app.omie.com.br/api/v1/geral/clientes/'
        omie_headers = {
            'Content-Type': 'application/json'
        }

        omie_payload = {
            "call": "IncluirCliente",
            "app_key": "1826443506888",
            "app_secret": "4a98af31f25d8b152a18911c65d23190",
            "param": [
                {
                    "codigo_cliente_integracao": codigo_cliente,
                    "razao_social": neovero_data[0]["razaosocial"][:60],
                    "nome_fantasia": neovero_data[0]["nomefantasia"],
                    "cnpj_cpf": neovero_data[0]["cnpj"]  
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
        print(f"Erro na requisição para o Neovero: {neovero_response.status_code}\n{neovero_response.text}")

# Exemplo de uso da função
codigo_cliente = input("Digite o código do cliente: ")
cadastrar_cliente(codigo_cliente)
