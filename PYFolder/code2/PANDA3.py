import os
import pandas as pd

DATA = r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\DATAXLSX"
output_file = "XLSXmerged.xlsx"

def merge_files(data_path, output_file):
    all_data = []
    
    # Percorre os arquivos XLSX
    for arquivo in os.listdir(data_path):
        if arquivo.endswith(".xlsx"):
            caminho_arq = os.path.join(data_path, arquivo)
            df = pd.read_excel(caminho_arq, engine="openpyxl")
            
            # Adiciona a coluna 'Origem' apenas se ela não existir
            if 'Origem' not in df.columns:
                df.insert(0, 'Origem', arquivo)
            
            all_data.append(df)
    
    if not all_data:
        print("Nenhum arquivo XLSX encontrado!")
        return
    
    # Concatenar todos os DataFrames mantendo todas as colunas
    df_merged = pd.concat(all_data, join='outer', ignore_index=True)
    
    # Converter 'Data Cadastro' para datetime, se existir
    if 'Data Cadastro' in df_merged.columns:
        df_merged['Data Cadastro'] = pd.to_datetime(df_merged['Data Cadastro'], errors='coerce')

    # Remover duplicatas baseadas no 'Email', mantendo a linha com 'Data Cadastro' mais recente
    if 'Email' in df_merged.columns:
        df_merged = df_merged.sort_values(by=['Data Cadastro'], ascending=False, na_position='last')
        df_merged = df_merged.drop_duplicates(subset=['Email'], keep='first')

    # Salvar no Excel
    df_merged.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Arquivo {output_file} gerado com sucesso!")

merge_files(DATA, output_file)
