import qrcode
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def gerar_qrcodes():
    links = entry_links.get("1.0", END).strip().split('\n')
    if not links or links == ['']:
        messagebox.showwarning("Aviso", "Digite ao menos um link.")
        return

    # Limpar a área onde os QR Codes serão exibidos
    for widget in qr_frame.winfo_children():
        widget.destroy()

    for index, link in enumerate(links):
        if link.strip():
            sanitized_link = sanitize_filename(link.strip())
            image = qrcode.make(link.strip())
            filepath = f'imagem_{sanitized_link}_{index + 1}.png'
            image.save(filepath)

            # Carregar e exibir o QR Code na interface
            img = Image.open(filepath)
            img = img.resize((150, 150))  # Redimensionar para caber na interface
            img = ImageTk.PhotoImage(img)

            qr_label = Label(qr_frame, image=img, bg="#ffffff")
            qr_label.image = img
            qr_label.grid(row=index // 3, column=index % 3, padx=10, pady=10)

    messagebox.showinfo("Sucesso", "Os QR Codes foram gerados e exibidos com sucesso!")

# Criando a interface gráfica
root = Tk()
root.title("Gerador de QR Code")

# Estilo da interface
root.configure(bg="#f0f0f0")  # Cor de fundo
root.geometry("700x600")  # Dimensões da janela

# Rótulo e caixa de texto para inserir os links
label_instruction = ttk.Label(root, text="Digite os links que deseja transformar em QR Code (um por linha):", background="#f0f0f0", font=("Arial", 12))
label_instruction.pack(pady=10)

entry_links = Text(root, height=8, width=60, font=("Arial", 10), wrap=WORD, relief=SOLID, borderwidth=1)
entry_links.pack(pady=10)

# Botão para gerar os QR Codes
button_generate = ttk.Button(root, text="Gerar QR Codes", command=gerar_qrcodes)
button_generate.pack(pady=10)

# Frame para exibir os QR Codes
qr_frame = Frame(root, bg="#ffffff", relief=SOLID, borderwidth=1)
qr_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Executando a aplicação
root.mainloop()