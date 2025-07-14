# class ConnectionManager:
#     #initialize list for websockets connections
#     def __init__(self):    
#         self.active_connections: List[WebSocket] = []
#         self.connection_names: dict[WebSocket, str] = {}

#     async def connect(self, websocket: WebSocket):
#         if len(self.active_connections) >= 5:
#             await websocket.accept()
#             await websocket.send_text("Room full. Try again later.")
#             await websocket.close()
            
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
        
#     async def broadcast(self, message: str, websocket: WebSocket = None):
#         for connection in self.active_connections:
#             if websocket is not None and connection == websocket:
#                 continue
#             await connection.send_text(message)

    
#     def set_name(self, websocket: WebSocket, name: str):
#         self.connection_names[websocket] = name

#     def get_name(self, websocket: WebSocket) -> str:
#         return self.connection_names.get(websocket, "Unknown")
    

# connectionmanager = ConnectionManager()


# @app.get("/", response_class=HTMLResponse)
# def join_page(request: Request):
#     return templates.TemplateResponse("join.html", {"request" : request})

# @app.get("/home", response_class=HTMLResponse)
# def home_page(request: Request):
#     return templates.TemplateResponse("home.html", {"request" : request})





# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):

#     await connectionmanager.connect(websocket)
    
#     try:
#         # Wait for the first message (token)
#         first_data = await websocket.receive_text()
#         first_data = json.loads(first_data)
#         token = first_data.get("token")

#         db: Session = SessionLocal()
#         guest = db.query(Guest).filter(Guest.id == token).first()
#         name = guest.name if guest else "Unknown"

#         # Register the name with the connection
#         connectionmanager.set_name(websocket, name)

#         # Announce join
#         await connectionmanager.broadcast(json.dumps({
#             "name": "Server",
#             "message": f"{name} joined the chat"
#         }))

#         # Main message loop
#         while True:
#             data = await websocket.receive_text()
#             data = json.loads(data)
#             message = data.get("message")

#             payload = json.dumps({"name": name, "message": message})
#             await connectionmanager.broadcast(payload, websocket)

#     except WebSocketDisconnect:
#         # Retrieve name from connection manager before removing it
#         name = connectionmanager.get_name(websocket)
#         connectionmanager.disconnect(websocket)

#         await connectionmanager.broadcast(json.dumps({
#             "name": "Server",
#             "message": f"{name} left the chat"
#         }))
