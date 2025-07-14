from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone


SECRET_KEY = "8421e5bee29cbac54cc771f0ae3c33b926bd0be9db350f47a261826abf1db205"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict ,expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expiry_time = datetime.now(timezone.utc) + expires_delta
    else:
        expiry_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry_time})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise JWTError("Invalid token: No user_id")
        return user_id
    except JWTError:
        return None