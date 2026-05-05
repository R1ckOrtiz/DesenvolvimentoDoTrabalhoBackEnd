from pydantic import BaseModel, ConfigDict


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    cidade: str
    bairro: str
    ativa: bool

    model_config = ConfigDict(from_attributes=True)


class CardapioItemResponse(BaseModel):
    produto_id: int
    nome: str
    categoria: str
    descricao: str
    preco: float
    quantidade_disponivel: int
    disponivel: bool
