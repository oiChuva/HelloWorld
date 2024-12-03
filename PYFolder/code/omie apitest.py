import requests
import json

def requisicao_consulta_nf(nCodCli):
    # Variáveis fixas para app_key e app_secret
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"

    # URL para onde a requisição será enviada
    url = "https://app.omie.com.br/api/v1/geral/clientes/"

    # Dados que serão enviados no corpo da requisição
    dados = {
        "call": "ConsultarCliente",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "codigo_cliente_omie": nCodCli,
                "codigo_cliente_integracao": ""
            }
        ]
    }

    # Configurando o cabeçalho para indicar que o conteúdo é JSON
    headers = {"Content-Type": "application/json"}

    # Enviando a requisição POST
    response = requests.post(url, data=json.dumps(dados), headers=headers)

    # Verificando a resposta do servidor
    if response.status_code == 200:
        print("Requisição bem-sucedida. Resposta do servidor:")

        # Extrair os valores desejados da resposta JSON
        resposta_json = response.json()

        # Extraindo os dados de endereço da resposta
        endereco = resposta_json.get('endereco', '')
        endereco_numero = resposta_json.get('endereco_numero', '')
        bairro = resposta_json.get('bairro', '')
        cidade = resposta_json.get('cidade', '')
        estado = resposta_json.get('estado', '')
        complemento = resposta_json.get('complemento', '')
        cep = resposta_json.get('cep', '')

        # Juntando os dados em uma única string
        endereco_completo = f"{endereco}, {endereco_numero}, {bairro}, {cidade}, {estado}, {complemento}, {cep}"

        # Retornando os dados de endereço combinados
        return endereco_completo
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)

# Exemplo de uso da função requisicao_consulta_nf
endereco_completo = requisicao_consulta_nf(nCodCli=input("Digite o código do cliente OMIE:"))
print(endereco_completo)
