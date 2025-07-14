from fastapi import UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
from app.config import settings


cloudinary.config(
    cloud_name = settings.CLOUD_NAME,
    api_key = settings.API_KEY,
    api_secret = settings.API_SECRET_KEY
)

def upload_to_cloudinary(file: UploadFile):
    try:
        contents = file.file.read()
        result = cloudinary.uploader.upload(contents, folder="chat_app_images")  

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image to Cloudinary: {e}")