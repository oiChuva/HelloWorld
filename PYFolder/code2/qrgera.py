import qrcode
from tkinter import *
from tkinter import messagebox
import re

def sanitize_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def gerar_qrcodes():
    links = entry_links.get("1.0", END).strip().split('\n')
    if not links or links == ['']:
        messagebox.showwarning("Aviso", "Digite ao menos um link.")
        return
    
    for index, link in enumerate(links):
        if link.strip():
            sanitized_link = sanitize_filename(link.strip())
            image = qrcode.make(link.strip())
            image.save(f'imagem_{sanitized_link}_{index + 1}.png')
    
    messagebox.showinfo("Sucesso", "Os QR Codes foram gerados e salvos com sucesso!")

# Criando a interface gráfica
root = Tk()
root.title("Gerador de QR Code")

# Rótulo e caixa de texto para inserir os links
label_instruction = Label(root, text="Digite os links que deseja transformar em QR Code (um por linha):")
label_instruction.pack(pady=5)

entry_links = Text(root, height=10, width=50)
entry_links.pack(pady=5)

# Botão para gerar os QR Codes
button_generate = Button(root, text="Gerar QR Codes", command=gerar_qrcodes)
button_generate.pack(pady=10)

# Executando a aplicação
root.mainloop()