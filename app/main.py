from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.routes.auth import router as auth_router
from app.api.routes.pagamentos import router as pagamentos_router
from app.api.routes.pedidos import router as pedidos_router
from app.api.routes.unidades import router as unidades_router
from app.api.routes.usuarios import router as usuarios_router
from app.core.config import get_settings
from app.core.errors import api_error_handler, validation_error_handler
from app.db.init_db import create_db_and_seed

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_seed()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para gerenciamento de pedidos da Raizes do Nordeste.",
    lifespan=lifespan,
)
app.add_exception_handler(HTTPException, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.include_router(auth_router)
app.include_router(unidades_router)
app.include_router(pedidos_router)
app.include_router(pagamentos_router)
app.include_router(usuarios_router)


@app.get("/", tags=["Sistema"])
def read_root() -> dict[str, str]:
    return {
        "nome": settings.app_name,
        "versao": settings.app_version,
        "ambiente": settings.environment,
    }


@app.get("/health", tags=["Sistema"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
