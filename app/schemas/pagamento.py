from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pedido import StatusPagamento


class PagamentoMockRequest(BaseModel):
    pedido_id: int = Field(..., gt=0, alias="pedidoId")
    aprovado: bool = Field(..., description="Define se o mock aprova ou recusa.")

    model_config = ConfigDict(populate_by_name=True)


class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int = Field(alias="pedidoId")
    status: StatusPagamento
    valor: float
    codigo_transacao: str = Field(alias="codigoTransacao")
    mensagem: str
    criado_em: datetime = Field(alias="criadoEm")
    status_pedido: str = Field(alias="statusPedido")

    model_config = ConfigDict(populate_by_name=True)
