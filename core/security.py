from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os 
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password:str):
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)

def verify_password(password,hashpassword):
    password = password.encode("utf-8")[:72]
    return pwd_context.verify(password,hashpassword)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MIN = int(os.getenv("EXPIRE_MIN"))

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
