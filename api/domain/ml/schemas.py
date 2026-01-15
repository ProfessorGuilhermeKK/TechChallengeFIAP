from pydantic import BaseModel, Field
from typing import Optional, List


class MLFeatures(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    category: str
    in_stock: bool

    price_normalized: float = Field(..., description="Preço normalizado")
    rating_normalized: float = Field(..., description="Rating normalizado")
    category_encoded: int = Field(..., description="Categoria codificada")


class MLTrainingData(BaseModel):
    features: List[MLFeatures]
    metadata: dict = Field(..., description="Metadados do dataset")


class MLPrediction(BaseModel):
    book_id: int = Field(..., description="ID do livro")
    prediction: float = Field(..., description="Valor da predição")
    confidence: Optional[float] = Field(None, description="Confiança da predição")
    model_version: Optional[str] = Field(None, description="Versão do modelo usado")
