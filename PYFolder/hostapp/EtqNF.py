import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import os

hostapp_dir = os.path.dirname(os.path.abspath(__file__))
# Funções para interação com a API
def apinum1(nNF):
    url_nf = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    dados_nf = {
        "call": "ConsultarNF",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "nNF": nNF
            }
        ]
    }
    response = requests.post(url_nf, json=dados_nf)
    if response.status_code == 200:
        resposta_json = response.json()
        produtos = resposta_json.get("det", [])
        nCodCliNF = resposta_json.get("nfDestInt", {}).get("nCodCli")
        cnpj_cpf = resposta_json.get("nfDestInt", {}).get("cnpj_cpf")
        cRazao = resposta_json.get("nfDestInt", {}).get("cRazao")
        nNF = resposta_json.get("ide", {}).get("nNF")
        
        return nNF, nCodCliNF, produtos, cRazao, cnpj_cpf

    else:
        messagebox.showerror("Erro", f"Erro na requisição. Código de status: {response.status_code}")
        return None, None, None, None, None

def apinum2(nCodCli):
    if nCodCli is None:
        messagebox.showerror("Erro", "Não foi possível consultar o cliente devido a um erro anterior.")
        return None
    
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"
    url = "https://app.omie.com.br/api/v1/geral/clientes/"
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
    
    response = requests.post(url, json=dados)
    if response.status_code == 200:
        resposta_json = response.json()
        endereco = resposta_json.get("endereco")
        endereco_numero = resposta_json.get('endereco_numero', '')
        bairro = resposta_json.get('bairro', '')
        cidade = resposta_json.get('cidade', '')
        complemento = resposta_json.get('complemento', '')
        cep = resposta_json.get('cep', '')
        endereco_completo = f"{endereco}, {endereco_numero}, {bairro}, {cidade}, {complemento}, {cep}"
        return endereco_completo
    else:
        messagebox.showerror("Erro", f"Erro na requisição. Código de status: {response.status_code}")
        return None

def gerar_planilha():
    nNF_input = nf_entry.get()
    volumes = volume_entry.get()

    nNF, nCodCliNF, produtos, cRazao, cnpj_cpf = apinum1(nNF=nNF_input)
    endereco = apinum2(nCodCli=nCodCliNF)

    if None not in [nNF, nCodCliNF, produtos, cRazao, cnpj_cpf, endereco]:
        remetente = "Opus Medical e Eletronics LTDA\nCNPJ: 14.368.486/0001-20"
        dados_produtos = []
        for produto in produtos:
            detalhe_produto = {
                'Nota Fiscal': nNF,
                'Remetente': remetente,
                'Destinatário': cRazao,
                'CNPJ/CPF Destinatário': cnpj_cpf,
                'Endereço Destinatário': endereco,
                'Descrição Produto': produto['prod']['xProd'],
                'Código Produto': produto['prod']['cProd'],
                'Quantidade': produto['prod'].get("qCom"),
                'Volume': volumes
            }
            dados_produtos.append(detalhe_produto)

        df = pd.DataFrame(dados_produtos)
        df.to_excel(os.path.join(hostapp_dir, f"plan_{nNF}.xlsx"), index=False)
        messagebox.showinfo("Sucesso", f"Planilha 'plan_{nNF}.xlsx' gerada com sucesso.")
        root.destroy()
    else:
        messagebox.showerror("Erro", "Não foi possível obter todos os dados necessários.")
        root.destroy()

# Interface Tkinter
root = tk.Tk()
root.title("Gerador de Planilhas")

# Label e Entry para Nota Fiscal
ttk.Label(root, text="Número da Nota Fiscal:").grid(row=0, column=0, padx=10, pady=10)
nf_entry = ttk.Entry(root)
nf_entry.grid(row=0, column=1, padx=10, pady=10)

# Label e Entry para Volume
ttk.Label(root, text="Volume:").grid(row=1, column=0, padx=10, pady=10)
volume_entry = ttk.Entry(root)
volume_entry.grid(row=1, column=1, padx=10, pady=10)

# Botão para gerar planilha
gerar_btn = ttk.Button(root, text="Gerar Planilha", command=gerar_planilha)
gerar_btn.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()