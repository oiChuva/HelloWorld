import requests
import json
import time
import unicodedata
import pythoncom
import win32com.client as win32
from flask import Flask, request, jsonify
from queue import Queue
from threading import Thread

app = Flask(__name__)
queue = Queue()

# Função para remover acentos
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Função para consultar o equipamento
def consultar_equipamento(numero_serie_input):
    max_attempts = 5  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        url = 'https://opusmedical.api.neovero.com/api/Equipamentos/query'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8',  # Substitua pelo seu token
            'Content-Type': 'application/json-patch+json'
        }
        data = {
            "limit": 100,
            "offset": 0,
            "filterGroups": [
                {
                    "combineOperator": "AND",
                    "filters": [
                        {
                            "property": "numeroSerie",
                            "value": numero_serie_input,
                            "combineOperator": "AND"
                        },
                        {
                            "property": "modelo.id",
                            "value": [10, 828],
                            "combineOperator": "OR"
                        }
                    ]
                },
                {
                    "combineOperator": "OR",
                    "filters": [
                        {
                            "property": "modelo.nome",
                            "value": "",
                            "combineOperator": "AND"
                        }
                    ]
                }
            ],
            "orderBy": [
                {
                    "column": "modelo.nome",
                    "ascending": True
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)  # Timeout em 10 segundos
            print(f"Attempt {attempt + 1}: Status Code: {response.status_code}")

            if response.status_code == 200:
                response_json = response.json()

                if isinstance(response_json, dict) and isinstance(response_json.get('records'), list):
                    records = response_json['records']
                    filtered_items = [item for item in records if item.get("numeroSerie") == numero_serie_input]

                    if not filtered_items:
                        print(f"Equipamento com número de série {numero_serie_input} não encontrado.")
                        return {"error": "Equipamento não encontrado"}

                    data = filtered_items[0]
                    numero_serie = data.get("numeroSerie", None)
                    patrimonio = data.get("patrimonio", None)
                    nome = data.get("nome", None)
                    modelo_nome = data.get("modelo", {}).get("nome", None)
                    fabricante_nome = data.get("modelo", {}).get("fabricante", {}).get("nome", None)
                    familia_nome = data.get("modelo", {}).get("familia", {}).get("nome", None)
                    valor_aquisicao = data.get("valorAquisicao", None)
                    cliente_id = data.get("clienteId", None)

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
                        "valorAquisicao": valor_aquisicao,
                        "clienteId": cliente_id
                    }

                    print(resposta_desejada)

                    if numero_serie:
                        print("Número de Série:", numero_serie)
                        print("Patrimônio:", patrimonio)
                        print("Nome do Equipamento:", nome)
                        print("Nome do Modelo:", modelo_nome)
                        print("Fabricante do Modelo:", fabricante_nome)
                        print("Família do Modelo:", familia_nome)
                        print("Valor de Aquisição:", valor_aquisicao)
                        print("Cliente ID:", cliente_id)

                        if patrimonio:
                            codOMIE = numero_serie + "-EQ" + patrimonio
                            descOMIE = nome + " " + numero_serie
                            blocoK = "08"
                        else:
                            if cliente_id:
                                codOMIE = numero_serie + "-CL"
                            else:
                                codOMIE = numero_serie + "-EQ"
                            descOMIE = nome + " " + numero_serie
                            blocoK = "99"

                        print(codOMIE)

                        if familia_nome == "ARCO CIRURGICO" or familia_nome == "CARRO MONITOR" or familia_nome == "RAIO-X":
                            Ncm = "9022.14.19"
                        elif familia_nome == "ULTRASSOM":
                            Ncm = "9018.12.10"
                        elif "TRANSDUTOR" in familia_nome:
                            Ncm = "9018.19.90"
                        elif familia_nome == "VIDEO PRINTER":
                            Ncm = "9022.14.19"
                        elif familia_nome == "DEA":
                            Ncm = "9018.90.96"
                        elif familia_nome == "MONITOR MULTIPARAMETRO":
                            Ncm = "9018.19.80"
                        else:
                            Ncm = "9999.99.99"

                        if familia_nome == "ARCO CIRURGICO" or familia_nome == "CARRO MONITOR" or familia_nome == "RAIO-X":
                            CodFamilia = "7257939493"
                        elif familia_nome == "7345596682":
                            CodFamilia = "7325470580"
                        elif familia_nome == "ULTRASSOM":
                            CodFamilia = "7281767348"
                        elif "TRANSDUTOR" in familia_nome:
                            CodFamilia = "7281767246"
                        elif familia_nome == "VIDEO PRINTER":
                            CodFamilia = "7281766997"
                        elif familia_nome == "MONITOR MULTIPARAMETRO":
                            CodFamilia = "7281771794"
                        elif familia_nome == "FONTE":
                            CodFamilia = "7311711664"
                        elif familia_nome == "NOBREAK":
                            CodFamilia = "7283633935"
                        elif familia_nome == "MAMOGRAFO":
                            CodFamilia = "7313952606"
                        elif familia_nome == "DEA":
                            CodFamilia = "7316078524"
                        elif familia_nome == "CAMA HOSPITALAR":
                            CodFamilia = "7302443424"
                        elif familia_nome == "MESA CIRURGICA" or familia_nome == "ACESSORIO MESA":
                            CodFamilia = "7313811760"
                        elif familia_nome == "TOMOGRAFIA":
                            CodFamilia = "7281766618"
                        elif familia_nome == "VENTILADOR PULMONAR" or familia_nome == "VENTILADOR DE TRANSPORTE":
                            CodFamilia = "7281767228"
                        elif familia_nome == "ASPIRADOR CIRURGICO":
                            CodFamilia = "7281771910"
                        elif familia_nome == "BATERIA":
                            CodFamilia = "7325470580"
                        elif familia_nome == "ELETROCARDIOGRAFO":
                            CodFamilia = "7312162428"
                        elif familia_nome == "FOCO CIRURGICO":
                            CodFamilia = "7281767369"
                        elif familia_nome == "MAQUINA DE ANESTESIA":
                            CodFamilia = "7281767561"
                        elif familia_nome == "POLIGRAFO":
                            CodFamilia = "7281766206"
                        elif familia_nome == "ELETROENCEFALOGRAFO":
                            CodFamilia = "7281766174"
                        elif familia_nome == "SISTEMA DE INFUSAO":
                            CodFamilia = "7281766533"
                        elif familia_nome == "OXIMETRO DE PULSO":
                            CodFamilia = "7345596682"
                        elif familia_nome == "OXIMETRO DE DEDO":
                            CodFamilia = "7345596682"
                        elif familia_nome == "DESFIBRILADOR":
                            CodFamilia = "7281766758"
                        elif familia_nome == "ANALISADOR DE GASES" or familia_nome == "ANALISADOR DE HEMATOLOGIA":
                            CodFamilia = "7281765910"
                        elif familia_nome == "IMPRESSORA" or familia_nome == "CARRO TRANSPORTE IMPRESSORA":
                            CodFamilia = "7281766248"
                        elif familia_nome == "BOMBA DE INFUSAO":
                            CodFamilia = "7281766345"
                        elif familia_nome == "CENTRIFUGA":
                            CodFamilia = "7281766366"
                        elif familia_nome == "COLPOSCOPIO":
                            CodFamilia = "7281766550"
                        elif familia_nome == "POLISSONOGRAFO":
                            CodFamilia = "7281766782"
                        elif familia_nome == "REVELADOR":
                            CodFamilia = "7281766935"
                        elif familia_nome == "INCUBADORA":
                            CodFamilia = "7281766395"
                        elif familia_nome == "MAQUINA DE LAVAR ENDOSCOPIA":
                            CodFamilia = "7281767440"
                        elif familia_nome == "MICROSCOPIO":
                            CodFamilia = "7281767428"
                        elif familia_nome == "VENTILADOR DE TRANSPORTE":
                            CodFamilia = "7281767451"
                        elif familia_nome == ["ANALISADOR DE COAGULACAO", "ANALISADOR DE MULTIPARAMETROS", "MULTIMETRO", "LUXIMETRO",
                            "ANALIZADOR DE BISTURI", "ANALISADOR DE VENTILADOR PULMONAR", "ANALISADOR DE SEGURANCA ELETRICA", "ANALISADOR DE QUALIFICACAO TERMICA",
                            "ANALISADOR DE NIBP", "CAPACIMETRO", "TRENA LASER", "NIVEL LASER", "TERMO-HIGROMETRO"]:
                            CodFamilia = "7281766525"
                        else:
                            CodFamilia = "7281765596"

                        print(CodFamilia)

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
                                print("Produto incluído com sucesso no OMIE.")
                                return True  # Indica que o produto foi incluído com sucesso
                            else:
                                print("Erro na requisição. Código de status:", response.status_code)
                                print(response.text)
                                print("Erro ao incluir produto no OMIE.")
                                return False  # Indica que houve um erro ao incluir o produto

                        # Faz a requisição de inclusão e verifica o resultado
                        inclusao_ok = requisicao_inclusao(
                            codigo=codOMIE,
                            ncm=Ncm,
                            descricao_completa=descOMIE,
                            unidade="UN",
                            modelo=modelo_nome,
                            marca=fabricante_nome,
                            codigo_familia=CodFamilia,
                            origem_mercadoria="0",
                            valor_unitario=valor_aquisicao * 0.7
                        )

                        # Enviar email com base no resultado da inclusão
                        if inclusao_ok:
                            enviar_email(numero_serie_input, codOMIE)

                        return resposta_desejada  # Retorna os dados do equipamento
                    else:
                        return {"error": "Número de série não encontrado"}
                else:
                    print("Erro ao acessar a API. Código de status:", response.status_code)
                    return {"error": "Erro ao acessar a API"}

        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição: {e}")
            return {"error": f"Erro de requisição: {e}"}
        
        except ValueError as e:
            print(f"Resposta não é um JSON válido: {e}")
            return {"error": f"Resposta não é um JSON válido: {e}"}
        
        except Exception as e:
            print(f"Erro não esperado: {e}")
            return {"error": f"Erro não esperado: {e}"}
        
        else:
            # Incrementa a tentativa
            attempt += 1
            print(f"Tentativa {attempt} de consulta.")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente

    # Se todas as tentativas falharem
    print("Erro ao acessar a API após várias tentativas.")
    return {"error": "Erro ao acessar a API após várias tentativas"}

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
                    "app_secret": "4a98af31f25d8b152a18911c65d23190",
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

# Função para processar a fila de requisições
def process_queue():
    while True:
        numero_serie = queue.get()
        result = consultar_equipamento(numero_serie)
        if 'error' not in result:
            # Não faz nada aqui, porque o email já é enviado na função consultar_equipamento
            pass
        queue.task_done()

# Função para enviar email
# Função para enviar email
def enviar_email(numero_serie, codOMIE):
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = "cadastro@opusmedical.com.br; augusto@opusmedical.com.br; almoxarifado@opusmedical.com.br; comercial@opusmedical.com.br; logistica@opusmedical.com.br; suportetecnico@opusmedical.com.br"
    email.Subject = "Cadastrado"
    email.HTMLBody = f"""
        <p>Itens cadastrados.</p>
        <p>O equipamento com número de série {numero_serie} foi cadastrado com sucesso no OMIE.</p>
        <p>Código OMIE: {codOMIE}</p>
    """
    try:
        email.Send()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def Send_Email(ht_mail):
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = "logistica@opusmedical.com.br; augusto@opusmedical.com.br; almoxarifado@opusmedical.com.br"
    email.Subject = "Requisição de item do estoque"
    email.HTMLBody = ht_mail
    email.Send()
    print("Email enviado.")
    # Exibir mensagem de sucesso
    print("Sucesso", "Email enviado com sucesso!")

# Thread para processar a fila de forma assíncrona
queue_thread = Thread(target=process_queue)
queue_thread.daemon = True
queue_thread.start()

# Rota para o webhook
@app.route('/neovero-receiver', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")
    numero_serie_input = data.get('numeroSerie')
    if not numero_serie_input:
        return jsonify({"error": "numeroSerie is required"}), 400
    
    # Adiciona o número de série à fila para processamento
    queue.put(numero_serie_input)
    
    return jsonify({"message": "Recebido com sucesso e adicionado à fila"})

# Rota para o segundo webhook
@app.route('/neovero-end-c', methods=['POST'])
def webhook_end_c():
    data = request.json
    print(f"Received data from /neovero-end-c: {data}")
    codigo_cliente = data.get('codigo_cliente')
    if not codigo_cliente:
        return jsonify({"error": "codigo_cliente is required"}), 400
    
    cadastrar_cliente(codigo_cliente)
    
    return jsonify({"message": "Recebido com sucesso pelo Endpoint"})

@app.route('/SolEstoque', methods=['POST'])
def webhook_end_s():
    data = request.json
    ht_mail = data.get('ht_mail')
    if not ht_mail:
        return jsonify({"error": "ht_mail is required"}), 400
    
    Send_Email()

    return jsonify({"message": "Recebido com sucesso pelo Endpoint"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
