# API Raizes do Nordeste

API desenvolvida para o trabalho de Back-end, com foco no fluxo principal de pedido,
pagamento mock e atualizacao de status.

## Tecnologias e versoes

- Python 3.13.12
- FastAPI 0.115.6
- Uvicorn 0.34.0
- Pydantic Settings 2.7.1
- SQLAlchemy 2.0.36
- SQLite

## Requisitos para rodar

- Python 3.13 ou superior
- Pip
- Terminal PowerShell no Windows

## Como rodar localmente

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Copie o arquivo de ambiente:

```bash
copy .env.example .env
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

## Banco de dados e seed

Nesta etapa, a API usa SQLite local pelo valor `DATABASE_URL` do `.env`.
Ao iniciar a aplicacao, o banco `raizes_do_nordeste.db` e criado
automaticamente se ainda nao existir.

O seed inicial tambem roda automaticamente na primeira subida e cria:

- 2 unidades
- 3 produtos
- cardapio por unidade com preco e quantidade disponivel

As migrations ainda serao adicionadas em uma etapa futura do trabalho.

## Endpoints iniciais

- `GET /` - informacoes basicas da API
- `GET /health` - verificacao simples de funcionamento
- `GET /unidades` - lista unidades ativas
- `GET /unidades/{id}/cardapio` - lista produtos disponiveis por unidade

## Ordem sugerida para testar a entrega atual

1. Subir a API com `uvicorn app.main:app --reload`
2. Abrir o Swagger em `http://127.0.0.1:8000/docs`
3. Chamar `GET /unidades`
4. Usar um `id` retornado para chamar `GET /unidades/{id}/cardapio`

## Swagger

Com a API rodando, acesse:

```text
http://127.0.0.1:8000/docs
```
