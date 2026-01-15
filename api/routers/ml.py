from fastapi import APIRouter, Depends, Body
from typing import List

from api.core.auth import get_current_active_user

from api.core.deps import get_ml_service
from api.domain.ml.schemas import MLFeatures, MLPrediction, MLTrainingData
from api.domain.ml.service import MLService
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
async def get_ml_features(
    service: MLService = Depends(get_ml_service),
):
    return service.get_features()


@router.get(
    "/training-data",
    response_model=MLTrainingData,
    summary="Dataset para treinamento",
    description="Retorna dataset completo formatado para treinamento de modelos ML"
)
async def get_training_data(
    service: MLService = Depends(get_ml_service),
):
    return service.get_training_data()


@router.post(
    "/predictions",
    response_model=List[MLPrediction],
    summary="Receber predições (MOCKADO)",
    description="""
    ⚠️ **ENDPOINT MOCKADO** - Demonstração de funcionalidade futura
    
    Este endpoint está implementado com dados mockados para demonstração da API.
    Atualmente, ele recebe predições de modelos de ML e as retorna como confirmação.
    
    **Implementação Futura:**
    - Armazenamento de predições em banco de dados
    - Validação de predições contra dados reais
    - Métricas de performance de modelos
    - Versionamento de modelos
    - Sistema de cache
    
    **Autenticação:** Requerida (Bearer Token)
    """,
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
    ),
    service: MLService = Depends(get_ml_service),
):
    return service.submit_predictions(predictions)


@router.get(
    "/stats",
    summary="Estatísticas ML",
    description="Retorna estatísticas úteis para análise de dados e ML"
)
async def get_ml_stats(
    service: MLService = Depends(get_ml_service),
):
    return service.get_ml_stats()
