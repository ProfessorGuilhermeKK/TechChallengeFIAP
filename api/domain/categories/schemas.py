from pydantic import BaseModel, Field
from typing import List


class Category(BaseModel):
    """Modelo de categoria"""
    name: str = Field(..., description="Nome da categoria")
    total_books: int = Field(..., description="Total de livros na categoria")


class CategoryList(BaseModel):
    """Resposta com lista de categorias"""
    total: int = Field(..., description="Total de categorias")
    categories: List[Category] = Field(..., description="Lista de categorias")
