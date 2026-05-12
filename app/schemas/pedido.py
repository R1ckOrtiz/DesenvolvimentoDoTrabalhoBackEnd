from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pedido import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int = Field(..., gt=0, alias="produtoId")
    quantidade: int = Field(..., gt=0)

    model_config = ConfigDict(populate_by_name=True)


class PedidoCreate(BaseModel):
    unidade_id: int = Field(..., gt=0, alias="unidadeId")
    canal_pedido: CanalPedido = Field(..., alias="canalPedido")
    itens: list[ItemPedidoCreate] = Field(..., min_length=1)

    model_config = ConfigDict(populate_by_name=True)


class ItemPedidoResponse(BaseModel):
    produto_id: int = Field(alias="produtoId")
    nome: str
    quantidade: int
    preco_unitario: float = Field(alias="precoUnitario")
    subtotal: float

    model_config = ConfigDict(populate_by_name=True)


class PedidoResponse(BaseModel):
    id: int
    usuario_id: int = Field(alias="usuarioId")
    unidade_id: int = Field(alias="unidadeId")
    canal_pedido: CanalPedido = Field(alias="canalPedido")
    status: StatusPedido
    valor_total: float = Field(alias="valorTotal")
    criado_em: datetime = Field(alias="criadoEm")
    itens: list[ItemPedidoResponse]

    model_config = ConfigDict(populate_by_name=True)
