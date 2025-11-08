"""
Endpoints de autenticação JWT
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from api.models import Token, User
from api.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)
from config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint de login - retorna token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes
    }


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh Token",
    description="Renova o token JWT do usuário autenticado"
)
async def refresh_token(current_user: User = Depends(get_current_active_user)):
    """Renova o token JWT"""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes
    }


@router.get(
    "/me",
    response_model=User,
    summary="Get Current User",
    description="Retorna informações do usuário autenticado"
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retorna informações do usuário atual"""
    return current_user





