

from fastapi import HTTPException, status
from app.core.security import verify_password, get_password_hash
from app.models.models import User
from app.schemes.auth import UserCreate

def create_user(db, user: UserCreate) -> User:
    # Verifica se o e-mail já está cadastrado no banco
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )

    
    hashed_password = get_password_hash(user.password)
    
    
    db_user = User(
        email=user.email, 
        full_name=user.full_name, 
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user