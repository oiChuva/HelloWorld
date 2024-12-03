import requests
import win32com.client as win32
import json
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import threading
import os

# Função para realizar a requisição à API para um estoque e página específicos
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

# Função principal para realizar múltiplas requisições
def consultar_multiplos_estoques(data_posicao, progress_bar, progress_label):
    estoques = {
        7257847287: "ALMOXARIFADO OPUS",
        7279534259: "OPUS VENDAS",
        7281748243: "OPUS LOCAÇÃO",
        7281751216: "INSTRUMENTO DE MEDIÇÃO",
        7284481758: "LIMPEZA",
        7284957048: "TECNICA",
        7292328980: "ESTOQUE VM"
    }
    todas_respostas = []
    total_produtos = 0

    total_steps = len(estoques) * 3
    step = 0

    for codigo_local_estoque, nome_estoque in estoques.items():
        for pagina in range(1, 4):
            resultado = requisicao_consulta_estoque(data_posicao, codigo_local_estoque, pagina)
            if not resultado.empty:
                todas_respostas.append(resultado)
                total_produtos += len(resultado)
            
            step += 1
            progress = (step / total_steps) * 100
            progress_bar['value'] = progress
            progress_label.config(text=f'Progresso: {int(progress)}%')
            progress_bar.update()

    df_estoques_concatenados = pd.concat(todas_respostas)
    df_estoques_concatenados.drop_duplicates(subset="cCodigo", keep="first", inplace=True)

    if not df_estoques_concatenados.empty:
        nome_arquivo = "Estoque_temp.xlsx"
        df_estoques_selecionados = df_estoques_concatenados[["cCodigo", "cDescricao", "codigo_local_estoque", "nSaldo"]]
        df_estoques_selecionados.to_excel(nome_arquivo, index=False)
        progress_label.config(text=f"Concluído, temp: {nome_arquivo}")
        botao_fazer_requisicao.config(state=tk.NORMAL)
    else:
        progress_label.config(text="Nenhum produto encontrado para os estoques e páginas especificados.")

# Função para iniciar a consulta em uma thread separada
def iniciar_consulta():
    botao_fazer_requisicao.config(state=tk.DISABLED)
    data_posicao = datetime.now().strftime("%d/%m/%Y")
    threading.Thread(target=consultar_multiplos_estoques, args=(data_posicao, progress_bar, progress_label)).start()

def abrir_nova_janela():
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Fazer Requisição")
    nova_janela.geometry("900x400")

    global pR2_Desc, pR2_Quant, pR2_Cod, data_entrega
    pR2_Desc = tk.StringVar()
    pR2_Quant = tk.IntVar()
    pR2_Cod = tk.StringVar()
    data_entrega = tk.StringVar()

    solicitante_var = tk.StringVar()
    motivo_os_var = tk.StringVar()

    df = pd.read_excel("Estoque_temp.xlsx")
    lista_produtos = df.apply(lambda row: f"{row['cCodigo']} - {row['cDescricao']}", axis=1).tolist()

    def atualizar_combobox(event):
        typed = lista_combobox.get()
        if typed == '':
            data = lista_produtos
        else:
            data = [item for item in lista_produtos if typed.lower() in item.lower()]
        lista_combobox['values'] = data

    label_codigo_desc = tk.Label(nova_janela, text="Código e Descrição do Item:")
    label_codigo_desc.pack(pady=5)

    frame_combobox = tk.Frame(nova_janela)
    frame_combobox.pack(pady=5)
    lista_combobox = ttk.Combobox(frame_combobox, values=lista_produtos, width=80)
    lista_combobox.pack(side=tk.LEFT)
    lista_combobox.bind("<KeyRelease>", atualizar_combobox)
    
    label_info_combobox = tk.Label(frame_combobox, text="Clique no ícone no canto direito do campo para selecionar o item.")
    label_info_combobox.pack(side=tk.LEFT, padx=5)

    label_quantidade = tk.Label(nova_janela, text="QUANTIDADE EM ESTOQUE:", font=("TkDefaultFont", 10, "bold"))
    label_quantidade.pack(pady=5)

    label_quantidade_solicitada = tk.Label(nova_janela, text="Quantidade Solicitada:")
    label_quantidade_solicitada.pack(pady=5)

    entry_quantidade = tk.Entry(nova_janela, textvariable=pR2_Quant, validate="key")
    entry_quantidade['validatecommand'] = (entry_quantidade.register(lambda P: P.isdigit() or P == ""), '%P')
    entry_quantidade.pack(pady=10)

    def atualizar_quantidade(event):
        produto_selecionado = lista_combobox.get()
        codigo_produto, descricao_produto = produto_selecionado.split(" - ", 1)
        quantidade = df.loc[df["cCodigo"] == codigo_produto, "nSaldo"].values[0]
        label_quantidade.config(text=f"QUANTIDADE EM ESTOQUE: {quantidade}", font=("TkDefaultFont", 10, "bold"))
        pR2_Desc.set(descricao_produto)
        pR2_Cod.set(codigo_produto)

    lista_combobox.bind("<<ComboboxSelected>>", atualizar_quantidade)

    label_solicitante = tk.Label(nova_janela, text="Solicitante:")
    label_solicitante.pack(pady=5)
    entry_solicitante = tk.Entry(nova_janela, textvariable=solicitante_var, width=50)
    entry_solicitante.pack(pady=5)

    label_motivo_os = tk.Label(nova_janela, text="Motivo/OS:")
    label_motivo_os.pack(pady=5)
    entry_motivo_os = tk.Entry(nova_janela, textvariable=motivo_os_var, width=50)
    entry_motivo_os.pack(pady=5)

    label_data_entrega = tk.Label(nova_janela, text="Data de Entrega (dd/mm/aaaa):")
    label_data_entrega.pack(pady=5)
    entry_data_entrega = tk.Entry(nova_janela, textvariable=data_entrega, width=20)
    entry_data_entrega.pack(pady=5)

    def enviar_dados():
        descricao = pR2_Desc.get()
        quantidade = pR2_Quant.get()
        codigo_produto = pR2_Cod.get()
        solicitante = solicitante_var.get()
        motivo_os = motivo_os_var.get()
        data_entrega_selecionada = data_entrega.get()
        print(f"Código: {codigo_produto}, Descrição: {descricao}, Quantidade: {quantidade}, Solicitante: {solicitante}, Motivo/OS: {motivo_os}, Data de Entrega: {data_entrega_selecionada}")
        
        enviar_email(codigo_produto, descricao, quantidade, solicitante, motivo_os, data_entrega_selecionada)
        
        # Remover o arquivo Excel após o envio dos dados
        os.remove("Estoque_temp.xlsx")

    botao_enviar = tk.Button(nova_janela, text="Enviar", command=enviar_dados)
    botao_enviar.pack(pady=10)

# Função para enviar o email
def enviar_email(codigo_produto, descricao, quantidade, solicitante, motivo_os, data_entrega):
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = "middleware@opusmedical.com.br; augusto@opusmedical.com.br; almoxarifado@opusmedical.com.br"
    email.Subject = "Requisição Automática do Python"
    email.HTMLBody = f"""
    <p>Este é um teste de envio de email para a automação pyhton da requisição de estoque.</p>
    <p>Código do Produto: {codigo_produto}</p>
    <p>Descrição: {descricao}</p>
    <p>Quantidade: {quantidade}</p>
    <p>Solicitante: {solicitante}</p>
    <p>Motivo/OS: {motivo_os}</p>
    <p>Data de Entrega: {data_entrega}</p>
    """
    email.Send()
    print("Email enviado.")
    # Exibir mensagem de sucesso
    messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
    # Adicionar botão para encerrar a aplicação
    botao_finalizar = tk.Button(root, text="Finalizar", command=root.quit)
    botao_finalizar.pack(pady=20)

root = tk.Tk()
root.title("Consulta de Estoques")
root.geometry("600x300")

progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate')
progress_bar.pack(pady=20)

progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.pack(pady=10)

botao_iniciar = tk.Button(root, text="Iniciar Consulta", command=iniciar_consulta)
botao_iniciar.pack(pady=20)

botao_fazer_requisicao = tk.Button(root, text="Fazer Requisição", state=tk.DISABLED, command=abrir_nova_janela)
botao_fazer_requisicao.pack(pady=20)

root.mainloop()
