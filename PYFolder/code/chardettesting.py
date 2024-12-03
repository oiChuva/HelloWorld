# Vamos tentar detectar a codificação e depois decodificar
import chardet

# Texto original corrompido
corrupted_text = b'\xc2\xbc\xc2\xbe\xc2\xbb\xc2\xaa\xc3\xab\xc2\xba\xc3\x9aa634511266'

# Detectar a codificação
detected_encoding = chardet.detect(corrupted_text)
print(detected_encoding)

# Decodificar usando a codificação detectada (se for uma codificação válida)
decoded_text = corrupted_text.decode(detected_encoding['encoding'])
print(decoded_text)
