import hmac
import hashlib

def generate_hmac_sha256(key: str, message: str) -> str:
    hmac_obj = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    hmac_hash = hmac_obj.hexdigest()  # Retorna o hash como uma string hexadecimal contínua

    return hmac_hash.upper()  # Converte para letras maiúsculas

if __name__ == "__main__":
    key = "SHA256="  # Atribua a chave aqui
    message = "meusegredo"
    custom_hmac_sha256_result = generate_hmac_sha256(key, message)
    print(f"Custom HMAC-SHA-256 of '{message}' with key '{key}': {custom_hmac_sha256_result}")
