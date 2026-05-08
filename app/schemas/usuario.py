from pydantic import BaseModel, ConfigDict


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
