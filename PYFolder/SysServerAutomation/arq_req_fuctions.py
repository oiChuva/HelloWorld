import requests
import json

def incluir_requisicao_compra(codIntReqCompra, codProj, dtSugestao, obsIntReqCompra, codItem, codProd, qtde):
    """
    Função para incluir uma requisição de compra na API Omie.
    Recebe os seguintes parâmetros:
        - codIntReqCompra: Código interno da requisição de compra.
        - codProj: Código do projeto.
        - dtSugestao: Data sugerida para a requisição.
        - obsIntReqCompra: Observação interna da requisição.
        - codItem: Código do item.
        - codProd: Código do produto.
        - qtde: Quantidade do item.
    """
    # Define o endpoint da API e os headers
    url = "https://app.omie.com.br/api/v1/produtos/requisicaocompra/"
    headers = {
        "Content-type": "application/json"
    }

    # Define o payload com as variáveis recebidas
    payload = {
        "call": "IncluirReq",
        "param": [
            {
                "codCateg": "2.03.98",
                "codIntReqCompra": codIntReqCompra,
                "codProj": codProj,
                "dtSugestao": dtSugestao,
                "obsIntReqCompra": obsIntReqCompra,
                "ItensReqCompra": [
                    {
                        "codItem": codItem,
                        "codProd": codProd,
                        "precoUnit": 1,  # Valor fixo, pode ser ajustado se necessário
                        "qtde": qtde
                    }
                ]
            }
        ],
        "app_key": "1826443506888",  # Inclui app_key diretamente no JSON
        "app_secret": "c9e60167e96e156e2655a92fdcd77df7"  # Inclui app_secret diretamente no JSON
    }

    # Faz a requisição POST
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Retorna o status e o corpo da resposta
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    return response

def consultar_produto(codItem):
    """
    Função para consultar um produto específico na API Omie com base no código do produto.
    Retorna o codProd do produto consultado.
    """
    url = "https://app.omie.com.br/api/v1/geral/produtos/"
    headers = {
        "Content-type": "application/json"
    }

    # Define o payload com o código do produto
    payload = {
        "call": "ConsultarProduto",
        "param": [
            {
                "codigo": codItem
            }
        ],
        "app_key": "1826443506888",  # Inclui app_key diretamente no JSON
        "app_secret": "c9e60167e96e156e2655a92fdcd77df7"  # Inclui app_secret diretamente no JSON
    }

    # Faz a requisição POST
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"[ERROR] Falha na requisição. Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        return None

    # Processa a resposta
    resposta_json = response.json()
    codProd = resposta_json.get("codigo_produto")
    if not codProd:
        print(f"[ERROR] codProd não encontrado para o produto com código {codItem}.")
        return None

    print(f"[INFO] Produto consultado: {resposta_json}")
    return codProd

