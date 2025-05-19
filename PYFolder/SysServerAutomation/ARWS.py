from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import logging
import random

# Importação das funções existentes
from arq_consultar_equipamento import consultar_equipamento
from arq_cadastrar_cliente import cadastrar_cliente
from arq_process_queue import process_queue
from arq_Send_Email import Send_Email
from arq_requisicao_inclusao_D import requisicao_inclusao_D
from arq_requisicao_inclusao_O import requisicao_inclusao_O
from arq_enviar_email import enviar_email
from arq_lerEstoque import lerEstoque
from arq_NF_Functions import requisicao_consulta_nf
from arq_NF_Functions import requisicao_consultar_empresa
from arq_NF_Functions import requisicao_consulta_endereco_dest
from arq_req_fuctions import incluir_requisicao_compra
from arq_req_fuctions import consultar_produto

def calcular_data_sugestao(dias_uteis):
    """
    Calcula a data de sugestão adicionando um número de dias úteis à data atual.
    Pula sábados e domingos.
    """
    data_atual = datetime.now()
    dias_adicionados = 0

    while dias_adicionados < dias_uteis:
        data_atual += timedelta(days=1)
        # Incrementa apenas se não for sábado (5) ou domingo (6)
        if data_atual.weekday() < 5:
            dias_adicionados += 1

    return data_atual.strftime("%d/%m/%Y")

def gerar_codIntReqCompra():
    """
    Gera um código aleatório no padrão API00000X00.
    """
    parte_numerica = f"{random.randint(0, 99999):05}"  # Gera um número de 5 dígitos com zero à esquerda
    parte_letra = chr(random.randint(65, 90))  # Gera uma letra maiúscula aleatória (A-Z)
    parte_final = f"{random.randint(0, 99):02}"  # Gera um número de 2 dígitos com zero à esquerda
    return f"API{parte_numerica}{parte_letra}{parte_final}"

# External SysServerAutomation/arq_NF_Functions.py
app_key = "1826443506888"
app_secret = "c9e60167e96e156e2655a92fdcd77df7"

app = FastAPI(title="ODE PROXY API", version="1.0.0")
queue = Queue()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (use isso com cautela em produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Thread para processar a fila de forma assíncrona
queue_thread = Thread(target=process_queue)
queue_thread.daemon = True
queue_thread.start()

logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def log_request_data(request: Request, call_next):
    body = await request.body()
    logger.info(
        f"Client: {request.client.host}, Method: {request.method}, Path: {request.url.path}, Body: {body.decode('utf-8')}"
    )
    response = await call_next(request)
    return response

@app.get("/test-page", response_class=HTMLResponse)
async def test_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; text-align: center; padding: 50px; }
            h1 { color: #4CAF50; }
            p { font-size: 1.2em; }
            .status { font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Server is Running!</h1>
        <p>Welcome to the <span class="status">FastAPI Server Test Page</span></p>
        <p>Status: <span class="status">OK</span></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/neovero-receiver")
async def webhook(request: Request):
    """Recebe dados via webhook e processa a inclusão."""
    try:
        data = await request.json()
        print(f"Received data: {data}")
        
        numero_serie_input = data.get("numeroSerie")
        if not numero_serie_input:
            raise ValueError("numeroSerie is required")
        
        # Consulta equipamento para obter `empresa_id`
        resultado = consultar_equipamento(numero_serie_input)
        
        if "error" in resultado:
            raise ValueError(resultado["error"])
        
        # Extração das informações relevantes
        codOMIE = resultado.get('codOMIE')
        if not codOMIE:
            raise ValueError("O código do produto (codOMIE) é obrigatório e não pode estar vazio.")
        Ncm = resultado.get("ncm")
        descOMIE = f"{resultado.get('nome')} {resultado.get('numeroSerie', '')}"
        unidade = "UN"
        modelo_nome = resultado.get("modelo", {}).get("nome", "")
        fabricante_nome = resultado.get("modelo", {}).get("fabricante", {}).get("nome", "")
        CodFamilia = resultado.get("codigoFamilia")
        valor_aquisicao = resultado.get("valorAquisicao", 0)
        blocoK=resultado.get("blocoK")
        empresa_id = resultado.get("empresaId")
        print(empresa_id)
        
        # Processa inclusão com base no `empresa_id`
        if empresa_id == "3":
            requisicao_inclusao_D(
                codigo=codOMIE,
                ncm=Ncm,
                descricao_completa=descOMIE,
                unidade=unidade,
                modelo=modelo_nome,
                marca=fabricante_nome,
                codigo_familia=CodFamilia,
                origem_mercadoria="0",
                valor_unitario=valor_aquisicao,
                blocoK=blocoK
            )
        else:
            requisicao_inclusao_O(
                codigo=codOMIE,
                ncm=Ncm,
                descricao_completa=descOMIE,
                unidade=unidade,
                modelo=modelo_nome,
                marca=fabricante_nome,
                codigo_familia=CodFamilia,
                origem_mercadoria="0",
                valor_unitario=valor_aquisicao,
                blocoK=blocoK
            )
        
        # Envia e-mail
        enviar_email(numero_serie=numero_serie_input, codOMIE=codOMIE)
        return JSONResponse(content={"message": "Recebido com sucesso e adicionado à fila"}, status_code=200)
    except Exception as e:
        # Registra erro no log e retorna status 200 com mensagem de erro
        print(f"Erro ao processar requisição: {str(e)}")
        return JSONResponse(
            content={"message": "Erro processado internamente, mas identificado como sucesso.", "error": str(e)},
            status_code=200
        )

@app.post("/neovero-end-c")
async def webhook_end_c(request: Request):
    """Recebe dados para cadastrar cliente."""
    try:
        data = await request.json()
        print(f"Received data from /neovero-end-c: {data}")
        
        codigo_cliente = data.get("codigo_cliente")
        if not codigo_cliente:
            raise HTTPException(status_code=400, detail="codigo_cliente is required")
        
        cadastrar_cliente(codigo_cliente)
        return JSONResponse(content={"message": "Recebido com sucesso pelo Endpoint"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

sent_emails = set()

@app.post("/sendmail")
async def webhook_end_s(request: Request):
    """Recebe dados para envio de e-mail."""
    try:
        data = await request.json()
        ht_mail = data.get("ht_mail")
        if not ht_mail:
            raise HTTPException(status_code=400, detail="ht_mail is required")
        
        if ht_mail in sent_emails:
            return JSONResponse(content={"message": "E-mail já enviado anteriormente"}, status_code=200)
        
        sent_emails.add(ht_mail)
        Send_Email(ht_mail)
        return JSONResponse(content={"message": "Recebido com sucesso pelo Endpoint"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/LerEst")
def webhook_end_l():
    """Lê dados do estoque com base na data atual."""
    try:
        # Data de posição definida internamente
        data_posicao = datetime.now().strftime("%d/%m/%Y")

        # Chamar a função lerEstoque
        estoque_json = lerEstoque(data_posicao)
        
        return JSONResponse(content=estoque_json, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/EtiquetaNota")
async def webhook_end_E(request: Request):
    """Read the fiscal notes with no exception in the Omie Sistem."""
    try:
        data = await request.json()
        print(f"Received data: {data}")
        numero_serie_input = data.get("numeroSerie")
        if not numero_serie_input:
            raise HTTPException(status_code=400, detail="numeroSerie is required")

        return {"message": "Data received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/NotaFiscal")
async def webhook_end_NF(request: Request):
    """
    Webhook que utiliza o número da nota fiscal (numNF) para puxar os dados da NF,
    empresa e endereço do destinatário.
    """
    try:
        # Parsear os dados da requisição
        data = await request.json()
        nNF = data.get("numNF")
        if not nNF:
            raise HTTPException(status_code=400, detail="Número da nota fiscal (numNF) é obrigatório.")

        # Consultar dados da nota fiscal
        resultado_nf = requisicao_consulta_nf("0", nNF)
        if not resultado_nf:
            raise HTTPException(status_code=404, detail="Dados da nota fiscal não encontrados.")

        razao_social_dest, cnpj_cpf_dest, numero_nf_dest, tp_nf, detalhes_produtos, nCodEmp, nCodCli = resultado_nf

        # Consultar dados da empresa
        empresa_consultada = requisicao_consultar_empresa(nCodEmp)
        if not empresa_consultada:
            raise HTTPException(status_code=404, detail="Dados da empresa não encontrados.")

        # Consultar endereço do destinatário
        endereco_destino = requisicao_consulta_endereco_dest(nCodCli)
        if not endereco_destino:
            raise HTTPException(status_code=404, detail="Endereço do destinatário não encontrado.")

        # Montar a resposta
        response_data = {
            "numero_nf_dest": numero_nf_dest,
            "tipo_nf": tp_nf,
            "destinatario": {
                "razao_social": razao_social_dest,
                "cnpj_cpf": cnpj_cpf_dest,
                "endereco": endereco_destino,
            },
            "remetente": {
                "razao_social": empresa_consultada['razao_social'],
                "telefone": f"({empresa_consultada['telefone1_ddd']}) {empresa_consultada['telefone1_numero']}",
            },
            "produtos": detalhes_produtos,
        }

        return JSONResponse(content=response_data)

    except HTTPException as http_exc:
        # Tratar exceções específicas do FastAPI
        raise http_exc

    except Exception as e:
        # Tratar erros gerais
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/RequisicaoInclusaoCompra")
async def requisicao_inclusao_compra_endpoint(request: Request):
    """
    Endpoint para incluir uma compra na API Omie.
    O codItem recebido será pesquisado na função consultar_produto.
    """
    try:
        # Recebe os dados da requisição
        print("[INFO] Recebendo dados da requisição...")
        data = await request.json()
        print(f"[INFO] Dados recebidos: {data}")

        codItem = data.get("codItem")
        qtde = data.get("qtde")
        obsReqCompra = data.get("obsReqCompra")

        if not codItem or not qtde:
            print("[ERROR] Campos obrigatórios ausentes: codItem ou qtde.")
            raise HTTPException(status_code=400, detail="codItem e qtde são obrigatórios.")

        # Chama a função consultar_produto para obter o codProd
        print(f"[INFO] Consultando produto com codItem: {codItem}")
        codProd = consultar_produto(codItem)
        if not codProd:
            print(f"[ERROR] Produto com codItem '{codItem}' não encontrado.")
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
        print(f"[INFO] Produto encontrado. codProd: {codProd}")

        # Calcula a data de sugestão (5 dias úteis a partir de hoje)
        print("[INFO] Calculando data de sugestão...")
        dtSugestao = calcular_data_sugestao(5)
        print(f"[INFO] Data de sugestão calculada: {dtSugestao}")

        # Gera o código interno da requisição
        print("[INFO] Gerando código interno da requisição...")
        codIntReqCompra = gerar_codIntReqCompra()
        print(f"[INFO] Código interno gerado: {codIntReqCompra}")

        # Chama a função para incluir a requisição de compra
        print("[INFO] Incluindo requisição de compra...")
        response = incluir_requisicao_compra(
            codIntReqCompra=codIntReqCompra,
            codProj=7396740205,  # Exemplo de código do projeto
            dtSugestao=dtSugestao,  # Data de sugestão calculada
            obsIntReqCompra=obsReqCompra,  # Exemplo de observação
            codItem=codItem,
            codProd=codProd,
            qtde=qtde
        )
        print("[INFO] Requisição de compra incluída com sucesso.")

        return JSONResponse(content={"message": "Requisição incluída com sucesso", "codIntReqCompra": codIntReqCompra}, status_code=200)

    except HTTPException as http_exc:
        # Tratar exceções específicas do FastAPI
        print(f"[ERROR] HTTPException: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        # Tratar erros gerais
        print(f"[ERROR] Erro inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
