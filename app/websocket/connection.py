from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):    
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= 5:
            await websocket.accept()
            await websocket.send_text("Room full. Try again later.")
            await websocket.close()
        else:
            await websocket.accept()
            self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket = None):
        for connection in self.active_connections:
            if websocket is not None and connection == websocket:
                continue
            await connection.send_text(message)


connectionmanager = ConnectionManager()
