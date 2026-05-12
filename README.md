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
- 1 usuario administrador
- 1 usuario cliente

As migrations ainda serao adicionadas em uma etapa futura do trabalho.

## Usuarios de teste

| Perfil | E-mail | Senha |
| --- | --- | --- |
| ADMIN | `admin@raizes.com` | `admin123` |
| CLIENTE | `cliente@raizes.com` | `cliente123` |

## Endpoints iniciais

- `GET /` - informacoes basicas da API
- `GET /health` - verificacao simples de funcionamento
- `POST /auth/login` - autentica usuario e retorna token Bearer
- `GET /usuarios/me` - consulta usuario autenticado
- `GET /usuarios/admin-check` - valida acesso exclusivo de administrador
- `GET /unidades` - lista unidades ativas
- `GET /unidades/{id}/cardapio` - lista produtos disponiveis por unidade
- `POST /pedidos` - cria pedido autenticado com itens
- `GET /pedidos` - lista pedidos, com filtro opcional por `canalPedido`
- `GET /pedidos/{id}` - consulta pedido pelo identificador

## Pedido e canalPedido

O campo `canalPedido` registra a origem operacional do pedido. Ele e um dado
de dominio porque afeta analise de atendimento, operacao da unidade e futuras
regras por canal.

Valores aceitos:

- `APP`
- `TOTEM`
- `BALCAO`
- `PICKUP`
- `WEB`

Status atual documentado:

- `CRIADO` - pedido registrado e aguardando proxima etapa do fluxo.

## Ordem sugerida para testar a entrega atual

1. Subir a API com `uvicorn app.main:app --reload`
2. Abrir o Swagger em `http://127.0.0.1:8000/docs`
3. Chamar `POST /auth/login` com o usuario administrador
4. Copiar o `access_token` retornado e usar no botao `Authorize`
5. Chamar `GET /usuarios/me`
6. Chamar `GET /usuarios/admin-check`
7. Chamar `GET /unidades`
8. Usar um `id` retornado para chamar `GET /unidades/{id}/cardapio`
9. Criar um pedido em `POST /pedidos`
10. Consultar o pedido criado em `GET /pedidos/{id}`
11. Listar pedidos por canal em `GET /pedidos?canalPedido=APP`

Exemplo de corpo para login:

```json
{
  "email": "admin@raizes.com",
  "senha": "admin123"
}
```

Exemplo de corpo para criar pedido:

```json
{
  "unidadeId": 1,
  "canalPedido": "APP",
  "itens": [
    {
      "produtoId": 1,
      "quantidade": 1
    }
  ]
}
```

## Swagger

Com a API rodando, acesse:

```text
http://127.0.0.1:8000/docs
```
