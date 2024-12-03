import requests
import json
from datetime import datetime

def consultar_posicao_estoque(app_key, app_secret, id_prod=0, data="", apenas_saldo="S"):
    url = "https://app.omie.com.br/api/v1/estoque/consulta/"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "call": "PosicaoEstoque",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "id_prod": id_prod,
            "data": data,
            "apenas_saldo": apenas_saldo
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

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
if __name__ == "__main__":
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"
    id_prod = (input("Digite: "))
    data_atual = datetime.now().strftime("%d/%m/%Y")
    apenas_saldo = ("N")
    
    consultar_posicao_estoque(app_key, app_secret, id_prod, data_atual, apenas_saldo)
