from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.errors import ApiError
from app.models.pedido import Pagamento, Pedido, StatusPagamento, StatusPedido
from app.models.usuario import Usuario
from app.schemas.pagamento import PagamentoMockRequest, PagamentoResponse

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def _pagamento_response(pagamento: Pagamento) -> PagamentoResponse:
    return PagamentoResponse(
        id=pagamento.id,
        pedido_id=pagamento.pedido_id,
        status=StatusPagamento(pagamento.status),
        valor=pagamento.valor,
        codigo_transacao=pagamento.codigo_transacao,
        mensagem=pagamento.mensagem,
        criado_em=pagamento.criado_em,
        status_pedido=pagamento.pedido.status,
    )


def _validar_acesso_ao_pedido(pedido: Pedido, usuario: Usuario) -> None:
    if usuario.perfil != "ADMIN" and pedido.usuario_id != usuario.id:
        raise ApiError(
            status_code=403,
            error_code="ACESSO_NEGADO",
            message="Usuario sem permissao para pagar este pedido.",
        )


@router.post(
    "/mock",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "Token ausente ou invalido"},
        403: {"description": "Usuario sem permissao para pagar o pedido"},
        404: {"description": "Pedido nao encontrado"},
        409: {"description": "Pedido ja possui pagamento"},
    },
)
def registrar_pagamento_mock(
    payload: PagamentoMockRequest,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PagamentoResponse:
    pedido = db.get(Pedido, payload.pedido_id)
    if pedido is None:
        raise ApiError(
            status_code=404,
            error_code="PEDIDO_NAO_ENCONTRADO",
            message="Pedido nao encontrado.",
        )

    _validar_acesso_ao_pedido(pedido, usuario)

    pagamento_existente = db.scalar(
        select(Pagamento).where(Pagamento.pedido_id == payload.pedido_id)
    )
    if pagamento_existente is not None:
        raise ApiError(
            status_code=409,
            error_code="PAGAMENTO_JA_REGISTRADO",
            message="Pedido ja possui pagamento registrado.",
        )

    status_pagamento = (
        StatusPagamento.APROVADO if payload.aprovado else StatusPagamento.RECUSADO
    )
    pedido.status = (
        StatusPedido.PAGAMENTO_APROVADO.value
        if payload.aprovado
        else StatusPedido.PAGAMENTO_RECUSADO.value
    )

    pagamento = Pagamento(
        pedido_id=pedido.id,
        status=status_pagamento.value,
        valor=pedido.valor_total,
        codigo_transacao=f"MOCK-{uuid4().hex[:12].upper()}",
        mensagem=(
            "Pagamento mock aprovado."
            if payload.aprovado
            else "Pagamento mock recusado."
        ),
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return _pagamento_response(pagamento)
