

from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.models import User  

from app.schemes.chat import ChatRequest, ChatResponse
from app.services.ai_service import ask_ai 
from app.core.security import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    redirect_slashes=False  
)


@router.post(
    "",
    response_model=ChatResponse
)
async def chat(
    data: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)]
):
    ai_response = await ask_ai(data.message)

    return ChatResponse(
        response=ai_response
    )