from pydantic import BaseModel, Field


class StatsOverview(BaseModel):
    """Estatísticas gerais da coleção"""
    total_books: int = Field(..., description="Total de livros")
    total_categories: int = Field(..., description="Total de categorias")
    average_price: float = Field(..., description="Preço médio")
    min_price: float = Field(..., description="Preço mínimo")
    max_price: float = Field(..., description="Preço máximo")
    average_rating: float = Field(..., description="Rating médio")
    books_in_stock: int = Field(..., description="Livros em estoque")
    books_out_of_stock: int = Field(..., description="Livros fora de estoque")
    rating_distribution: dict = Field(..., description="Distribuição de ratings")


class CategoryStats(BaseModel):
    """Estatísticas de uma categoria"""
    category: str = Field(..., description="Nome da categoria")
    total_books: int = Field(..., description="Total de livros")
    average_price: float = Field(..., description="Preço médio")
    min_price: float = Field(..., description="Preço mínimo")
    max_price: float = Field(..., description="Preço máximo")
    average_rating: float = Field(..., description="Rating médio")
    books_in_stock: int = Field(..., description="Livros em estoque")
