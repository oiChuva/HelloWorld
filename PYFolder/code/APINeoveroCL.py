import tkinter as tk
from tkinter import messagebox
import requests

def enviar_solicitacoes():
    # Obter o código do cliente do campo de entrada
    codCLI = entry_codCLI.get()

    # Solicitação para a API Neovero
    response_neovero = requests.post(url_neovero, json={"codigo": codCLI, "empresaId": 1, "ativo": True}, headers=headers_neovero)

    # Verificar se a solicitação para a API Neovero foi bem-sucedida
    if response_neovero.status_code == 200:
        response_data_neovero = response_neovero.json()
        messagebox.showinfo("Resposta Neovero", str(response_data_neovero))
        
        cliente_neovero = response_data_neovero[0]
        idCODi = cliente_neovero['id']
        razaoSocial = cliente_neovero['razaosocial']
        nomeFantasia = cliente_neovero['nomefantasia']
        cnpjCpf = cliente_neovero['cnpj']

        # Solicitação para a API Omie
        response_omie = requests.post(url_omie, json={"call": "IncluirCliente", "app_key": "1826443506888", "app_secret": "4a98af31f25d8b152a18911c65d23190", "param": [{"codigo_cliente_integracao": idCODi, "razao_social": razaoSocial, "nome_fantasia": nomeFantasia, "cnpj_cpf": cnpjCpf}]}, headers=headers_omie)

        # Verificar se a solicitação para a API Omie foi bem-sucedida
        if response_omie.status_code == 200:
            response_data_omie = response_omie.json()
            messagebox.showinfo("Resposta Omie", str(response_data_omie))
        else:
            response_data_omie = response_omie.json()
            faultstring = response_data_omie.get('faultstring', 'Erro desconhecido')
            messagebox.showerror("Erro Omie", f"Erro na solicitação para a API Omie: {faultstring}")
    else:
        messagebox.showerror("Erro Neovero", f"Erro {response_neovero.status_code} ao enviar a solicitação para a API Neovero.")

# Configurações da janela principal
root = tk.Tk()
root.title("Consulta de Clientes")

# URL da API Neovero
url_neovero = 'https://opusmedical.api.neovero.com/api/clientes/pesquisa'
# URL da API Omie
url_omie = "https://app.omie.com.br/api/v1/geral/clientes/"

# Cabeçalhos da solicitação para a API Neovero
headers_neovero = {'accept': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMTI2IiwianRpIjoiMTEyNiIsImlhdCI6MTcxMjA4MjU4MCwic3ViIjoiaW50ZWdyYWNhb19hcGkiLCJkb21haW4iOiJvcHVzbWVkaWNhbC5hcGkubmVvdmVyby5jb20iLCJuYmYiOjE3MTIwODI1ODAsImV4cCI6MTcxMjA4NjE4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdCIsImF1ZCI6ImU2YjBmOTNiNjAyNTQ0MDg5ZDM0MzZmYWJjNWI0YWIwIn0.uH7yBN_f9k1bG1IWij9NGPzohwv8qyWWsjg7kNemBA8', 'Content-Type': 'application/json' }
# Cabeçalhos da solicitação para a API Omie
headers_omie = {'Content-Type': 'application/json'}

# Rótulo e campo de entrada para o código do cliente
label_codCLI = tk.Label(root, text="Código do Cliente:")
label_codCLI.grid(row=0, column=0, padx=10, pady=5)
entry_codCLI = tk.Entry(root)
entry_codCLI.grid(row=0, column=1, padx=10, pady=5)

# Botão para enviar as solicitações
button_enviar = tk.Button(root, text="Enviar Solicitações", command=enviar_solicitacoes)
button_enviar.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Função para fechar a janela
def fechar_janela():
    root.destroy()

# Botão para sair
button_sair = tk.Button(root, text="Sair", command=fechar_janela)
button_sair.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Loop principal da aplicação
root.mainloop()
