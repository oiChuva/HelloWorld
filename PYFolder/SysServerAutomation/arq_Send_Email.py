import pythoncom
import win32com.client as win32

def Send_Email(ht_mail):
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = "logistica@opusmedical.com.br; augusto@opusmedical.com.br; almoxarifado@opusmedical.com.br; compras@opusmedical.com.br; compras2@opusmedical.com.br"
    email.Subject = "Requisição de item do estoque"
    email.HTMLBody = ht_mail
    email.Send()
    print("Email enviado.")
    # Exibir mensagem de sucesso
    print("Sucesso", "Email enviado com sucesso!")
    pythoncom.CoUninitialize()