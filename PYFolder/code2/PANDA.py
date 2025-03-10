import os
import pandas as pd

DATA = r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\DATA"
output_file = "merged_data.xlsx"

def merge_files(data_path, output_file):
    all_data = []
    
    # Percorre os arquivos CSV
    for arquivo in os.listdir(data_path):
        if arquivo.endswith(".csv"):
            caminho_arq = os.path.join(data_path, arquivo)
            df = pd.read_csv(caminho_arq, encoding="utf-8", sep=";", low_memory=False)
            
            # Adiciona a coluna 'Origem' com o nome do arquivo, se não existir
            if 'Origem' not in df.columns:
                df.insert(0, 'Origem', arquivo)
            else:
                df['Origem'] = arquivo
            
            all_data.append(df)
    
    if not all_data:
        print("Nenhum arquivo CSV encontrado!")
        return
    
    # Concatenar todos os DataFrames (somente colunas em comum)
    df_merged = pd.concat(all_data, join='inner', ignore_index=True)
    
    # Converter 'Data Cadastro' para datetime
    df_merged['Data Cadastro'] = pd.to_datetime(df_merged['Data Cadastro'], errors='coerce')
    
    # Remover colunas duplicadas com menos informações
    df_merged = df_merged.sort_values(by=['Data Cadastro'], ascending=False)
    df_merged = df_merged.drop_duplicates(subset=['Email'], keep='first')
    
    # Salvar no Excel
    df_merged.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Arquivo {output_file} gerado com sucesso!")

merge_files(DATA, output_file)
