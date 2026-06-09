

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    # Dados de Autenticação
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    historico_chat = relationship("ChatMessage", back_populates="usuario", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Quem mandou a mensagem: "user" (paciente) ou "assistant" (IA)
    role = Column(String, nullable=False) 
    
    # O texto da mensagem em si
    content = Column(String, nullable=False)
    
    # Horário da mensagem
    enviado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento inverso para voltar ao usuário
    usuario = relationship("User", back_populates="historico_chat")