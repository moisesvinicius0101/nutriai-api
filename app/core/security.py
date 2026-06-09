

# Toda parte de autenticação e segurança do sistema deve ser implementada aqui
import os 
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import Annotated
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError 
from passlib.context import CryptContext  
from sqlalchemy.orm import Session 

from app.database import get_db  
from app.models.models import User
from app.schemes.auth import TokenData


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

oauth2_schemes = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password) 

def get_password_hash(password: str):
    return pwd_context.hash(password)
    

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    
    
    if not verify_password(password, user.hashed_password): 
        return False
    return user


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
        

async def get_current_user(
    
    token_auth: Annotated[str, Depends(oauth2_schemes)], 
    db: Annotated[Session, Depends(get_db)] 
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        
        token_pura = token_auth.credentials
        
        payload = jwt.decode(token_pura, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub") 
        if username is None:
            raise credential_exception 
        token_data = TokenData(username=username)
        
    except (ExpiredSignatureError, InvalidTokenError):
        raise credential_exception
        
    user = db.query(User).filter(User.email == token_data.username).first()
    if user is None:
        raise credential_exception
        
    return user