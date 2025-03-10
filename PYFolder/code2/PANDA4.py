import os
import pandas as pd

# Diretórios de origem e destino
pasta_origem = r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\TREAT"
pasta_destino = r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\TREATNONAME"
arquivo_nome = "XLSXTREAT.xlsx"

# Caminho completo do arquivo
caminho_origem = os.path.join(pasta_origem, arquivo_nome)
caminho_destino = os.path.join(pasta_destino, arquivo_nome)

# Verifica se o arquivo existe
if os.path.exists(caminho_origem):
    # Carregar o arquivo
    df = pd.read_excel(caminho_origem, engine="openpyxl")

    # Remover linhas onde a coluna 'Nome' está vazia
    df = df.dropna(subset=['Nome'])
    # Remove coluna vazia
    df = df.dropna(axis=1, how='all')
    df = df.drop_duplicates(subset=['Email'], keep='first')

    # Salvar o arquivo na pasta de destino
    df.to_excel(caminho_destino, index=False, engine="openpyxl")

    print(f"Arquivo processado e salvo em: {caminho_destino}")
else:
    print(f"Arquivo {arquivo_nome} não encontrado em {pasta_origem}")
