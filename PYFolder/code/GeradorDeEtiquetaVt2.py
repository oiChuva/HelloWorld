import requests
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT  # Importando os alinhamentos



def requisicao_consulta_nf(nCodNF, nNF):
    url_nf = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    dados_nf = {
        "call": "ConsultarNF",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "nNF": nNF
            }
        ]
    }
    response = requests.post(url_nf, json=dados_nf)

    if response.status_code == 200:
        resposta_json = response.json()
        
        nf_dest = resposta_json.get("nfDestInt", {})
        razao_social_dest = nf_dest.get("cRazao", "")
        cnpj_cpf_dest = nf_dest.get("cnpj_cpf", "")
        nCodCli = nf_dest.get("nCodCli", "")

        ide = resposta_json.get("ide", {})
        numero_nf_dest = ide.get("nNF", "")
        tp_nf = ide.get("tpNF", "")

        detalhes_produtos = []
        detalhes = resposta_json.get("det", [])
        for detalhe in detalhes:
            prod = detalhe.get("prod", {})
            cProd = prod.get("cProd", "")
            xProd = prod.get("xProd", "")
            vProd = prod.get("vProd", "")
            qCom = prod.get("qCom", "")
            detalhes_produtos.append({"cProd": cProd, "xProd": xProd, "vProd": vProd, "qCom": qCom})

        nf_emit_int = resposta_json.get("nfEmitInt", {})
        nCodEmp = nf_emit_int.get("nCodEmp", "")

        return razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)
        return None, None, None, None, None, None, None

def requisicao_consultar_empresa(nCodEmp):
    url = "https://app.omie.com.br/api/v1/geral/empresas/"
    dados = {
        "call": "ConsultarEmpresa",
        "app_key": "1826443506888",
        "app_secret": "4a98af31f25d8b152a18911c65d23190",
        "param": [
            {
                "codigo_empresa": nCodEmp
            }
        ]
    }
    response = requests.post(url, json=dados)

    if response.status_code == 200:
        dados_empresa = response.json()
        return {
            'razao_social': dados_empresa.get('razao_social', ''),
            'cnpj_cpf': dados_empresa.get('cnpj', ''),  # Ajuste para incluir o CNPJ
            'telefone1_ddd': dados_empresa.get('telefone1_ddd', ''),
            'telefone1_numero': dados_empresa.get('telefone1_numero', '')
        }
    else:
        print("Erro na requisição:", response.status_code)
        return None


def requisicao_consulta_endereco_dest(nCodCli):
    app_key = "1826443506888"
    app_secret = "4a98af31f25d8b152a18911c65d23190"
    url = "https://app.omie.com.br/api/v1/geral/clientes/"
    dados = {
        "call": "ConsultarCliente",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "codigo_cliente_omie": nCodCli,
                "codigo_cliente_integracao": ""
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(dados), headers=headers)

    if response.status_code == 200:
        resposta_json = response.json()
        endereco = resposta_json.get('endereco', '')
        endereco_numero = resposta_json.get('endereco_numero', '')
        bairro = resposta_json.get('bairro', '')
        cidade = resposta_json.get('cidade', '')
        estado = resposta_json.get('estado', '')
        complemento = resposta_json.get('complemento', '')
        cep = resposta_json.get('cep', '')
        endereco_completo = f"{endereco}, {endereco_numero}, {bairro}, {cidade}, {estado}, {complemento}, {cep}"
        return endereco_completo
    else:
        print("Erro na requisição. Código de status:", response.status_code)
        print(response.text)
        return None

def gerar_etiqueta(dados_nf, dados_empresa, endereco_dest, detalhe_produto, quantidade, volume):
    doc = SimpleDocTemplate(f"etiqueta_{dados_nf[2]}.pdf", pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.fontSize = 16
    title_style.leading = 20
    normal_style = styles["Normal"]

    # Título
    elements.append(Paragraph("CONFERÊNCIA - EXPEDIÇÃO", title_style))

    # Linha de entrega e retirada com logo
    data = [
        [Paragraph('ENTREGA', normal_style), 'X', Paragraph('RETIRADA', normal_style), Image('logo.png', width=50, height=50)]
    ]
    table = Table(data, colWidths=[120, 30, 120, 100])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    
    elements.append(Spacer(1, 12))

    # Dados principais
    data = [
        [Paragraph(f'NOTA FISCAL Nº:', normal_style), Paragraph(dados_nf[2], normal_style)],
        [Paragraph(f'VOLUMES:', normal_style), Paragraph(str(volume), normal_style)],
        [Paragraph(dados_empresa['razao_social'], normal_style), ''],
        [Paragraph(f'CNPJ:', normal_style), Paragraph(dados_empresa['cnpj_cpf'], normal_style)],
        [Paragraph(f'CLIENTE/FORNECEDOR:', normal_style), Paragraph(dados_nf[0], normal_style)],
        [Paragraph(f'CNPJ:', normal_style), Paragraph(dados_nf[1], normal_style)],
        [Paragraph(f'ENDEREÇO:', normal_style), Paragraph(endereco_dest, normal_style)],
        [Paragraph(f'DESCRIÇÃO:', normal_style), Paragraph(detalhe_produto["xProd"], normal_style)],
        [Paragraph(f'CÓDIGO:', normal_style), Paragraph(detalhe_produto["cProd"], normal_style)],
        [Paragraph(f'QUANTIDADE:', normal_style), Paragraph(str(quantidade), normal_style)],
    ]

    table = Table(data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(Spacer(1, 12))
    elements.append(table)
    
    doc.build(elements)


nNF = input("Digite o número da NF: ")

razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli = requisicao_consulta_nf("", nNF)

if numero_nf_dest:
    print(f"Razão Social do Destinatário: {razao_social_dest}")
    print(f"CNPJ/CPF do Destinatário: {cnpj_cpf_dest}")
    print(f"Número da NF: {numero_nf_dest}")
    print(f"Tipo de NF: {tp_nf}")
    print(f"Código da Empresa Emitente: {nCodEmp}")
    print(f"Código do Cliente: {nCodCli}")

    dados_empresa = requisicao_consultar_empresa(nCodEmp) if nCodEmp else None
    endereco_completo = requisicao_consulta_endereco_dest(nCodCli) if nCodCli else None

    if dados_empresa and endereco_completo:
        print("\nDetalhes dos Produtos:")
        for produto in detalhes_produtos:
            print(f"Código: {produto['cProd']}, Descrição: {produto['xProd']}, Valor: {produto['vProd']}, Quantidade: {produto['qCom']}")
            quantidade = produto['qCom']
            qVol = input("Digite o Volume: ")

            # Chamar a função para gerar a etiqueta
            gerar_etiqueta(
                dados_nf=(razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli),
                dados_empresa=dados_empresa,
                endereco_dest=endereco_completo,
                detalhe_produto=produto,
                quantidade=quantidade,
                volume=qVol
            )
    else:
        print("Não foi possível gerar a etiqueta devido a informações faltantes.")
else:
    print("Não foi possível consultar a NF.")
