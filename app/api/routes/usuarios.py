from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_admin
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/me", response_model=UsuarioResponse)
def consultar_usuario_logado(
    usuario: Usuario = Depends(get_current_user),
) -> Usuario:
    return usuario


@router.get("/admin-check")
def validar_acesso_admin(_: Usuario = Depends(require_admin)) -> dict[str, str]:
    return {"status": "acesso_admin_confirmado"}
