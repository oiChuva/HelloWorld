import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests

# Funções de consulta (conforme descrito anteriormente)
def consultar_prod(codigo):
    url_consprod = "https://app.omie.com.br/api/v1/geral/produtos/"
    payload = {
        "call": "ConsultarProduto",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "codigo": codigo
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url_consprod, headers=headers, json=payload)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erro ao consultar produto. Código de status: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def extrair_informacoes(data):
    codigo_produto = data.get("codigo_produto")
    codigo = data.get("codigo")
    descricao = data.get("descricao")
    descricao_familia = data.get("descricao_familia")

    return codigo_produto, codigo, descricao, descricao_familia

def consultar_posicao_estoque(codigo_produto, data, codigo_local_estoque):
    url_estoque = "https://app.omie.com.br/api/v1/estoque/consulta/"
    payload = {
        "call": "PosicaoEstoque",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "codigo_local_estoque": codigo_local_estoque,
                "id_prod": codigo_produto,
                "data": data
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url_estoque, headers=headers, json=payload)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erro ao consultar posição de estoque. Código de status: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def ajustar_texto(texto, fonte, largura_max):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste_linha = f"{linha_atual} {palavra}".strip()
        largura_texto = fonte.getbbox(teste_linha)[2]
        if largura_texto <= largura_max:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return "\n".join(linhas)

def gerar_etiqueta(codigo, descricao, quantidade):
    largura = 400
    altura = 250
    img = Image.new('RGB', (largura, altura), color='white')
    d = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("arial.ttf", 20)
        fonte_bold = ImageFont.truetype("arialbd.ttf", 26)
    except IOError:
        fonte = ImageFont.load_default()
        fonte_bold = ImageFont.load_default()

    d.text((10, 10), f"CÓDIGO: {codigo}", font=fonte_bold, fill=(0, 0, 0))
    d.text((10, 50), f"DESCRIÇÃO:", font=fonte_bold, fill=(0, 0, 0))

    descricao_ajustada = ajustar_texto(descricao, fonte, largura - 30)
    d.text((10, 80), descricao_ajustada, font=fonte, fill=(0, 0, 0))
    
    d.text((10, 170), f"QUANTIDADE: {quantidade} APROVADO", font=fonte_bold, fill=(0, 0, 0))

    tamanho_quadrado = 30
    espacamento = 5
    inicio_x = 10
    inicio_y = 200
    for i in range(10):
        d.rectangle(
            [inicio_x + i * (tamanho_quadrado + espacamento), inicio_y,
             inicio_x + i * (tamanho_quadrado + espacamento) + tamanho_quadrado, inicio_y + tamanho_quadrado],
            outline="black"
        )

    img.save(f'etiqueta_{codigo}.png')

estoques = {
    7257847287: "ALMOXARIFADO_OPUS",
    7279534259: "OPUS_VENDAS",
    7281748243: "OPUS_LOCACAO",
    7281751216: "INSTRUMENTO_DE_MEDICAO",
    7284481758: "LIMPEZA",
    7284957048: "TECNICA",
    7292328980: "ESTOQUE_VM"
}
def criar_tela():
    root = tk.Tk()
    root.title("Consulta e Geração de Etiqueta")
    root.geometry("400x250")

    # Campo de entrada para o código do produto
    lbl_codigo = tk.Label(root, text="Código do Produto:")
    lbl_codigo.pack(pady=10)
    entrada_codigo = tk.Entry(root, width=20)
    entrada_codigo.pack()

    progresso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progresso.pack(pady=20)

    # Função para executar consulta e geração de etiqueta
    def executar():
        codigo_prod = entrada_codigo.get()  # Obtém o código do produto da entrada do usuário
        resultado_prod = consultar_prod(codigo_prod)
        
        if resultado_prod:
            codigo_produto, codigo, descricao, descricao_familia = extrair_informacoes(resultado_prod)
            data_atual = datetime.now().strftime("%d/%m/%Y")
            quantidade = 0
            total_estoques = len(estoques)
            passo_progresso = 100 / total_estoques
            progresso_atual = 0

            for i, (codigo_local_estoque, nome_estoque) in enumerate(estoques.items(), start=1):
                resultado_estoque = consultar_posicao_estoque(codigo_produto, data_atual, codigo_local_estoque)
                if resultado_estoque:
                    saldo = resultado_estoque.get("saldo", 0)
                    if saldo > 0:
                        quantidade = saldo
                        gerar_etiqueta(codigo, descricao, quantidade)

                progresso_atual += passo_progresso
                progresso['value'] = progresso_atual
                root.update_idletasks()  # Atualiza a interface gráfica

            if quantidade == 0:
                print("Nenhum saldo disponível nos estoques.")

        else:
            print(f"Falha ao consultar o produto {codigo_prod}.")
        
        root.destroy()  # Fecha a janela ao finalizar

    btn_executar = tk.Button(root, text="Executar", command=executar)
    btn_executar.pack(pady=10)

    root.mainloop()

# Chamada para criar a tela
criar_tela()