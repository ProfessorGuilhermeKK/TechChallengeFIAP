"""
Testes básicos da API
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Testa rota raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Testa health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "data_available" in data


def test_login():
    """Testa login"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_login_invalid():
    """Testa login com credenciais inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401





