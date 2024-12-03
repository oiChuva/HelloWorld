import os
import win32com.client as win32

# Função para enviar e-mails
def enviar_email(destinatario, assunto, corpo, anexos=[]):
    # Conectando ao Outlook
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)  # Criando um novo e-mail

    # Definindo os parâmetros do e-mail
    email.To = destinatario
    email.Subject = assunto
    email.BodyFormat = 2  # 2 = HTML
    email.HTMLBody = corpo  # Usando HTML no corpo do e-mail

    # Adicionando anexos
    for anexo in anexos:
        if os.path.exists(anexo):
            email.Attachments.Add(anexo)
        else:
            print(f"Anexo não encontrado: {anexo}")

    # Enviando o e-mail
    email.Send()

# Lista de e-mails e responsáveis
emails_responsaveis = [
    # sua lista de e-mails
]

# Caminho da pasta onde estão as assinaturas e PDF
anexo_dir = r"C:\Users\Isaque\.vscode\PYFOLDER\code\Assinaturas\Imagens"
pdf_padrao = r"C:\Users\Isaque\.vscode\PYFOLDER\code\TutorialAssinatura.pdf"  # Caminho do PDF padrão

# Iterando sobre a lista de e-mails e enviando os e-mails
for pessoa in emails_responsaveis:
    nome = pessoa["nome"]
    email = pessoa["email"]
    cargo = pessoa["cargo"]

    # Definindo o destinatário, assunto e corpo do e-mail
    destinatario = email
    assunto = f"Assinatura de {nome} {cargo}"
    corpo = f"""
    <p>Este é um envio de email para atualização de assinatura.</p>
    <p>Olá {nome},</p>
    <p>Por favor, verifique os documentos anexados e entre em contato se precisar de mais informações.</p>
    """

    # Tentando encontrar o arquivo de assinatura correspondente
    anexo_imagem = os.path.join(anexo_dir, f"{nome}{cargo}.png")  # Substitua pela extensão correta (ex: .png, .jpeg)

    # Lista de anexos (incluindo o PDF padrão)
    anexos = [pdf_padrao]
    if os.path.exists(anexo_imagem):
        anexos.append(anexo_imagem)

    # Enviando o e-mail com os anexos
    enviar_email(destinatario, assunto, corpo, anexos)

