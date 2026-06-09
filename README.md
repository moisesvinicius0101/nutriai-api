
# 🥑 NutriAi API

> Uma API inteligente de nutrição que integra inteligência artificial para responder dúvidas sobre alimentação, contagem de calorias e macros, totalmente protegida por autenticação JWT.

---

## 📸 Demonstração da Interface

Abaixo está uma prévia da documentação interativa da API gerada automaticamente pelo Swagger UI, onde é possível realizar os testes de autenticação e das rotas de chat:

![Swagger UI](img-swagger.png)

---

## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as ferramentas mais modernas do ecossistema Python:

* **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alta performance e fácil utilização.
* **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para mapeamento e manipulação do banco de dados.
* **[PostgreSQL](https://www.postgresql.org/)**: Banco de dados relacional robusto para produção.
* **[PyJWT](https://pyjwt.readthedocs.io/)**: Token seguro para autenticação de usuários (JWT).
* **[Passlib (Bcrypt)](https://passlib.readthedocs.io/)**: Criptografia segura para senhas de usuários.
* **Uvicorn**: Servidor ASGI rápido para rodar a aplicação.

---

## 🔒 Arquitetura de Segurança

A API utiliza o protocolo **OAuth2 com HTTPBearer**. O fluxo de segurança funciona da seguinte forma:

1. **Cadastro/Login**: O usuário se autentica enviando e-mail e senha.
2. **Token JWT**: A API valida as credenciais e retorna um Token de Acesso temporário.
3. **Requisições Protegidas**: O usuário insere o token no cabeçalho `Authorization: Bearer <TOKEN>` para acessar rotas privadas (como o chat de nutrição).

---

## 🗺️ Principais Rotas da API

### Autenticação (`/auth`)
* `POST /auth/register` - Cadastra um novo usuário no sistema.
* `POST /auth/login` - Autentica o usuário e retorna o token JWT.

### Chat Inteligente (`/chat`)
* `POST /chat` - Envia uma mensagem para a IA de Nutrição e retorna orientações nutricionais personalizados. *(Requer Token)*

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Instância do PostgreSQL rodando.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/moisesvinicius0101/nutriai-api.git](https://github.com/moisesvinicius0101/nutriai-api.git)
   cd nutriai-api

python -m venv venv
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

DATABASE_URL=postgresql://usuario:senha@localhost:5432/nutriai_db
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

uvicorn app.main:app --reload

