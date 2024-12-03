import requests
from bs4 import BeautifulSoup 
import pandas as pd

# Carregar o arquivo Excel
caminho_do_arquivo = 'valorcURL.xlsx'
planilha = pd.read_excel(caminho_do_arquivo)

# Lista para armazenar os valores coletados
valores_coletados = []

for linha in planilha['Vlink']:
    # Obter o valor da coluna "Vlink" para a linha atual
    VLink = str(linha)
    link = "https://opusmedical.neovero.com/SetorAlterar.aspx?TelaCliente=S&Codigo=" + VLink
    headers = {
                "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "authority": "opusmedical.neovero.com",
                "Cookie": "ASP.NET_SessionId=cdbupevoneeppd05mo1n1q3j; .AspNet.Cookies=P49YvtjR1k3dXdkKsKVEOo_QuygFQXL0wkJ8xrqR241rYbX3uKB3zh6sRbxR9tVdMsTPdtS51IGnnXSBGjoFRlY2sQfL6rU2_8HZZoJAvaJaWU9GzHsIg0oIaKiwnvZ6_9k81rG2XBGjZ1u36RpHmHwKjzXl82vR9lUP3w1P9BUYQ_MUCKEre2qqBSIZetdHIeAxWo373gKzPa-BcQuDDqzaysiyr7Jivyv6iL0B7MkKbadW8qxpJ63peBo-0VKESLcnucVrOGZq6N41aTEnr5EWrW59tDXLR3hRT8jv-runMSvfAMg3MNFnRNEDSB7vrlOBjGURlYfEBfelM2zWv-zBG0_VcZ2jYJQ9EW_F2NTDkfV6tFV0jIVW-3WLKSpCmUGo_BMB1i01jLzAZVGe5wsrmxyRGGp_rOAFC_bOcP0g--8ddk7ZdBWWBwhRqt1AuboDJ6IsCQad3SbPWl-c4KLv-K_p93_YEHox_aBb3q6Fdl50olxc6CtZozBpeZiryWYa3E23626fAddojiE7r_QL67tSFSw3a4gRgOuUT46kf0bid3g8bFoghU_pyf3nncE1d4wWmbSM9eTj0UfrPy2IR-8ZuhrQD0lATc1mcaLMkuNSRGVE_CaFy_cmwDLWtEoVWVUON3bEkGGuxaKbFWjcmEVYbXaZfq6JmTpmEaTOzLY3cQWMcgpMqNfKGLCNJDRbwOEo91swdsrawdV29qB5xav17YB4ksESEzaPvWutLjTbQ325KkjN5Nj_8zABeGRpAsCKcIU5jbxQwVyDn2ymGUrAY-w-ypYpepAHhlWY9-w_aPtxGZLu01KG96RATuhKAtXf-ijNBazX5rezTmwSsOaJVSxi9JAbJY3hsG3_i8gaajjXgy7usL8qpMpl3KzygI3wItMQ4C-P7RU4-dZ8K2HrYW3Yb8nhsdm3DFpQw_sLmtyoFSBlEardxwX7zWI8yJaLKxMwSI60DgCCr_dr9vzpp7D2ZackXN86dMM0gNavRfTL5cYq2wwhUE9X9XvfH_eCB9I6gSR4oYKWjw"
              }
    requisicao = requests.get(link, headers=headers)
    site = BeautifulSoup(requisicao.text, "html.parser")

    titulo = site.find('title').text.strip()
    pesquisa2 = site.find("input", {"name": "txtcod_equipamento_nominal"})
    valor_coletado = pesquisa2["value"]  if pesquisa2 else None
    print("Valor atual de VLink:", VLink)
    print(requisicao)
    print(titulo)
    print(pesquisa2)
    print(valor_coletado)
    valores_coletados.append(valor_coletado)

# Adicionar os valores coletados como uma nova coluna no DataFrame
planilha['Valor Coletado'] = valores_coletados

# Salvar o DataFrame em um novo arquivo Excel
planilha.to_excel('valorcURL_coletado.xlsx', index=False)
