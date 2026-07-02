# Burger House

Landing page pública e painel administrativo separado para a hamburgueria Burger House.

## Stack

Backend:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT
- Uvicorn

Frontend:
- HTML5
- CSS3
- JavaScript puro
- GitHub Pages

## Estrutura

```text
burger-house/
├── render.yaml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── seed.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   ├── runtime.txt
│   └── .env.example
└── frontend/
    ├── index.html
    ├── admin.html
    ├── css/style.css
    ├── js/config.js
    ├── js/app.js
    ├── js/admin.js
    └── images/
```

## Versão do Python

O backend está fixado para Python 3.11.9 no arquivo:

```text
backend/runtime.txt
```

Conteúdo obrigatório:

```text
python-3.11.9
```

Esse arquivo é importante no Render porque evita que o serviço use Python 3.14.x. O Python 3.14 ainda pode quebrar a instalação de dependências com binários nativos, especialmente `pydantic-core`, resultando em erro de `metadata-generation-failed`.

As dependências em `backend/requirements.txt` foram mantidas em versões compatíveis com Python 3.11:

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
SQLAlchemy==2.0.36
psycopg2-binary==2.9.10
pydantic==2.10.4
pydantic-settings==2.7.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20
email-validator==2.2.0
```

## Rodar Localmente

1. Crie o banco PostgreSQL local:

```sql
CREATE DATABASE burger_house;
CREATE USER burger_user WITH PASSWORD 'burger_password';
GRANT ALL PRIVILEGES ON DATABASE burger_house TO burger_user;
```

2. Entre no backend:

```bash
cd backend
```

3. Crie o arquivo `.env` a partir de `.env.example`:

```env
DATABASE_URL=postgresql://burger_user:burger_password@localhost:5432/burger_house
SECRET_KEY=troque_por_uma_chave_grande_e_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:5500
GITHUB_PAGES_URL=https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO
```

4. Instale dependências:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

5. Rode o seed:

```bash
python -m app.seed
```

O seed é seguro para rodar mais de uma vez. Ele atualiza ou cria categorias, produtos, combos e promoções sem duplicar os exemplos principais.

6. Inicie a API:

```bash
uvicorn app.main:app --reload
```

7. Abra:

```text
API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
```

8. Em outro terminal, sirva o frontend:

```bash
cd frontend
python -m http.server 5500
```

9. Abra:

```text
Landing: http://localhost:5500
Admin: http://localhost:5500/admin.html
```

## Admin Inicial

O seed cria o gerente inicial:

```text
Email: gerente@burgerhouse.com.br
Senha: Burger@123
```

O admin usa:
- `POST /auth/login`
- token JWT salvo em `sessionStorage`
- `Authorization: Bearer SEU_TOKEN` nas rotas protegidas

## Configuração do Frontend

A URL da API e o número do WhatsApp ficam em:

```text
frontend/js/config.js
```

Para produção, troque:

```js
const API_BASE_URL = window.location.hostname.includes("github.io")
  ? "https://SUA-API-RENDER.onrender.com"
  : "http://127.0.0.1:8000";

const WHATSAPP_NUMBER = "5511999999999";
```

Substitua `https://SUA-API-RENDER.onrender.com` pela URL real do backend no Render.

## Deploy do Backend no Render

Opção recomendada: usar o `render.yaml` na raiz do projeto.

1. Suba o projeto para um repositório GitHub.
2. No Render, clique em `New +`.
3. Escolha `Blueprint`.
4. Conecte o repositório.
5. O Render vai ler `render.yaml`.
6. Ele cria:
   - serviço web `burger-house-api`
   - banco PostgreSQL `burger-house-db`

Configuração esperada do serviço web:

```text
Root Directory: backend
Runtime: Python
Python Version: python-3.11.9 via backend/runtime.txt
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Se o Render mostrar Python 3.14.x nos logs de build, confira:

```text
backend/runtime.txt
```

O arquivo precisa estar dentro da pasta `backend/`, porque o serviço usa `Root Directory: backend`.

Variáveis de ambiente no Render:

```text
DATABASE_URL=gerada pelo banco PostgreSQL do Render
SECRET_KEY=crie_uma_chave_grande_e_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
FRONTEND_URL=https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO
GITHUB_PAGES_URL=https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO
```

O backend já corrige automaticamente `postgres://` para `postgresql://`, caso o Render entregue a URL nesse formato.

## Rodar Seed no Render

Depois do primeiro deploy:

1. Abra o serviço `burger-house-api` no Render.
2. Entre em `Shell`.
3. Rode:

```bash
python -m app.seed
```

4. Teste:

```text
https://SUA-API-RENDER.onrender.com/docs
https://SUA-API-RENDER.onrender.com/products
https://SUA-API-RENDER.onrender.com/categories
```

## Deploy do Frontend no GitHub Pages

1. Confirme que `frontend/js/config.js` tem a URL real do Render.
2. Suba o projeto para o GitHub.
3. No GitHub, entre no repositório.
4. Vá em `Settings`.
5. Vá em `Pages`.
6. Em `Build and deployment`, escolha `Deploy from a branch`.
7. Escolha a branch principal.
8. Se o GitHub Pages permitir escolher pasta, publique `frontend`.

Se o GitHub Pages do repositório não permitir publicar a pasta `frontend` diretamente, use uma destas opções:
- mover temporariamente o conteúdo de `frontend` para a raiz da branch de publicação;
- usar GitHub Actions para publicar somente a pasta `frontend`;
- criar uma branch `gh-pages` contendo os arquivos de `frontend`.

URL esperada:

```text
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO/
```

Admin publicado:

```text
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO/admin.html
```

## CORS

O backend aceita:

```text
http://localhost:5500
http://127.0.0.1:5500
http://localhost:3000
http://127.0.0.1:3000
FRONTEND_URL
GITHUB_PAGES_URL
```

Se aparecer erro de CORS:

1. Confira a URL exata do GitHub Pages.
2. Coloque a mesma URL em `FRONTEND_URL` e `GITHUB_PAGES_URL` no Render.
3. Não deixe barra final diferente. Use:

```text
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO
```

4. Faça redeploy do backend.

## Testes Pós-Deploy

Backend:

```text
GET /
GET /docs
GET /products
GET /categories
POST /auth/login
GET /admin/products sem token deve retornar 401/403
GET /admin/products com token deve retornar dados
```

Landing:
- abrir a URL do GitHub Pages;
- conferir se os produtos aparecem;
- filtrar por Lanches, Combos, Acompanhamentos, Bebidas e Sobremesas;
- clicar em WhatsApp e conferir a mensagem;
- conferir produto esgotado com selo `Esgotado`;
- conferir que produto inativo não aparece.

Admin:
- abrir `/admin.html`;
- fazer login com o gerente;
- criar produto;
- editar produto;
- marcar como esgotado;
- desativar produto;
- criar combo;
- criar promoção;
- voltar para a landing e conferir as mudanças.

## Segurança

Para teste gratuito, o projeto já separa landing e admin, usa JWT, PostgreSQL e rotas protegidas.

Antes de produção real:
- trocar `SECRET_KEY`;
- trocar a senha do gerente;
- restringir CORS aos domínios reais;
- usar HTTPS;
- criar política de backup do banco;
- usar storage próprio para imagens;
- adicionar migrations com Alembic;
- revisar logs e permissões do Render.
