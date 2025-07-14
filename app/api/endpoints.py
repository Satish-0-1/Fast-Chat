from fastapi import APIRouter, Depends, HTTPException, status
from app.db import get_db
from sqlalchemy.orm import Session, joinedload
from app.models import Guest, Message
from app.schemas import MessageRequest, PayLoad, Token
from app.auth import create_access_token
from fastapi import File, UploadFile, HTTPException
from app.helper import upload_to_cloudinary
from app.websocket.connection import connectionmanager
import json


router = APIRouter()


# SAVING MESSAGES TO THE DATABASE CORRESPONDING TO USER'S NAME
@router.post("/messages")
async def message_storage(request: MessageRequest, db: Session = Depends(get_db)):
    try:
        guest_user = db.query(Guest).filter(Guest.id == request.token).first()
        if not guest_user:
            raise HTTPException(status_code=404, detail="User not found")
        name = guest_user.name
        new_message = Message(chat=request.message, user_id=request.token)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {"message": f"Message saved successfully in the DB: {new_message.chat}","name" : name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error !, {e}")




# JOIN ROOM API, ALSO SENDING MESSAGE : {NAME} HAS JOINED
@router.post("/join-room")
async def new_user(data : PayLoad, db : Session = Depends(get_db)): 
    try:
        name = data.name
        email = data.email
        existing_user = db.query(Guest).filter(Guest.email == email).first()
        if existing_user:
            access_token = create_access_token(data={"user_id": str(existing_user.id)})
            await connectionmanager.broadcast(json.dumps({
                "name": "Server",
                "message": f"{existing_user.name} has joined the chat"
            }))
            return {
                "success": True,
                "status": status.HTTP_200_OK,
                "access_token": access_token,
                "id": existing_user.id
            }

        new_guest = Guest(
            name = name,
            email = email
        )
        db.add(new_guest)
        db.commit()
        db.refresh(new_guest)
        access_token = create_access_token(data={"user_id": str(new_guest.id)})
        await connectionmanager.broadcast(json.dumps({
                "name": "Server",
                "message": f"{existing_user.name} has joined the chat"
            }))

        return {"success" : True,
                "status" : status.HTTP_200_OK,
                "access_token" : access_token,
                "id" : new_guest.id,
                "name" : new_guest.name}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal Server Error !, {e}")
    


# UPLOADING THE IMAGES TO THE CLOUDINARY
@router.post("/upload-image/")
async def upload_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    upload_result = upload_to_cloudinary(file)
    return upload_result
  



# GETTING ALL CHATS AND IN HOME.HTML ASSIGNING THE CHATS ACCORDING TO THE CURENT USER 
@router.post("/chat-history")
def get_chat_history(data : Token,db: Session = Depends(get_db)):
    token = data.token
    messages = db.query(Message).options(joinedload(Message.user)).order_by(Message.send_at.asc()).all()
    current_user = db.query(Guest).filter(Guest.id == token).first()
    return [
        {
            "current" : current_user.name if current_user else "Unknown",
            "name": message.user.name,
            "message": message.chat,
            "time": message.send_at.isoformat()
        }
        for message in messages
    ]