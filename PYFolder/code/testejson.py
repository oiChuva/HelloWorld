import requests

def requisicao_consulta_nf(nCodNF, nNF):
    url_nf = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    dados_nf = {
        "call": "ConsultarNF",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "nCodNF": nCodNF,
                "nNF": nNF
            }
        ]
    }
    response = requests.post(url_nf, json=dados_nf)

    if response.status_code == 200:
        resposta_json = response.json()
        print("Valores retornados da consulta:")
        print(resposta_json)
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)

# Example usage:
nCodNF = '0'
nNF = '3083'
requisicao_consulta_nf(nCodNF, nNF)
