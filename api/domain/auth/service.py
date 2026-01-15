from __future__ import annotations

from datetime import timedelta
from typing import Dict, Any

from api.core.auth import authenticate_user, create_access_token, create_refresh_token, decode_token, get_user
from api.core.config import get_settings
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
        
        refresh_token = create_refresh_token(data={"sub": user.username})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes,
            "refresh_expires_in": settings.refresh_token_expire_days * 24 * 60,
        }

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise InvalidCredentialsError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise InvalidCredentialsError("Invalid token type")

        username = payload.get("sub")
        if not username:
            raise InvalidCredentialsError("Invalid refresh token payload")

        user = get_user(username)
        if not user or user.disabled:
            raise InvalidCredentialsError("User not found or inactive")

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        new_access_token = create_access_token(
            data={"sub": username},
            expires_delta=access_token_expires,
        )

        new_refresh_token = create_refresh_token(data={"sub": username})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes,
            "refresh_expires_in": settings.refresh_token_expire_days * 24 * 60,
        }

