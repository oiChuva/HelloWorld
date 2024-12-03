import threading
import requests
import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageDraw, ImageFont
import win32print
import win32api
import os
import shutil
import time

def requisicao_consulta_nf(nCodNF, nNF):
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
        
        nf_dest = resposta_json.get("nfDestInt", {})
        razao_social_dest = nf_dest.get("cRazao", "")
        cnpj_cpf_dest = nf_dest.get("cnpj_cpf", "")
        nCodCli = nf_dest.get("nCodCli", "")

        ide = resposta_json.get("ide", {})
        numero_nf_dest = ide.get("nNF", "")
        tp_nf = ide.get("tpNF", "")

        detalhes_produtos = []
        detalhes = resposta_json.get("det", [])
        for detalhe in detalhes:
            prod = detalhe.get("prod", {})
            cProd = prod.get("cProd", "")
            xProd = prod.get("xProd", "")
            vProd = prod.get("vProd", "")
            qCom = prod.get("qCom", "")
            detalhes_produtos.append({"cProd": cProd, "xProd": xProd, "vProd": vProd, "qCom": qCom})

        nf_emit_int = resposta_json.get("nfEmitInt", {})
        nCodEmp = nf_emit_int.get("nCodEmp", "")

        return razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)
        return None, None, None, None, None, None, None

def requisicao_consultar_empresa(nCodEmp):
    url = "https://app.omie.com.br/api/v1/geral/empresas/"
    dados = {
        "call": "ConsultarEmpresa",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "codigo_empresa": nCodEmp
            }
        ]
    }
    response = requests.post(url, json=dados)

    if response.status_code == 200:
        dados_empresa = response.json()
        return {
            'razao_social': dados_empresa.get('razao_social', ''),
            'telefone1_ddd': dados_empresa.get('telefone1_ddd', ''),
            'telefone1_numero': dados_empresa.get('telefone1_numero', '')
        }
    else:
        print("Erro na requisição:", response.status_code)
        return None

def requisicao_consulta_endereco_dest(nCodCli):
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
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(dados), headers=headers)

    if response.status_code == 200:
        resposta_json = response.json()
        endereco = resposta_json.get('endereco', '')
        endereco_numero = resposta_json.get('endereco_numero', '')
        bairro = resposta_json.get('bairro', '')
        cidade = resposta_json.get('cidade', '')
        estado = resposta_json.get('estado', '')
        complemento = resposta_json.get('complemento', '')
        cep = resposta_json.get('cep', '')
        endereco_completo = f"{endereco}, {endereco_numero}, {bairro}, {cidade}, {estado}, {complemento}, {cep}"
        return endereco_completo
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)
        return None

def consultar_nf():
    nNF = entry_nf.get()
    quantidade = entry_quantidade.get()
    volume = entry_volume.get()
    resultado_nf = requisicao_consulta_nf("0", nNF)
    if resultado_nf:
        razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli = resultado_nf
        info_nf_label.config(text=f"Razão Social (dest): {razao_social_dest}\nCNPJ/CPF (dest): {cnpj_cpf_dest}\nNúmero NF (dest): {numero_nf_dest}\nTipo NF: {tp_nf}\n")
        
        produtos_info = ""
        for idx, detalhe in enumerate(detalhes_produtos, start=1):
            produtos_info += f"Produto {idx}:\nCódigo do Produto: {detalhe['cProd']}\nDescrição: {detalhe['xProd']}\nValor do Produto: {detalhe['vProd']}\nQuantidade: {detalhe['qCom']}\n\n"
        
        produtos_nf_label.config(text=produtos_info)

        threading.Thread(target=consultar_empresa_endereco, args=(nCodEmp, nCodCli, resultado_nf, quantidade, volume)).start()

def consultar_empresa_endereco(nCodEmp, nCodCli, resultado_nf, quantidade, volume):
    dados_empresa = requisicao_consultar_empresa(nCodEmp)
    if dados_empresa:
        empresa_info_label.config(text=f"Razão Social: {dados_empresa['razao_social']}\nTelefone: ({dados_empresa['telefone1_ddd']}) {dados_empresa['telefone1_numero']}")
        
        endereco_dest = requisicao_consulta_endereco_dest(nCodCli)
        if endereco_dest:
            for detalhe in resultado_nf[4]:
                # Start the thread with the correct syntax
                threading.Thread(target=gerar_etiqueta, args=(resultado_nf, dados_empresa, endereco_dest, detalhe, quantidade, volume)).start()

from PIL import Image, ImageDraw, ImageFont

def gerar_etiqueta(dados_nf, dados_empresa, endereco_dest, detalhe_produto, quantidade, volume):
    # Configurações da etiqueta
    width, height = 200, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    logo = Image.open('logo.png')  # Atualize o caminho do logo
    logo_width, logo_height = 120, 55
    logo = logo.resize((logo_width, logo_height))

    try:
        font_large = ImageFont.truetype("arialbd.ttf", 18)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_description = ImageFont.truetype("arialbd.ttf", 22)
        font_code = ImageFont.truetype("arialbd.ttf", 22)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_description = ImageFont.load_default()
        font_code = ImageFont.load_default()

    def draw_centered_text(draw, text, font, y, image_width, box_height=None):
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        x = (image_width - text_width) / 2
        if box_height is None:
            box_height = text_height + 5  # Reduzir a margem vertical
        y_text = y + (box_height - text_height) / 2
        draw.text((x, y_text), text, fill="black", font=font)
        return y + box_height

    def draw_text_box(draw, text, font, y, image_width, box_height=40):
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        box_height = max(box_height, text_height + 10)  # Reduzir a margem superior e inferior
        draw.rectangle([(10, y), (image_width - 10, y + box_height)], outline="black", width=2)
        y = draw_centered_text(draw, text, font, y, image_width, box_height)
        return y

    def draw_label_and_text(draw, label, content, font, y, x, box_width, box_height=40):
        label_width, label_height = draw.textbbox((0, 0), label, font=font)[2:]
        content_width, content_height = draw.textbbox((0, 0), content, font=font)[2:]
        box_height = max(box_height, max(label_height, content_height) + 10)  # Reduzir a margem superior e inferior
        draw.rectangle([(x, y), (x + box_width, y + box_height)], outline="black", width=2)
        label_x = x + 10
        content_x = label_x + label_width + 10
        label_y = y + (box_height - label_height) / 2
        content_y = y + (box_height - content_height) / 2
        draw.text((label_x, label_y), label, fill="black", font=font)
        draw.text((content_x, content_y), content, fill="black", font=font)
        return y + box_height

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    def draw_resized_code(draw, label, content, font, y, image_width, box_height=40, max_font_size=22, min_font_size=10):
        current_font_size = max_font_size
        content_font = ImageFont.truetype("arialbd.ttf", current_font_size)
        
        # Ajusta o tamanho da fonte até caber na largura da imagem
        while draw.textbbox((0, 0), content, font=content_font)[2] > image_width - 40 and current_font_size > min_font_size:
            current_font_size -= 1
            content_font = ImageFont.truetype("arialbd.ttf", current_font_size)

        # Calcule a altura da caixa para o texto
        text_width, text_height = draw.textbbox((0, 0), content, font=content_font)[2:]

        # Certifique-se de que a caixa tenha altura adequada
        box_height = max(box_height, text_height + 10)  # Adiciona margem superior e inferior

        # Desenha a caixa ao redor do código
        draw.rectangle([(10, y), (image_width - 10, y + box_height)], outline="black", width=2)
        
        # Desenha o label e o conteúdo do código
        label_x = 20
        content_x = label_x + draw.textbbox((0, 0), label, font=font)[2] + 10
        label_y = y + (box_height - draw.textbbox((0, 0), label, font=font)[3]) / 2
        content_y = y + (box_height - text_height) / 2
        
        draw.text((label_x, label_y), label, fill="black", font=font)
        draw.text((content_x, content_y), content, fill="black", font=content_font)
        
        return y + box_height

    y = 10
    title_text = "CONFERÊNCIA\nEXPEDIÇÃO"
    title_width, title_height = draw.textbbox((0, 0), title_text, font=font_large)[2:]
    title_x = 20
    logo_x = width - logo_width - 20
    title_box_height = max(title_height, logo_height) + 30
    draw.rectangle([(10, y), (width - 10, y + title_box_height)], outline="black", width=2)
    draw.text((title_x, y + (title_box_height - title_height) // 2), title_text, fill="black", font=font_large)
    image.paste(logo, (logo_x, int(y + (title_box_height - logo_height) / 2)))
    y += title_box_height

    # Dados da NF
    razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli = dados_nf
    y = draw_label_and_text(draw, "NOTA FISCAL Nº:", numero_nf_dest, font_bold, y, 10, width-20, box_height=40)

    box_width = (width - 30) / 2  # largura das caixas para volume e quantidade

    y = draw_label_and_text(draw, "VOLUMES:", volume, font_bold, y, 10, box_width, box_height=40)
    y = draw_label_and_text(draw, "QUANTIDADE:", quantidade, font_bold, y - 40, box_width + 20, box_width, box_height=40)

    y += 10  # Adicionar espaço entre as seções
    y = draw_text_box(draw, f"{dados_empresa['razao_social']}\nCNPJ: 14.368.486/0001-20", font_bold, y, width, box_height=60)
    
    cliente_text = f"CLIENTE/FORNECEDOR:\n{razao_social_dest}\nCNPJ: {cnpj_cpf_dest}"
    cliente_linhas = wrap_text(cliente_text, font_medium, width - 40)
    cliente_texto = "\n".join(cliente_linhas)
    y = draw_text_box(draw, cliente_texto, font_medium, y, width, box_height=100)

    endereco_linhas = wrap_text(endereco_dest, font_medium, width - 40)
    endereco_texto = "\n".join(endereco_linhas)
    y = draw_text_box(draw, endereco_texto, font_medium, y, width, box_height=80)

    # Incrementa o valor de y para garantir que o código do produto fique abaixo da quantidade
    y += 10  # Adiciona espaço entre a quantidade e o código do produto

    # Descrição e código do produto
    descricao = f"DESCRIÇÃO:\n{detalhe_produto['xProd']}"
    codigo = detalhe_produto['cProd']
    descricao_linhas = wrap_text(descricao, font_description, width - 40)
    descricao_texto = "\n".join(descricao_linhas)
    y = draw_text_box(draw, descricao_texto, font_description, y, width, box_height=60)

    # Adiciona uma linha para imprimir o código para debug
    print(f"Código do produto: {codigo}")

    # Desenha o código do produto logo abaixo da descrição
    y = draw_resized_code(draw, "CÓDIGO:", codigo, font_code, y, width, box_height=40)

    # Diretório onde você quer salvar as etiquetas
    output_dir = r"C:\Users\Isaque\.vscode\fotos"

    # Verifica se o diretório existe, se não existir, cria
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Caminho completo do arquivo
    output_path = os.path.join(output_dir, f"etiqueta_{numero_nf_dest}.pdf")
    
    # Salvar a imagem
    image.save(output_path, "PDF")
    image.show()

    lista_impressoras = win32print.EnumPrinters(2)
    print("Lista de impressoras:", lista_impressoras)

    # Seleciona a primeira impressora da lista
    impressora = lista_impressoras[2]
    print("Impressora selecionada:", impressora[2])

    # Define a impressora padrão
    win32print.SetDefaultPrinter(impressora[2])

    # Caminho para a pasta contendo as fotos
    caminho = r"C:\Users\Isaque\.vscode\fotos"
    lista_arquivos = os.listdir(caminho)

    # Imprime cada arquivo na pasta
    for arquivo in lista_arquivos:
        caminho_completo = os.path.join(caminho, arquivo)
        print("Imprimindo arquivo:", caminho_completo)
        win32api.ShellExecute(0, "print", caminho_completo, None, caminho, 0)
    time.sleep(120)
    transfer() # type: ignore

root = tk.Tk()
root.title("Consulta de Nota Fiscal")

label_nf = tk.Label(root, text="Número da Nota Fiscal:")
label_nf.grid(row=0, column=0, padx=10, pady=10)

entry_nf = tk.Entry(root)
entry_nf.grid(row=0, column=1, padx=10, pady=10)

label_quantidade = tk.Label(root, text="Quantidade:")
label_quantidade.grid(row=1, column=0, padx=10, pady=10)

entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=1, column=1, padx=10, pady=10)

label_volume = tk.Label(root, text="Volume:")
label_volume.grid(row=2, column=0, padx=10, pady=10)

entry_volume = tk.Entry(root)
entry_volume.grid(row=2, column=1, padx=10, pady=10)

consultar_button = tk.Button(root, text="Consultar NF", command=consultar_nf)
consultar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

info_nf_label = tk.Label(root, text="")
info_nf_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

produtos_nf_label = tk.Label(root, text="")
produtos_nf_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

empresa_info_label = tk.Label(root, text="")
empresa_info_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

endereco_dest_label = tk.Label(root, text="")
endereco_dest_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

sair_button = tk.Button(root, text="Sair", command=root.quit)
sair_button.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()