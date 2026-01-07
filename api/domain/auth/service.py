from __future__ import annotations

from datetime import timedelta
from typing import Dict, Any

from api.core.auth import authenticate_user, create_access_token
from api.core.config import get_settings
from api.domain.auth.schemas import User
from api.domain.common.exceptions import InvalidCredentialsError

settings = get_settings()


class AuthService:
    def login(self, username: str, password: str) -> Dict[str, Any]:
        user = authenticate_user(username, password)
        if not user:
            raise InvalidCredentialsError("Incorrect username or password")

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes,
        }

    def refresh(self, current_user: User) -> Dict[str, Any]:
        # Mantém o comportamento atual: refresh só funciona se o user estiver autenticado. :contentReference[oaicite:1]{index=1}
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": current_user.username},
            expires_delta=access_token_expires,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes,
        }
