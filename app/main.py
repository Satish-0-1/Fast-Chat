from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from app.api.endpoints import router as user_router
import json
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Guest
from app.websocket.connection import connectionmanager



app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])


templates = Jinja2Templates(directory="/home/developer/Documents/Fast Chat/templates")

@app.get("/", response_class=HTMLResponse)
def join_page(request: Request):
    return templates.TemplateResponse("join.html", {"request" : request})

@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request" : request})




# THIS IS MY WEBSOCKET
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):

    await connectionmanager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            token = data.get("token")
            message = data.get("message")
            db: Session = SessionLocal()
            
            guest = db.query(Guest).filter(Guest.id == token).first()
            name = guest.name if guest else "Unknown"

            payload = json.dumps({"name": name, "message": message})
            await connectionmanager.broadcast(payload, websocket)

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket)
        await connectionmanager.broadcast(json.dumps({
            "name": "Server",
            "message": f"{name} left the chat"
        }))
