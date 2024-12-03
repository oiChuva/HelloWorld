import tkinter as tk
import ttkbootstrap as ttk

# Configuração da interface principal
style = ttk.Style(theme="darkly")
root = style.master
root.title("Exemplo de Botão com Bordas")
root.geometry("300x200")

# Configurar um novo estilo para os botões
style.configure("Custom.TButton", borderwidth=25, relief="solid", padding=10)

# Criar botões com o estilo personalizado
botao1 = ttk.Button(root, text="Botão 1", style="Custom.TButton")
botao1.pack(pady=10)

botao2 = ttk.Button(root, text="Botão 2", style="Custom.TButton")
botao2.pack(pady=10)

root.mainloop()
