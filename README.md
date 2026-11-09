# Instituto Acesso Legal

Catálogo web de direitos explicados em linguagem simples, organizados por categoria (Trabalho, Moradia etc.), com busca tolerante a acentos.

## Stack

- Python / Django 5
- SQLite (padrão local) ou PostgreSQL (via variáveis de ambiente)
- `python-decouple` para configuração via `.env`
- `Unidecode` para busca tolerante a acentos/erros de digitação

## Estrutura

- `config/` — configurações do projeto Django (settings, urls, wsgi/asgi)
- `catalogo/` — app principal: modelos `Categoria` e `Artigo`, views, templates e comando de seed
- `catalogo/management/commands/seed_demo.py` — popula o banco com categorias e artigos de exemplo

## Como rodar localmente

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e ajuste os valores (por padrão usa SQLite se `DB_ENGINE` não for `postgres`):
   ```bash
   copy .env.example .env
   ```
4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```
5. (Opcional) Popule dados de exemplo:
   ```bash
   python manage.py seed_demo
   ```
6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

No Windows, o atalho `run_server.bat` ativa a venv e já inicia o servidor.

## Funcionalidades

- Listagem de categorias de direitos na home
- Página de categoria com os artigos relacionados
- Página de artigo com conteúdo simplificado
- Busca por título ou palavras-chave, com fallback tolerante a acentos quando a busca direta não encontra resultados
