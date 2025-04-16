import requests
import json

# Função para realizar a requisição à API e retornar os dados como JSON
def lerEstoque(data_posicao):
    app_key = "1826443506888"
    app_secret = "c9e60167e96e156e2655a92fdcd77df7"
    url = "https://app.omie.com.br/api/v1/estoque/consulta/"
    
    estoques = {
        7257847287: "ALMOXARIFADO OPUS",
        7284481758: "LIMPEZA",
        7292328980: "ESTOQUE VM",
        7281751216: "INSTRUMENTO DE MEDIÇÃO"
    }
    
    todas_respostas = []

    for codigo_local_estoque, nome_estoque in estoques.items():
        for pagina in range(1, 4):  # Limite de 3 páginas
            dados = {
                "call": "ListarPosEstoque",
                "app_key": app_key,
                "app_secret": app_secret,
                "param": [
                    {
                        "nPagina": pagina,
                        "nRegPorPagina": 1000,
                        "dDataPosicao": data_posicao,
                        "cExibeTodos": "N",
                        "codigo_local_estoque": codigo_local_estoque
                    }
                ]
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(dados), headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if 'produtos' in result:
                    todas_respostas.extend(result['produtos'])

    # Retornar todos os dados consolidados como JSON
    return todas_respostas
