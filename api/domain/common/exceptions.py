from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem do erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais")
    
    
class DomainError(Exception):
    pass


class DataNotAvailableError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class InvalidInputError(DomainError):
    pass


class AuthError(DomainError):
    pass


class ForbiddenError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass