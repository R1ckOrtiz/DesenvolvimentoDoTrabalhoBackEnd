from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.errors import ApiError
from app.models.catalogo import CardapioUnidade, Unidade
from app.schemas.catalogo import CardapioItemResponse, UnidadeResponse

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.get("", response_model=list[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)) -> list[Unidade]:
    return list(
        db.scalars(
            select(Unidade)
            .where(Unidade.ativa.is_(True))
            .order_by(Unidade.nome)
        )
    )


@router.get(
    "/{unidade_id}/cardapio",
    response_model=list[CardapioItemResponse],
    responses={404: {"description": "Unidade nao encontrada"}},
)
def listar_cardapio_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
) -> list[CardapioItemResponse]:
    unidade = db.get(Unidade, unidade_id)
    if unidade is None or not unidade.ativa:
        raise ApiError(
            status_code=404,
            error_code="UNIDADE_NAO_ENCONTRADA",
            message="Unidade nao encontrada.",
        )

    itens = db.scalars(
        select(CardapioUnidade)
        .where(CardapioUnidade.unidade_id == unidade_id)
        .order_by(CardapioUnidade.id)
    ).all()

    return [
        CardapioItemResponse(
            produto_id=item.produto_id,
            nome=item.produto.nome,
            categoria=item.produto.categoria,
            descricao=item.produto.descricao,
            preco=item.preco,
            quantidade_disponivel=item.quantidade_disponivel,
            disponivel=item.disponivel,
        )
        for item in itens
    ]
