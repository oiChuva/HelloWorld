from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from queue import Queue
from threading import Thread
from datetime import datetime
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

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

app = FastAPI(title="Minha API FastAPI", version="1.0.0")
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
            raise HTTPException(status_code=400, detail="numeroSerie is required")
        
        # Consulta equipamento para obter `empresa_id`
        resultado = consultar_equipamento(numero_serie_input)
        
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        # Extração das informações relevantes
        codOMIE = f"{resultado.get('numeroSerie', '')}-EQ{resultado.get('patrimonio', '') or ''}"
        Ncm = resultado.get("ncm", "9999.99.99")
        descOMIE = f"{resultado.get('nome', '')} {resultado.get('numeroSerie', '')}"
        unidade = "UN"
        modelo_nome = resultado.get("modelo", {}).get("nome", "")
        fabricante_nome = resultado.get("modelo", {}).get("fabricante", {}).get("nome", "")
        CodFamilia = resultado.get("codigoFamilia", "7281765596")
        valor_aquisicao = resultado.get("valorAquisicao", 0)

        empresa_id = resultado.get("empresaId")
        
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
            )
        
        # Envia e-mail
        enviar_email(numero_serie=numero_serie_input, codOMIE=codOMIE)
        return JSONResponse(content={"message": "Recebido com sucesso e adicionado à fila"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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


# Comando para rodar o servidor: `uvicorn ARWS:app --host 0.0.0.0 --port 5000 --log-level info --reload --log-config log_config.yaml`
