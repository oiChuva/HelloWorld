import subprocess
import tkinter as tk

# Função para executar o script EtqNF.py
def executar_script():
    print("phase01")
    subprocess.run(['python', r'C:\\Users\\Isaque\\.vscode\\hostapp\\EtqNF.py'])
    print("phase02")
    subprocess.run(['python', r'C:\\Users\\Isaque\\.vscode\\hostapp\\Gene.py'])

def executar_script2():
    subprocess.run(['python', r'C:\\Users\\Isaque\\.vscode\\hostapp\\EtqAx.py'])

# Função para sair do aplicativo
def sair():
    root.destroy()

# Criar a janela principal
root = tk.Tk()
root.title("Seleção de Ação")

# Configurar o tamanho da janela
root.geometry("300x150")

# Criar o botão para executar o script
btn_executar = tk.Button(root, text="Etiqueta NF", command=executar_script)
btn_executar.pack(pady=10)

btn_executar = tk.Button(root, text="Etiqueta Estoque", command=executar_script2)
btn_executar.pack(pady=10)

# Criar o botão para sair
btn_sair = tk.Button(root, text="Sair", command=sair)
btn_sair.pack(pady=10)

# Iniciar o loop principal da interface
root.mainloop()
