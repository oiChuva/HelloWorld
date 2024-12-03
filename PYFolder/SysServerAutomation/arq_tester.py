from datetime import datetime
from arq_lerEstoque import lerEstoque
import json
import pandas as pd

def webhook_end_l():
    # Data de posição definida internamente
    data_posicao = datetime.now().strftime("%d/%m/%Y")

    # Chamar a função lerEstoque
    estoque_json = lerEstoque(data_posicao)

    # Convertendo os dados para JSON
    print(json.dumps(estoque_json, indent=4, ensure_ascii=False))

    # Supondo que estoque_json seja uma lista de dicionários (como esperado para um DataFrame)
    if isinstance(estoque_json, list):
        # Criar DataFrame a partir dos dados
        df = pd.DataFrame(estoque_json)
        
        # Definir o nome da planilha com base na data
        nome_arquivo = f"estoque_{data_posicao.replace('/', '')}.xlsx"
        
        # Salvar os dados na planilha
        df.to_excel(nome_arquivo, index=False)

        print(f"Planilha salva como {nome_arquivo}")
    else:
        print("Formato de dados inesperado")

webhook_end_l()
