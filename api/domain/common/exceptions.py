from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    """Resposta de erro padrão"""
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem do erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais")
    

class DomainError(Exception):
    """Base para erros de domínio (não-HTTP)."""


class DataNotAvailableError(DomainError):
    """CSV não carregado / scraping não rodou ainda."""


class NotFoundError(DomainError):
    """Recurso não encontrado."""


class InvalidInputError(DomainError):
    """Entrada inválida (ex.: min_price > max_price)."""


class AuthError(DomainError):
    """Erro de autenticação (credenciais/token)."""


class ForbiddenError(AuthError):
    """Autenticado, mas sem permissão."""


class InvalidCredentialsError(AuthError):
    pass