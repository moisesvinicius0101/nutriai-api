

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemes.auth import UserCreate, UserLogin, UserResponse 
from app.core.security import authenticate_user, create_access_token, get_current_user
from app.services.auth_service import create_user  

router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]

#
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: db_dependency):

    novo_usuario = create_user(db=db, user=user)
    return novo_usuario 



@router.post("/login")
async def login(user: UserLogin, db: db_dependency):
    
    usuario_autenticado = authenticate_user(db=db, email=user.email, password=user.password)
    
    if not usuario_autenticado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
  
    token_acesso = create_access_token(data={"sub": usuario_autenticado.email})
   
   
    return {
        "access_token": token_acesso,
        "token_type": "bearer",
        "user": {
            "id": usuario_autenticado.id,
            "full_name": usuario_autenticado.full_name,
            "email": usuario_autenticado.email
        }
    }