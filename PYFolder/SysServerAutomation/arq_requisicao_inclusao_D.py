import requests
import json

def requisicao_inclusao_D(codigo, ncm, descricao_completa, marca, modelo, unidade, codigo_familia, origem_mercadoria, valor_unitario, blocoK):
                            app_key = "3175223491440"
                            app_secret = "7fcdb4ba8e374fbc61db2832ac0857d0"
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