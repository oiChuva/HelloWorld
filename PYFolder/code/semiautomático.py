import requests

nSconsulta = input("Informe o número de série do equipamento:")
print("O número de série informado foi:", nSconsulta)

urlAPI1 = 'https://opusmedical.api.neovero.com/api/Equipamentos/pesquisa'
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8'
}

response = requests.post(urlAPI1, headers=headers, json={"numeroSerie": nSconsulta})

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Obtém o conteúdo da resposta em formato JSON
    data = response.json()
    
    # Extrai o valor do campo "id", remove o ".0" e armazena em uma variável
    equipamento_id = int(data[0]['id'])
    
    print("O ID do equipamento é:", equipamento_id)
else:
    print("Erro ao acessar a API. Código de status:", response.status_code)
