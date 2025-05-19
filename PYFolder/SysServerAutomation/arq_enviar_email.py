import pythoncom
import win32com.client as win32
import os

def enviar_email(numero_serie, codOMIE):
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)

    # Caminho completo da imagem
    image_path = os.path.join(os.path.dirname(__file__), "Logo Isaque-05.png")
    
    # Verifica se o arquivo existe
    if not os.path.exists(image_path):
        print(f"Erro: O arquivo '{image_path}' não foi encontrado.")
        pythoncom.CoUninitialize()
        return

    try:
        # Anexar a imagem
        attachment = email.Attachments.Add(image_path)
        attachment_cid = 'myimage'
        attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", attachment_cid)
        
        # Configurar e-mail
        email.To = "cadastro@opusmedical.com.br; almoxarifado@opusmedical.com.br; marcelo@opusmedical.com.br; celio@opusmedical.com.br; comercial@opusmedical.com.br; logistica@opusmedical.com.br; suportetecnico@opusmedical.com.br"
        email.Subject = "Cadastrado"
        email.HTMLBody = f"""<p>O equipamento com número de série {numero_serie} foi cadastrado com sucesso no OMIE.</p>
         <p>Código OMIE: {codOMIE}</p> 
         <p><img src="cid:{attachment_cid}"></p> """
        
        email.Send()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    finally:
        pythoncom.CoUninitialize()
