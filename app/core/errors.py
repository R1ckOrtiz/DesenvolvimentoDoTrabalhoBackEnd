from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiError(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "erro": error_code,
                "mensagem": message,
                "status_code": status_code,
                "detalhes": details,
            },
        )


async def api_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and {"erro", "mensagem", "status_code"} <= set(exc.detail):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": "ERRO_HTTP",
            "mensagem": str(exc.detail),
            "status_code": exc.status_code,
            "detalhes": None,
        },
    )


async def validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "erro": "ERRO_VALIDACAO",
            "mensagem": "Dados de entrada invalidos.",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detalhes": exc.errors(),
        },
    )
