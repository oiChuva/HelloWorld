import requests
import json
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def consultar_produto(app_key, app_secret, codigo=""):
    url = "https://app.omie.com.br/api/v1/geral/produtos/"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "call": "ConsultarProduto",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "codigo": codigo
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def consultar_posicao_estoque(app_key, app_secret, id_prod=0, data="", cdLocal_Est=""):
    url = "https://app.omie.com.br/api/v1/estoque/consulta/"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "call": "PosicaoEstoque",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "codigo_local_estoque": cdLocal_Est,
            "id_prod": id_prod,
            "data": data,
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        resposta_json = response.json()
        saldo = resposta_json.get('saldo', 0)
        return saldo
    else:
        response.raise_for_status()

def main(codigo):
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"

    try:
        resultado = consultar_produto(app_key, app_secret, codigo=codigo)

        # Extrair os campos específicos
        descricao_familia = resultado.get("descricao_familia", "")
        codigo_produto = resultado.get("codigo", "")
        descricao_produto = resultado.get("descricao", "")
        ncm = resultado.get("ncm", "")
        localizacao = ""

        # Procurar pela característica "LOCALIZACAO"
        caracteristicas = resultado.get("caracteristicas", [])
        for caracteristica in caracteristicas:
            if caracteristica.get("cNomeCaract") == "LOCALIZACAO":
                localizacao = caracteristica.get("cConteudo", "")

        # Extrai o valor de "codigo_produto" do JSON
        iD_produto = resultado.get("codigo_produto")

        if iD_produto is not None:
            data_atual = datetime.now().strftime("%d/%m/%Y")
            cdLocal_Est_list = [7257847287, 7279534259, 7281748243, 7281751216, 7284481758, 7284957048, 7292328980]
            
            rows = []

            # Configurar a barra de progresso
            progress_bar["maximum"] = len(cdLocal_Est_list)

            for idx, cdLocal_Est in enumerate(cdLocal_Est_list):
                try:
                    saldo = consultar_posicao_estoque(app_key, app_secret, iD_produto, data_atual, cdLocal_Est)
                    if saldo > 0:
                        nome_estoque = {
                            7257847287: "ALMOXARIFADO OPUS",
                            7279534259: "OPUS VENDAS",
                            7281748243: "OPUS LOCAÇÃO",
                            7281751216: "INSTRUMENTO DE MEDIÇÃO",
                            7284481758: "LIMPEZA",
                            7284957048: "TECNICA",
                            7292328980: "ESTOQUE VM"
                        }.get(cdLocal_Est, "ESTOQUE DESCONHECIDO")

                        rows.append({
                            "descricao_familia": descricao_familia,
                            "codigo": codigo_produto,
                            "descricao": descricao_produto,
                            "ncm": ncm,
                            "localizacao": localizacao,
                            "id_produto": iD_produto,
                            "nome_estoque": nome_estoque,
                            "saldo": saldo,
                            "data_consulta": data_atual
                        })

                except requests.exceptions.HTTPError as err:
                    print(f"Erro HTTP ocorreu com código local de estoque {cdLocal_Est}: {err}")
                except Exception as err:
                    print(f"Outro erro ocorreu com código local de estoque {cdLocal_Est}: {err}")

                # Atualizar a barra de progresso
                progress_bar["value"] = idx + 1
                root.update_idletasks()

            if rows:
                # Criar DataFrame e salvar em planilha
                df = pd.DataFrame(rows)
                df.to_excel("resultado_produtos_" + codigo_produto + ".xlsx", index=False)
                messagebox.showinfo("Sucesso", "Planilha gerada com sucesso.")
            else:
                messagebox.showinfo("Info", "Nenhum saldo encontrado maior que zero.")
        else:
            messagebox.showwarning("Aviso", "Não foi possível encontrar 'codigo_produto' no resultado.")

    except requests.exceptions.HTTPError as err:
        messagebox.showerror("Erro HTTP", f"Erro HTTP ocorreu: {err}")
    except Exception as err:
        messagebox.showerror("Erro", f"Outro erro ocorreu: {err}")

def on_submit():
    codigo = entry_codigo.get()
    progress_bar["value"] = 0  # Resetar a barra de progresso
    main(codigo)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Consulta de Produto")

tk.Label(root, text="Digite o código do produto:").grid(row=0, column=0, padx=10, pady=10)
entry_codigo = tk.Entry(root)
entry_codigo.grid(row=0, column=1, padx=10, pady=10)

btn_submit = tk.Button(root, text="Consultar", command=on_submit)
btn_submit.grid(row=1, column=0, columnspan=2, pady=10)

# Adicionar a barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

