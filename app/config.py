import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:

    CLOUD_NAME : str = os.getenv("CLOUD_NAME")
    API_KEY : str = os.getenv("API_KEY")
    API_SECRET_KEY : str = os.getenv("API_SECRET_KEY")
    
settings = Settings()
