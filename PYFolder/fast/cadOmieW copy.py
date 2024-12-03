import tkinter as tk
from tkinter import messagebox
import requests

def enviar_solicitacao(valor):
    url = "http://192.168.88.215:5000/neovero-receiver"
    data = { "eventType": "nv.orcamento-venda.approved", 
            "message": 
            { 
                "numeroSerie": valor
            }, 
            "detailedMessage": {
                "text": ""
            }, 
            "resource": {"orcamentoVendaUrl": "https://base.neovero.com/api/orcamentosvenda/", 
                "orcamentoVenda": "dados inuteis", 
                "changedFields": 'Lista de campos que foram alterados'
                        }
}
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", f"Sinal enviado com sucesso para {url}: {valor}.")
        else:
            messagebox.showerror("Erro", f"Erro ao enviar sinal para {url}: {valor}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar com {url}: {e}")

def enviar_clique():
    valor = valor_entry.get()

    if valor:
        enviar_solicitacao(valor)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um valor.")

# Criando a janela principal
root = tk.Tk()
root.title("Enviar Solicitação para API")

# Definindo a cor de fundo
cor_principal = "#E5E5E5"
root.configure(bg=cor_principal)

# Criando e configurando o frame principal
frame = tk.Frame(root, padx=20, pady=20, bg=cor_principal)
frame.pack()

label_valor = tk.Label(frame, text="Número de Série:", bg=cor_principal, font=("TkDefaultFont", 12, "bold"))
label_valor.grid(row=0, column=0, padx=10, pady=5, sticky='w')

valor_entry = tk.Entry(frame, width=60, bg="white", font=("TkDefaultFont", 10))
valor_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

enviar_button = tk.Button(frame, text="Enviar", command=enviar_clique, bg="#FF9558", fg="black", font=("TkDefaultFont", 12))
enviar_button.grid(row=1, columnspan=3, padx=10, pady=10)

# Rodando o loop principal do Tkinter
root.mainloop()
