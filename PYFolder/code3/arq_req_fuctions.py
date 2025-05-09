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

def listar_todos_produtos():
    """
    Função para listar todos os produtos da API Omie, percorrendo todas as páginas.
    """
    url = "https://app.omie.com.br/api/v1/geral/produtos/"
    headers = {
        "Content-type": "application/json"
    }
    
    pagina_atual = 1
    registros_por_pagina = 500
    todos_produtos = []

    while True:
        # Define o payload para a página atual
        payload = {
            "call": "ListarProdutos",
            "param": [
                {
                    "pagina": pagina_atual,
                    "registros_por_pagina": registros_por_pagina,
                    "apenas_importado_api": "N",
                    "filtrar_apenas_omiepdv": "N"
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
            break

        # Processa a resposta
        resposta_json = response.json()
        todos_produtos.extend(resposta_json.get("produtos", []))  # Adiciona os produtos da página atual

        # Verifica se há mais páginas
        pagina_atual += 1
        if pagina_atual > resposta_json.get("total_de_paginas", 1):
            break

    print(f"[INFO] Total de produtos obtidos: {len(todos_produtos)}")
    return todos_produtos

def listar_todos_projetos():
    """
    Função para listar todos os projetos da API Omie, percorrendo todas as páginas.
    """
    url = "https://app.omie.com.br/api/v1/geral/projetos/"
    headers = {
        "Content-type": "application/json"
    }
    
    pagina_atual = 1
    registros_por_pagina = 50
    todos_projetos = []

    while True:
        # Define o payload para a página atual
        payload = {
            "call": "ListarProjetos",
            "param": [
                {
                    "pagina": pagina_atual,
                    "registros_por_pagina": registros_por_pagina,
                    "apenas_importado_api": "N"
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
            break

        # Processa a resposta
        resposta_json = response.json()
        todos_projetos.extend(resposta_json.get("projetos", []))  # Adiciona os projetos da página atual

        # Verifica se há mais páginas
        pagina_atual += 1
        if pagina_atual > resposta_json.get("total_de_paginas", 1):
            break

    print(f"[INFO] Total de projetos obtidos: {len(todos_projetos)}")
    return todos_projetos
