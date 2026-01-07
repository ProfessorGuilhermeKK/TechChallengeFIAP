import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.domain.common.exceptions import (
    DataNotAvailableError,
    NotFoundError,
    InvalidInputError,
    AuthError,
    ForbiddenError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DataNotAvailableError)
    async def handle_data_not_available(_: Request, exc: DataNotAvailableError):
        return JSONResponse(status_code=503, content={"error": "data_unavailable", "message": str(exc)})

    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": "not_found", "message": str(exc)})

    @app.exception_handler(InvalidInputError)
    async def handle_invalid_input(_: Request, exc: InvalidInputError):
        return JSONResponse(status_code=400, content={"error": "invalid_input", "message": str(exc)})

    @app.exception_handler(ForbiddenError)
    async def handle_forbidden(_: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content={"error": "forbidden", "message": str(exc)})

    @app.exception_handler(AuthError)
    async def handle_auth(_: Request, exc: AuthError):
        return JSONResponse(status_code=401, content={"error": "unauthorized", "message": str(exc)})

    # Erros do próprio FastAPI (ex.: validação do body/query)
    @app.exception_handler(RequestValidationError)
    async def handle_validation(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": "validation_error", "message": "Invalid request", "detail": exc.errors()},
        )

    # Se algum controller ainda levantar HTTPException (ou libs levantarem)
    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"error": "http_error", "message": exc.detail})

    # Fallback (não vaza detalhes em produção)
    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception):
        logger.exception("Unhandled error", exc_info=exc)
        return JSONResponse(status_code=500, content={"error": "internal_error", "message": "Unexpected error"})
