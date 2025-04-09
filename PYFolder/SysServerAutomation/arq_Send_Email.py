import pythoncom
import win32com.client as win32
from threading import Lock

email_lock = Lock()

def Send_Email(ht_mail):
    with email_lock:
        print(f"[DEBUG] Iniciando envio de e-mail com conteúdo: {ht_mail}")
        pythoncom.CoInitialize()
        try:
            outlook = win32.Dispatch('outlook.application')
            email = outlook.CreateItem(0)
            email.To = "logistica@opusmedical.com.br;  almoxarifado@opusmedical.com.br; almoxarifado2@opusmedical.com.br"
            email.Subject = "Requisição de item do estoque"
            email.HTMLBody = ht_mail
            email.Send()
            print("[DEBUG] Email enviado com sucesso.")
        except Exception as e:
            print(f"[ERROR] Erro ao enviar e-mail: {e}")
        finally:
            pythoncom.CoUninitialize()