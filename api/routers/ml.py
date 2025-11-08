"""
Endpoints para Machine Learning
"""
from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List
from api.models import MLFeatures, MLTrainingData, MLPrediction, User
from api.database import get_database
from api.auth import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ml",
    tags=["machine-learning"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/features",
    response_model=List[MLFeatures],
    summary="Features para ML",
    description="Retorna dados formatados como features para modelos de Machine Learning"
)
async def get_ml_features():
    """Retorna features preparadas para ML"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    features = db.get_ml_features()
    return features


@router.get(
    "/training-data",
    response_model=MLTrainingData,
    summary="Dataset para treinamento",
    description="Retorna dataset completo formatado para treinamento de modelos ML"
)
async def get_training_data():
    """Retorna dataset para treinamento"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    features = db.get_ml_features()
    stats = db.get_stats_overview()
    
    metadata = {
        "total_samples": len(features),
        "total_categories": stats.get("total_categories", 0),
        "feature_columns": [
            "price_normalized",
            "rating_normalized",
            "category_encoded",
            "in_stock"
        ],
        "description": "Dataset de livros para treinamento de modelos de recomendação"
    }
    
    return {
        "features": features,
        "metadata": metadata
    }


@router.post(
    "/predictions",
    response_model=List[MLPrediction],
    summary="Receber predições",
    description="Endpoint para receber predições de modelos ML (protegido por autenticação)",
    dependencies=[Depends(get_current_active_user)]
)
async def submit_predictions(
    predictions: List[MLPrediction] = Body(
        ...,
        example=[
            {
                "book_id": 1,
                "prediction": 4.5,
                "confidence": 0.85,
                "model_version": "v1.0"
            }
        ]
    )
):
    """
    Recebe predições de modelos ML
    
    Este endpoint é protegido e requer autenticação JWT.
    Pode ser usado para armazenar predições de modelos de recomendação.
    """
    logger.info(f"Received {len(predictions)} predictions")
    
    # Em produção, aqui você salvaria as predições em um banco de dados
    # Por enquanto, apenas retornamos as predições recebidas
    
    return predictions


@router.get(
    "/stats",
    summary="Estatísticas ML",
    description="Retorna estatísticas úteis para análise de dados e ML"
)
async def get_ml_stats():
    """Retorna estatísticas úteis para ML"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    stats = db.get_stats_overview()
    categories = db.get_all_categories()
    
    # Calcular distribuição de preços
    import pandas as pd
    df = db.df
    
    price_quartiles = df['price'].quantile([0.25, 0.5, 0.75]).to_dict()
    
    ml_stats = {
        "dataset_size": stats.get("total_books", 0),
        "num_categories": len(categories),
        "price_distribution": {
            "min": stats.get("min_price", 0),
            "q1": price_quartiles.get(0.25, 0),
            "median": price_quartiles.get(0.5, 0),
            "q3": price_quartiles.get(0.75, 0),
            "max": stats.get("max_price", 0),
            "mean": stats.get("average_price", 0)
        },
        "rating_distribution": stats.get("rating_distribution", {}),
        "stock_balance": {
            "in_stock": stats.get("books_in_stock", 0),
            "out_of_stock": stats.get("books_out_of_stock", 0),
            "in_stock_percentage": round(
                (stats.get("books_in_stock", 0) / stats.get("total_books", 1)) * 100, 2
            )
        },
        "category_distribution": [
            {"category": cat["category"], "count": cat["total_books"]}
            for cat in categories
        ]
    }
    
    return ml_stats





