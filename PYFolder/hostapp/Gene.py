import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import win32print
import win32api
import glob
import time

output_dir = r"C:\Users\Isaque\.vscode\hostapp\etiquetas"
os.makedirs(output_dir, exist_ok=True)

def gerar_etiqueta(nota_fiscal, remetente, destinatario, cnpj_dest, endereco_dest, descricao_prod, codigo_prod, quantidade, volume, output_dir):
    print(f"Gerando etiqueta para Nota Fiscal {nota_fiscal} e Código {codigo_prod}")
    # Configurações da etiqueta
    width, height = 400, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    logo = Image.open(r'c:\Users\Isaque\.vscode\hostapp\logo.png')
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

    def draw_label_and_text(draw, label, content, font, y, image_width, box_height=40, x=10, box_width=380):
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
    y = draw_label_and_text(draw, "NOTA FISCAL Nº:", nota_fiscal, font_bold, y, width, box_height=40)
    y = draw_label_and_text(draw, "VOLUMES:", str(volume), font_bold, y, width // 2 - 20, box_width=width // 2 - 20)
    y = draw_label_and_text(draw, "QUANTIDADE:", str(quantidade), font_bold, y - 40, width // 2, box_width=width // 2 - 20)
    
    y = draw_text_box(draw, remetente, font_bold, y, width, box_height=60)
    
    cliente_text = f"CLIENTE/FORNECEDOR:\n{destinatario}\nCNPJ: {cnpj_dest}"
    cliente_linhas = wrap_text(cliente_text, font_medium, width - 40)
    cliente_texto = "\n".join(cliente_linhas)
    y = draw_text_box(draw, cliente_texto, font_medium, y, width, box_height=100)

    endereco_linhas = wrap_text(endereco_dest, font_medium, width - 40)
    endereco_texto = "\n".join(endereco_linhas)
    y = draw_text_box(draw, endereco_texto, font_medium, y, width, box_height=80)

    descricao = f"DESCRIÇÃO:\n{descricao_prod}"
    descricao_linhas = wrap_text(descricao, font_description, width - 40)
    descricao_texto = "\n".join(descricao_linhas)
    y = draw_text_box(draw, descricao_texto, font_description, y, width, box_height=60)

    # Desenha o código do produto logo abaixo da descrição
    y = draw_resized_code(draw, "CÓDIGO:", codigo_prod, font_code, y, width, box_height=40)

    # Salvando a imagem
    image_path = os.path.join(output_dir, f"etiqueta_{nota_fiscal}_{codigo_prod}.png")
    image.save(image_path)
    print(f"Etiqueta salva em: {image_path}")
    
    return image_path

def process_excel_file(file_path, output_dir):
    print(f"Processando arquivo Excel: {file_path}")
    # Carregar o arquivo Excel
    df = pd.read_excel(file_path)

    # Loop para gerar etiquetas para cada linha
    etiquetas = []
    for index, row in df.iterrows():
        print(f"Gerando etiqueta para a linha {index + 1}")
        etiqueta_path = gerar_etiqueta(
            str(row['Nota Fiscal']),
            str(row['Remetente']),
            str(row['Destinatário']),
            str(row['CNPJ/CPF Destinatário']),
            str(row['Endereço Destinatário']),
            str(row['Descrição Produto']),
            str(row['Código Produto']),
            str(row['Quantidade']),
            str(row['Volume']),
            output_dir  # Passa o diretório de saída para salvar a etiqueta
        )
        etiquetas.append(etiqueta_path)
    
    return etiquetas

# Caminho do diretório onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definir o diretório de saída para salvar as etiquetas
output_dir = os.path.join(script_dir, "etiquetas")
os.makedirs(output_dir, exist_ok=True)
print(f"Diretório de saída criado: {output_dir}")

# Listar todos os arquivos na pasta do script
files = os.listdir(script_dir)
print(f"Arquivos encontrados: {files}")

# Processar e excluir arquivos Excel
etiquetas_geradas = []
for file_name in files:
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        file_path = os.path.join(script_dir, file_name)
        
        # Processar o arquivo Excel
        etiquetas_geradas += process_excel_file(file_path, output_dir)
        
        # Excluir o arquivo Excel
        os.remove(file_path)
        print(f'Arquivo {file_name} excluído com sucesso.')

print(f"Etiquetas geradas: {etiquetas_geradas}")

# Listar arquivos na pasta de etiquetas
print(f"Arquivos na pasta de etiquetas:")
for file_name in os.listdir(output_dir):
    print(file_name)

def excluir_arquivos_pasta(diretorio):
    arquivos = glob.glob(os.path.join(diretorio, "*"))
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f"Arquivo {arquivo} excluído com sucesso.")

# Definir a impressora e imprimir as etiquetas
lista_impressoras = win32print.EnumPrinters(2)
impressora = lista_impressoras[2]
print(impressora)
win32print.SetDefaultPrinter(impressora[2])

# Imprimir todas as etiquetas geradas
for etiqueta_path in etiquetas_geradas:
    win32api.ShellExecute(0, "print", etiqueta_path, None, output_dir, 0)
    time.sleep(5)
excluir_arquivos_pasta(output_dir)
print(f"Todos os arquivos na pasta {output_dir} foram excluídos.")