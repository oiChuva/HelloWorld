import tkinter as tk
from tkinter import messagebox
import requests
import urllib3

# Suprimindo avisos de segurança relacionados à desabilitação da verificação SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def enviar_solicitacao(numero_serie):
    url = "https://192.168.88.72:5000/neovero-receiver"
    data = {'numeroSerie': numero_serie}

    try:
        # Desabilitando a verificação SSL
        response = requests.post(url, json=data, verify=False)

        if response.status_code == 200:
            messagebox.showinfo("Sucesso", f"Sinal enviado com sucesso para {url}: {numero_serie}.")
        else:
            messagebox.showerror("Erro", f"Erro ao enviar sinal para {url}: {numero_serie}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar com {url}: {e}")

def enviar_clique():
    numero_serie = valor_entry.get()

    if numero_serie:
        enviar_solicitacao(numero_serie)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um número de série.")

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
valor_entry.grid(row=0, column=1, padx=10, pady=5)

enviar_button = tk.Button(frame, text="Enviar", command=enviar_clique, bg="#009F48", fg="black", font=("TkDefaultFont", 12))
enviar_button.grid(row=1, columnspan=2, padx=10, pady=10)

# Rodando o loop principal do Tkinter
root.mainloop()
