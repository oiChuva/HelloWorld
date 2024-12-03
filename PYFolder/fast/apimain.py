from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Any

app = FastAPI()

class WebhookData(BaseModel):
    eventType: str
    data: Any

@app.post("/neovero-receiver")
async def webhook(request: Request):
    payload = await request.json()
    
    if payload.get('eventType') != 'nv.orcamento-venda.approved':
        raise HTTPException(status_code=400, detail="Invalid eventType")
    
    print(f"Received data: {payload}")
    
    if 'message' in payload and 'numeroSerie' in payload['message']:
        print(f"numeroSerie: {payload['message']['numeroSerie']}")
    
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
