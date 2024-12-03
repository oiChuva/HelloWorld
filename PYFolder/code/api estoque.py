import requests
import json

def requisicao_consulta_estoque(nPagina, nRegPorPagina):
    url_api = "https://app.omie.com.br/api/v1/estoque/consulta/"
    dados_api = {
        "call": "ListarPosEstoque",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "nPagina": nPagina,
                "nRegPorPagina": nRegPorPagina,
                "cExibeTodos": "N",
                "codigo_local_estoque": 0
            }
        ]
    }
    response = requests.post(url_api, json=dados_api)

    if response.status_code == 200:
        resposta_json = response.json()
        produtos = resposta_json.get("produtos", [])
        nTotPaginas = resposta_json.get("nTotPaginas", 1)  # Total de páginas na resposta

        # Filtrar produtos com nSaldo diferente de 0 e extrair somente os campos desejados
        produtos_filtrados = [
            {
                "cDescricao": produto["cDescricao"],
                "codigo_local_estoque": produto["codigo_local_estoque"],
                "nSaldo": produto["nSaldo"]
            }
            for produto in produtos if produto["nSaldo"] != 0
        ]
        
        # Atualizar a resposta JSON com os produtos filtrados e o número de páginas
        resposta_final = {
            "nTotPaginas": nTotPaginas,
            "produtos": produtos_filtrados
        }
        
        resposta_formatada = json.dumps(resposta_final, indent=4, ensure_ascii=False)
        print(resposta_formatada)
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)

# Exemplo de uso
requisicao_consulta_estoque(1, 1000)
