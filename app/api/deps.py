from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.usuario import Usuario

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None:
        raise ApiError(
            status_code=401,
            error_code="NAO_AUTENTICADO",
            message="Token de autenticacao ausente.",
        )

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise ApiError(
            status_code=401,
            error_code="TOKEN_INVALIDO",
            message="Token de autenticacao invalido ou expirado.",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise ApiError(
            status_code=401,
            error_code="TOKEN_INVALIDO",
            message="Token de autenticacao invalido ou expirado.",
        )

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ApiError(
            status_code=401,
            error_code="TOKEN_INVALIDO",
            message="Token de autenticacao invalido ou expirado.",
        ) from None

    usuario = db.get(Usuario, user_id_int)
    if usuario is None or not usuario.ativo:
        raise ApiError(
            status_code=401,
            error_code="USUARIO_INATIVO",
            message="Usuario nao encontrado ou inativo.",
        )

    return usuario


def require_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    if usuario.perfil != "ADMIN":
        raise ApiError(
            status_code=403,
            error_code="ACESSO_NEGADO",
            message="Usuario sem permissao para acessar este recurso.",
        )

    return usuario
