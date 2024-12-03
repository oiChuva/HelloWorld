from flask import Flask, render_template, jsonify
from flask_cors import CORS  # Import CORS
import requests
import pandas as pd
import json
from datetime import datetime

date_pos = datetime.now().strftime("%d/%m/%Y")

app = Flask(__name__)
CORS(app)  # Adiciona CORS ao app

def requisicao_consulta_estoque(data_posicao, codigo_local_estoque, nPagina):
    app_key = "1826443506888"
    app_secret = "c9e60167e96e156e2655a92fdcd77df7"
    url = "https://app.omie.com.br/api/v1/estoque/consulta/"
    
    dados = {
        "call": "ListarPosEstoque",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "nPagina": nPagina,
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
            df = pd.DataFrame(result['produtos'])
            df_filtrado = df[df['nSaldo'] > 0]
            return df_filtrado
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def consultar_multiplos_estoques(data_posicao):
    estoques = {
        7257847287: "ALMOXARIFADO OPUS",
        7284481758: "LIMPEZA",
        7292328980: "ESTOQUE VM",
        7281751216: "INSTRUMENTO DE MEDIÇÃO"
    }
    todas_respostas = []
    
    for codigo_local_estoque, nome_estoque in estoques.items():
        for pagina in range(1, 4):
            resultado = requisicao_consulta_estoque(data_posicao, codigo_local_estoque, pagina)
            if not resultado.empty:
                todas_respostas.append(resultado)

    if todas_respostas:
        df_estoques_concatenados = pd.concat(todas_respostas)
        df_estoques_concatenados.drop_duplicates(subset="cCodigo", keep="first", inplace=True)
        
        return df_estoques_concatenados[["cCodigo", "cDescricao", "codigo_local_estoque", "nSaldo"]].to_dict(orient="records")
    else:
        return []

@app.route('/LerEst')
def ler_est():
    data_posicao = date_pos
    resultado = consultar_multiplos_estoques(data_posicao)
    return jsonify(resultado)

@app.route('/PaginaDaApi')
def pag_est():
    return render_template('estoque.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
