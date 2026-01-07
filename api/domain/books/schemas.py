from pydantic import BaseModel, Field, ConfigDict
from typing import List


class Book(BaseModel):
    """Modelo de um livro"""
    id: int = Field(..., description="ID único do livro")
    title: str = Field(..., description="Título do livro")
    price: float = Field(..., description="Preço do livro em libras")
    price_text: str = Field(..., description="Preço formatado como texto")
    rating: int = Field(..., ge=0, le=5, description="Rating de 0 a 5 estrelas")
    in_stock: bool = Field(..., description="Se o livro está em estoque")
    quantity: int = Field(..., ge=0, description="Quantidade disponível")
    availability_text: str = Field(..., description="Texto de disponibilidade")
    image_url: str = Field(..., description="URL da imagem do livro")
    book_url: str = Field(..., description="URL da página do livro")
    category: str = Field(..., description="Categoria do livro")

    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    """Resposta com lista de livros"""
    total: int = Field(..., description="Total de livros")
    page: int = Field(default=1, description="Página atual")
    page_size: int = Field(default=50, description="Tamanho da página")
    books: List[Book] = Field(..., description="Lista de livros")
