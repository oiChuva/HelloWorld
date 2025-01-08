import requests
import time
from arq_remove_accents import remove_accents
from arq_enviar_email import enviar_email

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
                    modelo_nome = data.get("modelo", {}).get("nome", None)
                    fabricante_nome = data.get("modelo", {}).get("fabricante", {}).get("nome", None)
                    familia_nome = data.get("modelo", {}).get("familia", {}).get("nome", None)
                    valor_aquisicao = data.get("valorAquisicao", None)
                    cliente_id = data.get("clienteId", None)
                    empresa_id = data.get("empresa", {}).get("id", None)

                    if modelo_nome:
                        modelo_nome = remove_accents(modelo_nome)
                    if fabricante_nome:
                        fabricante_nome = remove_accents(fabricante_nome)
                    if familia_nome:
                        familia_nome = remove_accents(familia_nome)

                    resposta_desejada = {
                        "numeroSerie": numero_serie,
                        "patrimonio": patrimonio,
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
                        "clienteId": cliente_id,
                        "empresaId": empresa_id
                    }

                    print(resposta_desejada)

                    nome = (familia_nome + "|" + modelo_nome + "("+ fabricante_nome +")")

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
                            blocoK = "08"
                            print(f"Definindo codOMIE como EQ devido ao patrimônio: {codOMIE}")
                        elif cliente_id:
                            codOMIE = numero_serie + "-CL"
                            blocoK = "99"
                            print(f"Definindo codOMIE como CL devido ao cliente_id: {codOMIE}")
                        else:
                            codOMIE = numero_serie + "-EQ"
                            blocoK = "99"
                            print(f"Definindo codOMIE como EQ por padrão: {codOMIE}")

                        print(f"Descrição final: {nome}, BlocoK: {blocoK}")


                        if familia_nome == "ARCO CIRURGICO" or familia_nome == "CARRO MONITOR" or familia_nome == "RAIO-X" or familia_nome == "RAIO-X PORTATIL" or familia_nome == "EQUIPAMENTO DE RAIO-X MOVEL":
                            Ncm = "9022.14.19"
                        elif familia_nome == "CAMA HOSPITALAR" or familia_nome == "MESA CIRURGICA":
                            Ncm = "9402.90.20"
                        elif familia_nome == "FOCO HOSPITALAR":
                            Ncm = "9405.11.10"
                        elif familia_nome == "MONITOR MULTIPARAMETRO":
                            Ncm = "9018.19.80"
                        elif familia_nome == "ULTRASSOM":
                            Ncm = "9018.12.10"
                        elif "TRANSDUTOR" in familia_nome:
                            Ncm = "9018.19.90"
                        elif familia_nome == "VIDEO PRINTER":
                            Ncm = "9022.14.19"
                        else:
                            Ncm = "9999.99.99"

                        if familia_nome == "ARCO CIRURGICO":
                            CodFamilia = "7257939493"
                        elif familia_nome == "CARRO MONITOR":
                            CodFamilia = "7387297711"
                        elif familia_nome == "IMPRESSORA":
                            CodFamilia = "7387344116"
                        elif familia_nome == "RAIO-X" or familia_nome == "EQUIPAMENTO DE RAIO-X MOVEL":
                            CodFamilia = "7313956365"
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
                        elif familia_nome == "FOCO HOSPITALAR":
                            CodFamilia = "7302639730"
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
                            CodFamilia = "7281766230"
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
                        elif familia_nome == "RAIO-X PORTATIL":
                            CodFamilia = "7281767309"
                        else:
                            CodFamilia = "7281765596"

                        print(CodFamilia)

                        resposta_desejada = {
                        "numeroSerie": numero_serie,
                        "patrimonio": patrimonio,
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
                        "clienteId": cliente_id,
                        "empresaId": empresa_id
                        }
    
                        print(resposta_desejada)

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
