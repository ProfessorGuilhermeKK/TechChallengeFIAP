"""
Endpoints de autenticação JWT
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.core.auth import get_current_active_user
from api.domain.auth.schemas import Token, User
from api.domain.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Autentica usuário e retorna token JWT"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(AuthService),
):
    return service.login(form_data.username, form_data.password)


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh Token",
    description="Renova o token JWT do usuário autenticado"
)
async def refresh_token(
    current_user: User = Depends(get_current_active_user),
    service: AuthService = Depends(AuthService),
):
    return service.refresh(current_user)
