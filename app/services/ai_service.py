
import os
import logging

from groq import AsyncGroq  
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

MODEL_NAME = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY não encontrada.")
    raise ValueError("GROQ_API_KEY ausente no arquivo .env")

# Instancindo o cliente como AsyncGroq
client = AsyncGroq(
    api_key=GROQ_API_KEY,
    timeout=30
)

SYSTEM_PROMPT = """
Você é um Especialista em Nutrição Esportiva.

REGRAS:
- Responda apenas sobre:
  - nutrição
  - alimentação
  - calorias
  - exercícios
  - saúde
  - emagrecimento
  - ganho de massa

- Perguntas fora do tema devem ser recusadas educadamente.

- Destaque:
  - calorias
  - proteínas
  - carboidratos
  - gorduras

- Use Markdown.

- Seja claro e objetivo.

- Sempre finalize com:
'Dica do Nutri: ...'
"""


async def ask_ai(message: str) -> str:

    if not message.strip():
        raise HTTPException(
            status_code=400,
            detail="Mensagem vazia."
        )

    if len(message) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Mensagem muito longa."
        )

    try:
        logger.info(f"Pergunta recebida: {message}")

        # Adicionando o 'await' antes da chamada do cliente
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        ai_response = response.choices[0].message.content
        logger.info("Resposta gerada com sucesso.")
        return ai_response

    except Exception as e:
        logger.error(f"Erro na IA: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Serviço de IA temporariamente indisponível."
        )