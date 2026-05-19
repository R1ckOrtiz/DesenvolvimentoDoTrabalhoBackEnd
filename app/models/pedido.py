from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CanalPedido(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    PAGAMENTO_APROVADO = "PAGAMENTO_APROVADO"
    PAGAMENTO_RECUSADO = "PAGAMENTO_RECUSADO"
    CANCELADO = "CANCELADO"


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), nullable=False)
    canal_pedido: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(30),
        default=StatusPedido.CRIADO.value,
        nullable=False,
    )
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
    )
    pagamentos: Mapped[list["Pagamento"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped[Pedido] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship()


class StatusPagamento(str, Enum):
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    codigo_transacao: Mapped[str] = mapped_column(String(80), nullable=False)
    mensagem: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    pedido: Mapped[Pedido] = relationship(back_populates="pagamentos")
