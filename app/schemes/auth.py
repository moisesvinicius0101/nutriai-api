
from pydantic import BaseModel, EmailStr, Field 


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=3)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None