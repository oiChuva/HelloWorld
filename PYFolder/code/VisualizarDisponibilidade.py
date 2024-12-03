import requests
import json
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import threading

# Function to request stock data for a specific stock location and page
def requisicao_consulta_estoque(data_posicao, codigo_local_estoque, nPagina):
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"
    url = "https://app.omie.com.br/api/v1/estoque/consulta/"
    
    dados = {
        "call": "ListarPosEstoque",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "nPagina": nPagina,
                "nRegPorPagina": 1000,
                "dDataPosicao": data_posicao,
                "cExibeTodos": "S",
                "codigo_local_estoque": codigo_local_estoque
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(dados), headers=headers)

    if response.status_code == 200:
        result = response.json()
        if 'produtos' in result:
            df = pd.DataFrame(result['produtos'])
            df_filtrado = df[df['nSaldo'] > 0]
            return df_filtrado
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

# Main function to perform multiple requests
def consultar_multiplos_estoques(data_posicao, progress_bar, progress_label):
    estoques = {
        7279534259: "OPUS VENDAS",
        7281748243: "OPUS LOCAÇÃO",
    }
    todas_respostas = []
    total_produtos = 0

    total_steps = len(estoques) * 5
    step = 0

    for codigo_local_estoque, nome_estoque in estoques.items():
        for pagina in range(1, 6):
            resultado = requisicao_consulta_estoque(data_posicao, codigo_local_estoque, pagina)
            if not resultado.empty:
                todas_respostas.append(resultado)
                total_produtos += len(resultado)
            
            step += 1
            progress = (step / total_steps) * 100
            progress_bar['value'] = progress
            progress_label.config(text=f'Progresso: {int(progress)}%')
            progress_bar.update()

    if todas_respostas:
        df_estoques_concatenados = pd.concat(todas_respostas)
        df_estoques_concatenados.drop_duplicates(subset="cCodigo", keep="first", inplace=True)

        nome_arquivo = "Estoque_temp.xlsx"
        df_estoques_selecionados = df_estoques_concatenados[["cCodigo", "cDescricao", "codigo_local_estoque", "nSaldo"]]
        df_estoques_selecionados.to_excel(nome_arquivo, index=False)
        progress_label.config(text=f"Concluído, temp: {nome_arquivo}")
        visualizar_estoque(nome_arquivo)
    else:
        progress_label.config(text="Nenhum produto encontrado para os estoques e páginas especificados.")

# Function to start the consultation in a separate thread
def iniciar_consulta():
    botao_fazer_requisicao.config(state=tk.DISABLED)
    data_posicao = datetime.now().strftime("%d/%m/%Y")
    threading.Thread(target=consultar_multiplos_estoques, args=(data_posicao, progress_bar, progress_label)).start()

# Function to visualize the Excel file content in Tkinter
def visualizar_estoque(arquivo):
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Visualização de Estoque")
    nova_janela.geometry("800x600")

    df = pd.read_excel(arquivo)

    tree = ttk.Treeview(nova_janela, columns=("cCodigo", "cDescricao", "codigo_local_estoque", "nSaldo"), show='headings')
    tree.heading("cCodigo", text="Código")
    tree.heading("cDescricao", text="Descrição")
    tree.heading("codigo_local_estoque", text="Local de Estoque")
    tree.heading("nSaldo", text="Saldo")

    for index, row in df.iterrows():
        tree.insert("", tk.END, values=(row["cCodigo"], row["cDescricao"], row["codigo_local_estoque"], row["nSaldo"]))

    tree.pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Consulta de Estoque")
root.geometry("600x300")

progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate')
progress_bar.pack(pady=20)

progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.pack(pady=10)

botao_iniciar = tk.Button(root, text="Iniciar Consulta", command=iniciar_consulta)
botao_iniciar.pack(pady=20)

botao_fazer_requisicao = tk.Button(root, text="Visualizar Estoque", state=tk.DISABLED)
botao_fazer_requisicao.pack(pady=20)

root.mainloop()
