from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class User(BaseModel):
    name : str = Form(...)


class MessageRequest(BaseModel):
    token: str
    message: str


class PayLoad(BaseModel):
    name : str
    email :  str


class Token(BaseModel):
    token : str