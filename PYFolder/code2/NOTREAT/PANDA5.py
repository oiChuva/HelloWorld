import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados da planilha
df = pd.read_excel(r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\NOTREAT\CHART.xlsx")

# Limpar valores de hora ou strings inesperadas (se necessário)
df['Datas'] = df['Datas'].astype(str)  # Converte para string
df['Datas'] = df['Datas'].str.split(' ').str[0]  # Remove a parte de hora, se existir

# Garantir que a coluna 'Datas' está no formato datetime
df['Datas'] = pd.to_datetime(df['Datas'], format='%d/%m/%Y', errors='coerce')

# Verificar se há valores inválidos após a conversão
if df['Datas'].isnull().any():
    print("Existem datas inválidas. As linhas com erro foram removidas.")
    df = df.dropna(subset=['Datas'])

# Plotar o gráfico
plt.figure(figsize=(12, 7))  # Aumentar o tamanho do gráfico
plt.plot(df['Datas'], df['Valores'], marker='o', linestyle='-', color='b', label='Quantidade de arquivos')

# Título e rótulos com melhor formatação
plt.title('Quantidade de Arquivos por Data', fontsize=16, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Quantidade de Arquivos', fontsize=12)

# Melhor visualização das datas no eixo X
plt.xticks(rotation=45, ha='right')  # Ajustar a rotação e alinhamento das datas
plt.tight_layout()  # Melhorar o ajuste do layout para não cortar textos

# Melhorar a grade para facilitar a leitura
plt.grid(True, linimport pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados da planilha
df = pd.read_excel(r"C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code2\NOTREAT\CHART.xlsx")

# Limpar valores de hora ou strings inesperadas (se necessário)
df['Datas'] = df['Datas'].astype(str)  # Converte para string
df['Datas'] = df['Datas'].str.split(' ').str[0]  # Remove a parte de hora, se existir

# Garantir que a coluna 'Datas' está no formato datetime
df['Datas'] = pd.to_datetime(df['Datas'], format='%d/%m/%Y', errors='coerce')

# Verificar se há valores inválidos após a conversão
if df['Datas'].isnull().any():
    print("Existem datas inválidas. As linhas com erro foram removidas.")
    df = df.dropna(subset=['Datas'])

# Plotar o gráfico
plt.figure(figsize=(12, 7))  # Aumentar o tamanho do gráfico
plt.plot(df['Datas'], df['Valores'], marker='o', linestyle='-', color='b', label='Quantidade de arquivos')

# Título e rótulos com melhor formatação
plt.title('Quantidade de Arquivos por Data', fontsize=16, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Quantidade de Arquivos', fontsize=12)

# Adicionar os pontos de dados diretamente no gráfico
plt.scatter(df['Datas'], df['Valores'], color='red', zorder=5)  # Adicionar pontos vermelhos

# Melhor visualização das datas no eixo X
plt.xticks(rotation=45, ha='right')  # Ajustar a rotação e alinhamento das datas
plt.tight_layout()  # Melhorar o ajuste do layout para não cortar textos

# Melhorar a grade para facilitar a leitura
plt.grid(True, linestyle='--', alpha=0.6)

# Adicionar legenda
plt.legend(loc='upper left', fontsize=12)

# Exibir o gráfico
plt.show()

plt.legend(loc='upper left', fontsize=12)

# Exibir o gráfico
plt.show()