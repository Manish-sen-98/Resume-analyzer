from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os 

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MIN = int(os.getenv("EXPIRE_MIN"))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        return username
    except JWTError: 
        raise credentials_exception
    
def hash_password(password:str):
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)

def verify_password(password,hashpassword):
    password = password.encode("utf-8")[:72]
    return pwd_context.verify(password,hashpassword)


def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
