from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.errors import ApiError
from app.core.security import create_access_token, verify_password
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={401: {"description": "Credenciais invalidas"}},
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    usuario = db.scalar(select(Usuario).where(Usuario.email == payload.email))

    if (
        usuario is None
        or not usuario.ativo
        or not verify_password(payload.senha, usuario.senha_hash)
    ):
        raise ApiError(
            status_code=401,
            error_code="CREDENCIAIS_INVALIDAS",
            message="E-mail ou senha invalidos.",
        )

    settings = get_settings()
    return TokenResponse(
        access_token=create_access_token(usuario.id, usuario.perfil),
        expires_in_minutes=settings.access_token_expire_minutes,
        perfil=usuario.perfil,
    )
