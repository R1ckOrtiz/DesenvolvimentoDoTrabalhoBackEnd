# API Raizes do Nordeste

API desenvolvida para o trabalho de Back-end, com foco no fluxo principal de pedido,
pagamento mock e atualizacao de status.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Pydantic Settings

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

## Endpoints iniciais

- `GET /` - informacoes basicas da API
- `GET /health` - verificacao simples de funcionamento

## Swagger

Com a API rodando, acesse:

```text
http://127.0.0.1:8000/docs
```
