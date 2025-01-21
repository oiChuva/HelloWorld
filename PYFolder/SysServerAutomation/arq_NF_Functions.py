import threading
import requests
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import json
import os
from openpyxl import Workbook

def requisicao_consulta_nf(nCodNF, nNF):
    url_nf = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
    dados_nf = {
        "call": "ConsultarNF",
        "app_key": "1826443506888",
        "app_secret": "c9e60167e96e156e2655a92fdcd77df7",
        "param": [
            {
                "nCodNF": nCodNF,
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
            detalhes_produtos.append({
                "cProd": prod.get("cProd", ""),
                "xProd": prod.get("xProd", ""),
                "vProd": prod.get("vProd", ""),
                "qCom": prod.get("qCom", "")
            })

        nf_emit_int = resposta_json.get("nfEmitInt", {})
        nCodEmp = nf_emit_int.get("nCodEmp", "")

        return razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli
    else:
        raise Exception(f"Erro ao consultar NF. Status code: {response.status_code}, Response: {response.text}")

def requisicao_consultar_empresa(nCodEmp):
    url = "https://app.omie.com.br/api/v1/geral/empresas/"
    dados = {
        "call": "ConsultarEmpresa",
        "app_key": "1826443506888",
        "app_secret": "c9e60167e96e156e2655a92fdcd77df7",
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
            'telefone1_ddd': dados_empresa.get('telefone1_ddd', ''),
            'telefone1_numero': dados_empresa.get('telefone1_numero', '')
        }
    else:
        raise Exception(f"Erro ao consultar empresa. Status code: {response.status_code}, Response: {response.text}")

def requisicao_consulta_endereco_dest(nCodCli):
    url = "https://app.omie.com.br/api/v1/geral/clientes/"
    dados = {
        "call": "ConsultarCliente",
        "app_key": "1826443506888",
        "app_secret": "c9e60167e96e156e2655a92fdcd77df7",
        "param": [
            {
                "codigo_cliente_omie": nCodCli
            }
        ]
    }
    response = requests.post(url, json=dados)

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
        raise Exception(f"Erro ao consultar endereço. Status code: {response.status_code}, Response: {response.text}")
