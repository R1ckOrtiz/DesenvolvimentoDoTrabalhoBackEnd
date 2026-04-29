from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cidade: Mapped[str] = mapped_column(String(80), nullable=False)
    bairro: Mapped[str] = mapped_column(String(80), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cardapio: Mapped[list["CardapioUnidade"]] = relationship(
        back_populates="unidade",
        cascade="all, delete-orphan",
    )


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    categoria: Mapped[str] = mapped_column(String(80), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    unidades: Mapped[list["CardapioUnidade"]] = relationship(back_populates="produto")


class CardapioUnidade(Base):
    __tablename__ = "cardapio_unidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    quantidade_disponivel: Mapped[int] = mapped_column(Integer, nullable=False)
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    unidade: Mapped[Unidade] = relationship(back_populates="cardapio")
    produto: Mapped[Produto] = relationship(back_populates="unidades")
