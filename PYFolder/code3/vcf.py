import pandas as pd

# Caminho do seu arquivo VCF
vcf_path = r~2'C:\Users\Isaque\.vscode\GitHub\HelloWorld\PYFolder\code3\vcards_20250425_115048.vcf'

# Lista para armazenar os contatos
contatos = []

# Lendo o arquivo VCF
with open(vcf_path, 'r', encoding='utf-8') as file:
    contato = {}
    for linha in file:
        linha = linha.strip()
        if linha.startswith('FN:'):
            contato['Nome'] = linha[3:]
        elif linha.startswith('TEL'):
            contato['Telefone'] = linha.split(':')[1]
        elif linha.startswith('EMAIL'):
            contato['Email'] = linha.split(':')[1]
        elif linha.startswith('END'):
            contato['Endereço'] = linha.split(':')[1]
        elif linha == 'END:VCARD':
            contatos.append(contato)
            contato = {}

# Transformar em DataFrame
df = pd.DataFrame(contatos)

# Salvar como Excel
df.to_excel('contatos.xlsx', index=False)

print("Arquivo 'contatos.xlsx' gerado com sucesso!")
