from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HealthCheck(BaseModel):
    """Status de saúde da API"""
    status: str = Field(..., description="Status da API")
    version: str = Field(..., description="Versão da API")
    timestamp: datetime = Field(..., description="Timestamp da verificação")
    data_available: bool = Field(..., description="Se os dados estão disponíveis")
    total_books: int = Field(default=0, description="Total de livros disponíveis")
    message: Optional[str] = Field(None, description="Mensagem adicional")