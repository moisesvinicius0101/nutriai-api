

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=2,
        max_length=1000,
        description="Mensagem enviada pelo usuário para análise nutricional",
        example="Quantas calorias tem 2 ovos cozidos?"
    )


class ChatResponse(BaseModel):
    response: str