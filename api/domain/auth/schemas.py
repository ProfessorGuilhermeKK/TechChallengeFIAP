from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    """Token de autenticação JWT"""
    access_token: str = Field(..., description="Token de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em minutos")


class TokenData(BaseModel):
    """Dados extraídos do token"""
    username: Optional[str] = None


class User(BaseModel):
    """Usuário do sistema"""
    username: str = Field(..., description="Nome de usuário")
    email: Optional[str] = Field(None, description="Email do usuário")
    full_name: Optional[str] = Field(None, description="Nome completo")
    disabled: Optional[bool] = Field(False, description="Se o usuário está desabilitado")


class UserInDB(User):
    """Usuário armazenado no banco de dados"""
    hashed_password: str
