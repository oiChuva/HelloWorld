import win32com.client as win32
import pythoncom

def enviar_email(numero_serie, codOMIE):
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    # Anexar a imagem
    image_path = "Logo Isaque-05.png"  # Insira o caminho da sua imagem
    attachment = email.Attachments.Add(image_path)
    attachment_cid = "Assinatura"  # CID para referenciar a imagem no HTML

    # Configurar e-mail
    email.To = "cadastro@opusmedical.com.br; augusto@opusmedical.com.br; almoxarifado@opusmedical.com.br; comercial@opusmedical.com.br; logistica@opusmedical.com.br; suportetecnico@opusmedical.com.br"
    email.Subject = "Cadastrado"
    email.HTMLBody = f"""
        <p>Itens cadastrados.</p>
        <p>O equipamento com número de série {numero_serie} foi cadastrado com sucesso no OMIE.</p>
        <p>Código OMIE: {codOMIE}</p>
        <p><img src="cid:{attachment_cid}"></p>  <!-- Referência à imagem -->
    """ 
    try:
        email.Send()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
