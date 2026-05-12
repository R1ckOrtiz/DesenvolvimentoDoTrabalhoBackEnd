from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.errors import ApiError
from app.models.catalogo import CardapioUnidade, Unidade
from app.models.pedido import CanalPedido, ItemPedido, Pedido, StatusPedido
from app.models.usuario import Usuario
from app.schemas.pedido import ItemPedidoResponse, PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def _pedido_response(pedido: Pedido) -> PedidoResponse:
    return PedidoResponse(
        id=pedido.id,
        usuario_id=pedido.usuario_id,
        unidade_id=pedido.unidade_id,
        canal_pedido=CanalPedido(pedido.canal_pedido),
        status=StatusPedido(pedido.status),
        valor_total=pedido.valor_total,
        criado_em=pedido.criado_em,
        itens=[
            ItemPedidoResponse(
                produto_id=item.produto_id,
                nome=item.produto.nome,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                subtotal=item.subtotal,
            )
            for item in pedido.itens
        ],
    )


def _validar_acesso_ao_pedido(pedido: Pedido, usuario: Usuario) -> None:
    if usuario.perfil != "ADMIN" and pedido.usuario_id != usuario.id:
        raise ApiError(
            status_code=403,
            error_code="ACESSO_NEGADO",
            message="Usuario sem permissao para acessar este pedido.",
        )


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "Token ausente ou invalido"},
        404: {"description": "Unidade ou produto nao encontrado"},
        409: {"description": "Produto indisponivel"},
    },
)
def criar_pedido(
    payload: PedidoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PedidoResponse:
    unidade = db.get(Unidade, payload.unidade_id)
    if unidade is None or not unidade.ativa:
        raise ApiError(
            status_code=404,
            error_code="UNIDADE_NAO_ENCONTRADA",
            message="Unidade nao encontrada.",
        )

    quantidades_por_produto: dict[int, int] = {}
    for item in payload.itens:
        quantidades_por_produto[item.produto_id] = (
            quantidades_por_produto.get(item.produto_id, 0) + item.quantidade
        )

    itens_cardapio: list[tuple[CardapioUnidade, int]] = []
    for produto_id, quantidade in quantidades_por_produto.items():
        item_cardapio = db.scalar(
            select(CardapioUnidade).where(
                CardapioUnidade.unidade_id == payload.unidade_id,
                CardapioUnidade.produto_id == produto_id,
            )
        )

        if item_cardapio is None or not item_cardapio.produto.ativo:
            raise ApiError(
                status_code=404,
                error_code="PRODUTO_NAO_ENCONTRADO",
                message="Produto nao encontrado no cardapio da unidade.",
            )

        if (
            not item_cardapio.disponivel
            or item_cardapio.quantidade_disponivel < quantidade
        ):
            raise ApiError(
                status_code=409,
                error_code="PRODUTO_INDISPONIVEL",
                message="Produto sem quantidade disponivel para o pedido.",
                details={
                    "produtoId": produto_id,
                    "quantidadeDisponivel": item_cardapio.quantidade_disponivel,
                },
            )

        itens_cardapio.append((item_cardapio, quantidade))

    pedido = Pedido(
        usuario_id=usuario.id,
        unidade_id=payload.unidade_id,
        canal_pedido=payload.canal_pedido.value,
        status=StatusPedido.CRIADO.value,
        valor_total=0,
    )
    db.add(pedido)
    db.flush()

    valor_total = 0.0
    for item_cardapio, quantidade in itens_cardapio:
        subtotal = round(item_cardapio.preco * quantidade, 2)
        valor_total = round(valor_total + subtotal, 2)
        item_cardapio.quantidade_disponivel -= quantidade
        if item_cardapio.quantidade_disponivel == 0:
            item_cardapio.disponivel = False

        pedido.itens.append(
            ItemPedido(
                produto_id=item_cardapio.produto_id,
                quantidade=quantidade,
                preco_unitario=item_cardapio.preco,
                subtotal=subtotal,
            )
        )

    pedido.valor_total = valor_total
    db.commit()
    db.refresh(pedido)

    return _pedido_response(pedido)


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(
    canal_pedido: CanalPedido | None = Query(default=None, alias="canalPedido"),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PedidoResponse]:
    consulta = select(Pedido).order_by(Pedido.id.desc())

    if usuario.perfil != "ADMIN":
        consulta = consulta.where(Pedido.usuario_id == usuario.id)

    if canal_pedido is not None:
        consulta = consulta.where(Pedido.canal_pedido == canal_pedido.value)

    pedidos = db.scalars(consulta).all()
    return [_pedido_response(pedido) for pedido in pedidos]


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
    responses={
        403: {"description": "Usuario sem permissao para acessar este pedido"},
        404: {"description": "Pedido nao encontrado"},
    },
)
def consultar_pedido(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PedidoResponse:
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise ApiError(
            status_code=404,
            error_code="PEDIDO_NAO_ENCONTRADO",
            message="Pedido nao encontrado.",
        )

    _validar_acesso_ao_pedido(pedido, usuario)
    return _pedido_response(pedido)
