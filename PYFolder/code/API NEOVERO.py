import json
import requests
import unicodedata

def remove_accents(input_str):
    decoded_str = input_str.encode().decode('unicode-escape')
    nfkd_form = unicodedata.normalize('NFKD', decoded_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def consultar_equipamento(numero_serie):
    urlAPI1 = 'https://opusmedical.api.neovero.com/api/Equipamentos/pesquisa'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8'
    }

    response = requests.post(urlAPI1, headers=headers, json={"numeroSerie": numero_serie})

    if response.status_code == 200:
        data = response.json()
        equipamento_id = str(int(data[0]['id']))
        variavelURL = equipamento_id

        url = 'https://opusmedical.api.neovero.com/api/Equipamentos/' + variavelURL + '?api-version=1'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            numero_serie = data.get("numeroSerie", None)
            patrimonio = data.get("patrimonio", None)
            nome = data.get("nome", None)
            modelo_nome = data.get("modelo", {}).get("nome", None)
            fabricante_nome = data.get("modelo", {}).get("fabricante", {}).get("nome", None)
            familia_nome = data.get("modelo", {}).get("familia", {}).get("nome", None)
            valor_aquisicao = data.get("valorAquisicao", None)
            
            if nome:
                nome = remove_accents(nome)
            if modelo_nome:
                modelo_nome = remove_accents(modelo_nome)
            if fabricante_nome:
                fabricante_nome = remove_accents(fabricante_nome)
            if familia_nome:
                familia_nome = remove_accents(familia_nome)
            
            resposta_desejada = {
                "numeroSerie": numero_serie,
                "patrimonio": patrimonio,
                "nome": nome,
                "modelo": {
                    "nome": modelo_nome,
                    "fabricante": {
                        "nome": fabricante_nome
                    },
                    "familia": {
                        "nome": familia_nome
                    }
                },
                "valorAquisicao": valor_aquisicao
            }

            if numero_serie:
                print("Número de Série:", numero_serie)
                print("Patrimônio:", patrimonio)
                print("Nome do Equipamento:", nome)
                print("Nome do Modelo:", modelo_nome)
                print("Fabricante do Modelo:", fabricante_nome)
                print("Família do Modelo:", familia_nome)
                print("Valor de Aquisição:", valor_aquisicao)

                if patrimonio:
                    codOMIE = (numero_serie + "-EQ" + patrimonio)
                    descOMIE = (nome + " " + numero_serie)
                    blocoK = "08"
                    if familia_nome == "CARRO MONITOR":
                        codOMIE = ("CM" + codOMIE)
                    else:
                        codOMIE = (codOMIE)
                else:
                    codOMIE = (numero_serie + "-CL")
                    descOMIE = (nome + " " + numero_serie)
                    blocoK = "99"
                    if familia_nome == "CARRO MONITOR":
                        codOMIE = ("CM" + codOMIE)
                    else:
                        codOMIE = (codOMIE)

                if familia_nome == "ARCO CIRURGICO" or familia_nome == "CARRO MONITOR":
                    Ncm = "9022.14.19"
                elif familia_nome == "ULTRASSOM":
                    Ncm = "9018.12.10"
                elif "TRANSDUTOR" in familia_nome:
                    Ncm = "9018.19.90"
                elif familia_nome == "VIDEO PRINTER":
                    Ncm = "9022.14.19"
                else:
                    Ncm = "9999.99.99"

                if familia_nome == "ARCO CIRURGICO" or familia_nome == "CARRO MONITOR":
                    CodFamilia = "7257939493"
                elif familia_nome == "ULTRASSOM":
                    CodFamilia = "7281767348"
                elif "TRANSDUTOR" in familia_nome:
                    CodFamilia = "7281767246"
                elif familia_nome == "VIDEO PRINTER":
                    CodFamilia = "7281766997"
                else:
                    CodFamilia = "7281765596"

                def requisicao_inclusao(codigo, ncm, descricao_completa, marca, modelo, unidade, codigo_familia, origem_mercadoria, valor_unitario):
                    app_key = "1826443506888"
                    app_secret = "4a98af31f25d8b152a18911c65d23190"
                    url = "https://app.omie.com.br/api/v1/geral/produtos/"

                    dados = { 
                        "call": "IncluirProduto",
                        "app_key": app_key,
                        "app_secret": app_secret,
                        "param": [
                            {
                                "codigo_produto_integracao": codigo,
                                "codigo": codigo,
                                "ncm": ncm,
                                "descricao": descricao_completa,
                                "marca": marca,
                                "modelo": modelo,
                                "unidade": unidade,
                                "codigo_familia": codigo_familia,
                                "valor_unitario": valor_unitario,
                                "tipoItem": blocoK,
                                "recomendacoes_fiscais": {
                                    "origem_mercadoria": origem_mercadoria
                                }
                            }
                        ]
                    }

                    headers = {"Content-Type": "application/json"}

                    response = requests.post(url, data=json.dumps(dados), headers=headers)

                    if response.status_code == 200:
                        print("Requisição bem-sucedida. Resposta do servidor:")
                        print(response.json())
                    else:
                        print("Erro na requisição. Código de status:", response.status_code)
                        print(response.text)

                requisicao_inclusao(
                    codigo=codOMIE,
                    ncm=Ncm,
                    descricao_completa=descOMIE,
                    unidade="UN",
                    modelo=modelo_nome,
                    marca=fabricante_nome,
                    codigo_familia=CodFamilia,
                    origem_mercadoria="0",
                    valor_unitario=valor_aquisicao
                )

        else:
            print("Erro:", response.status_code)

# Example usage
consultar_equipamento(input("Número de Série: "))
