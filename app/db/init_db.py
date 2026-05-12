from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import engine
from app.models.catalogo import CardapioUnidade, Produto, Unidade
from app.models.pedido import ItemPedido, Pedido
from app.models.usuario import Usuario


def create_db_and_seed() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        unidade_existente = db.scalar(select(Unidade.id).limit(1))

        if unidade_existente is None:
            unidade_centro = Unidade(
                nome="Raizes do Nordeste - Centro",
                cidade="Curitiba",
                bairro="Centro",
            )
            unidade_batel = Unidade(
                nome="Raizes do Nordeste - Batel",
                cidade="Curitiba",
                bairro="Batel",
            )

            baiao = Produto(
                nome="Baiao de Dois",
                categoria="Prato principal",
                descricao="Arroz, feijao verde, queijo coalho e carne de sol.",
            )
            tapioca = Produto(
                nome="Tapioca de Carne Seca",
                categoria="Lanche",
                descricao="Tapioca recheada com carne seca cremosa.",
            )
            cuscuz = Produto(
                nome="Cuscuz Nordestino",
                categoria="Prato principal",
                descricao="Cuscuz com manteiga de garrafa e ovo.",
            )

            db.add_all(
                [
                    unidade_centro,
                    unidade_batel,
                    baiao,
                    tapioca,
                    cuscuz,
                ]
            )
            db.flush()

            db.add_all(
                [
                    CardapioUnidade(
                        unidade_id=unidade_centro.id,
                        produto_id=baiao.id,
                        preco=32.90,
                        quantidade_disponivel=20,
                    ),
                    CardapioUnidade(
                        unidade_id=unidade_centro.id,
                        produto_id=tapioca.id,
                        preco=18.50,
                        quantidade_disponivel=12,
                    ),
                    CardapioUnidade(
                        unidade_id=unidade_batel.id,
                        produto_id=baiao.id,
                        preco=34.90,
                        quantidade_disponivel=8,
                    ),
                    CardapioUnidade(
                        unidade_id=unidade_batel.id,
                        produto_id=cuscuz.id,
                        preco=21.00,
                        quantidade_disponivel=15,
                    ),
                ]
            )

        usuario_existente = db.scalar(select(Usuario.id).limit(1))
        if usuario_existente is None:
            db.add_all(
                [
                    Usuario(
                        nome="Administrador",
                        email="admin@raizes.com",
                        senha_hash=hash_password("admin123"),
                        perfil="ADMIN",
                    ),
                    Usuario(
                        nome="Cliente Teste",
                        email="cliente@raizes.com",
                        senha_hash=hash_password("cliente123"),
                        perfil="CLIENTE",
                    ),
                ]
            )

        db.commit()
