from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para gerenciamento de pedidos da Raizes do Nordeste.",
)


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
