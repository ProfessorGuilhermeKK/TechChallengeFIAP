#!/usr/bin/env python3
"""
Script para executar o dashboard Streamlit
"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    print("=" * 60)
    print("Books API Dashboard - Tech Challenge FIAP")
    print("=" * 60)
    print()
    print("Iniciando dashboard Streamlit...")
    print("Dashboard estará disponível em: http://localhost:8501")
    print()
    print("Pressione CTRL+C para parar")
    print("=" * 60)
    print()
    
    # Executar streamlit
    dashboard_path = Path(__file__).parent / "dashboard.py"
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(dashboard_path),
        "--server.port=8501",
        "--server.address=localhost"
    ])


