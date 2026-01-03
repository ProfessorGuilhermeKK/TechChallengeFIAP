"""
Vercel serverless function entry point
"""
from main import app

# Vercel espera uma variável 'app' ou 'application'
# FastAPI app já está definido em main.py
__all__ = ['app']






