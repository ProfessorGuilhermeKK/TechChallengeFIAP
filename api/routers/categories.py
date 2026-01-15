from fastapi import APIRouter, Depends
import logging

from api.core.deps import get_categories_service
from api.domain.categories.schemas import CategoryList
from api.domain.categories.service import CategoriesService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=CategoryList,
    summary="Lista todas as categorias",
    description="Retorna lista de todas as categorias de livros disponíveis com contagem"
)
async def get_all_categories(
    service: CategoriesService = Depends(get_categories_service),
):
    return service.list_categories()
