"""
Modelos Pydantic para validação de dados da API
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


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


class Category(BaseModel):
    """Modelo de categoria"""
    name: str = Field(..., description="Nome da categoria")
    total_books: int = Field(..., description="Total de livros na categoria")


class CategoryList(BaseModel):
    """Resposta com lista de categorias"""
    total: int = Field(..., description="Total de categorias")
    categories: List[Category] = Field(..., description="Lista de categorias")


class HealthCheck(BaseModel):
    """Status de saúde da API"""
    status: str = Field(..., description="Status da API")
    version: str = Field(..., description="Versão da API")
    timestamp: datetime = Field(..., description="Timestamp da verificação")
    data_available: bool = Field(..., description="Se os dados estão disponíveis")
    total_books: int = Field(default=0, description="Total de livros disponíveis")
    message: Optional[str] = Field(None, description="Mensagem adicional")


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


class MLFeatures(BaseModel):
    """Features preparadas para Machine Learning"""
    id: int
    title: str
    price: float
    rating: int
    category: str
    in_stock: bool
    # Features numéricas
    price_normalized: float = Field(..., description="Preço normalizado")
    rating_normalized: float = Field(..., description="Rating normalizado")
    # Features categóricas (one-hot encoding seria aplicado no modelo)
    category_encoded: int = Field(..., description="Categoria codificada")


class MLTrainingData(BaseModel):
    """Dados formatados para treinamento de modelos ML"""
    features: List[MLFeatures]
    metadata: dict = Field(..., description="Metadados do dataset")


class MLPrediction(BaseModel):
    """Predição de um modelo ML"""
    book_id: int = Field(..., description="ID do livro")
    prediction: float = Field(..., description="Valor da predição")
    confidence: Optional[float] = Field(None, description="Confiança da predição")
    model_version: Optional[str] = Field(None, description="Versão do modelo usado")


class ErrorResponse(BaseModel):
    """Resposta de erro padrão"""
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem do erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais")





