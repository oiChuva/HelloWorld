import tkinter as tk
import pyperclip

def substituir_palavras(texto):
    substituicoes = {
        'PREFEITURA': 'PREF.',
        'MUNICIPAL': 'MUN.',
        'HOSPITAL': 'HOSP.',
        'HOSPITALAR': 'HOSP.',
        'MEDICAL': 'MED',
        'HOSPITALARES': 'HOSP',
        'SÃO': 'S.',
        'SANTO': 'ST.',
        'REGIONAL': 'REG.',
        'UNIDADE': 'UN.',
        'INDUSTRIA': 'IND',
        'COMERCIO': 'COM',
        'SERVICOS': 'SERV',
        'SERVICO': 'SERV'
    }

    for palavra, substituicao in substituicoes.items():
        texto = texto.replace(palavra, substituicao)
    
    return texto

def limitar_caracteres():
    texto = entrada.get()
    texto_antes.config(text="Texto antes: " + texto)

    # Substituir palavras
    texto = substituir_palavras(texto)

    if len(texto) > 60:
        texto_formatado = texto[:60]
    else:
        texto_formatado = texto
        
    texto_depois.config(text="Texto depois: " + texto_formatado)
    entrada.delete(0, tk.END)
    entrada.insert(0, texto_formatado)

def copiar_texto():
    texto_copiado = entrada.get()
    pyperclip.copy(texto_copiado)

# Configuração da interface
janela = tk.Tk()
janela.title("Limitador de Caracteres e Substituição de Palavras")

# Rótulo
rotulo = tk.Label(janela, text="Digite o texto:")
rotulo.pack(pady=10)

# Entrada de texto
entrada = tk.Entry(janela, width=40)
entrada.pack(pady=10)

# Rótulo para mostrar o texto antes da limitação
texto_antes = tk.Label(janela, text="Texto antes:")
texto_antes.pack()

# Botão para limitar caracteres
botao = tk.Button(janela, text="Limitar Caracteres e Substituir Palavras", command=limitar_caracteres)
botao.pack(pady=10)

# Rótulo para mostrar o texto depois da limitação
texto_depois = tk.Label(janela, text="Texto depois:")
texto_depois.pack()

# Botão para copiar o texto
botao_copiar = tk.Button(janela, text="Copiar Texto", command=copiar_texto)
botao_copiar.pack(pady=10)

# Rodar o loop principal da interface
janela.mainloop()