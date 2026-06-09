
from fastapi import FastAPI
from app.routes import chat, auth
from app.database import Base, engine, ensure_schema

description = """
**API NutriAi** - Uma API inteligente para auxiliar nas suas consultas e rotinas de nutrição. 🥑

### 🔒 Como testar a autenticação:
1. Vá até a rota **POST `/auth/login`** (ou use as credenciais de um usuário já criado).
2. Copie o código gerado no campo `access_token`.
3. Suba a página, clique no botão **Authorize** (o cadeado no topo direito).
4. Cole apenas o código gerado e clique em **Authorize**.
5. Pronto! As rotas do Chat já estarão liberadas para uso. 🚀
"""

app = FastAPI(title="Api NutriAi", description=description, version="1.0.0")


Base.metadata.create_all(bind=engine)
ensure_schema()

app.include_router(auth.router)
app.include_router(chat.router)