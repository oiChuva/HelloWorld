import tkinter as tk
from tkinter import messagebox
import win32api
import os

# Caminho para a pasta contendo os executáveis
caminho = r"C:\Users\Isaque\.vscode\code\dist"

# Caminhos completos para os executáveis
exe_path_1 = os.path.join(caminho, "cadOmieW.exe")
exe_path_2 = os.path.join(caminho, "RequisiçãoEstoqueV1.3.exe")

# Funções para executar os aplicativos
def Executar_app1():
    win32api.ShellExecute(0, "open", exe_path_1, None, None, 10)

def Executar_app2():
    win32api.ShellExecute(0, "open", exe_path_2, None, None, 10)

# Função para ser chamada ao pressionar o botão "Ir"
def executar():
    valor = opcao.get()
    if valor == 1:
        Executar_app1()
    elif valor == 2:
        Executar_app2()
    else:
        messagebox.showerror("Erro", "Selecione uma opção válida")

# Configurando a interface Tkinter
root = tk.Tk()
root.title("Escolha de Aplicativo")
root.geometry("500x100")  # Tamanho da tela

# Configurar a cor de fundo usando código hexadecimal
root.configure(bg='#BD7ED9')  # Exemplo de azul claro

# Variável para armazenar a opção selecionada
opcao = tk.IntVar()

# Frame para organizar os botões
frame = tk.Frame(root, bg='#BD7ED9')  # Usando o mesmo código hexadecimal
frame.pack(pady=20)

# Criação dos botões de rádio com cor de fundo e texto personalizados
radio1 = tk.Radiobutton(frame, text="Cadastro", variable=opcao, value=1, bg='#BD7ED9', fg='#000000', selectcolor='#E9A7F2')
radio1.pack(side=tk.LEFT, padx=10)

radio2 = tk.Radiobutton(frame, text="Estoque", variable=opcao, value=2, bg='#BD7ED9', fg='#000000', selectcolor='#E9A7F2')
radio2.pack(side=tk.LEFT, padx=10)

# Criação do botão "Ir" com cor personalizada
botao_ir = tk.Button(frame, text="Ir", command=executar, width=5, height=1, bg='#854AD9', fg='#E9A7F2')  # Botão azul
botao_ir.pack(side=tk.LEFT, padx=10)

# Iniciar o loop da interface
root.mainloop()
