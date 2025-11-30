"""
Script de demonstração de autenticação JWT
Demonstra endpoints públicos vs protegidos
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(num, text):
    """Imprime passo numerado"""
    print(f"\n{num}️⃣ {text}")
    print("-" * 70)

def main():
    print_header("DEMONSTRAÇÃO DE AUTENTICAÇÃO JWT - Books API")
    
    # 1. Testar endpoint público (sem autenticação)
    print_step("1", "Testando endpoint PÚBLICO (sem token)")
    try:
        response = requests.get(f"{BASE_URL}/books?limit=1", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ✅ Endpoint público funciona sem autenticação!")
        if response.status_code == 200:
            data = response.json()
            print(f"   📚 Total de livros retornados: {len(data.get('books', []))}")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERRO: API não está rodando!")
        print("   💡 Execute: python run_api.py")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 2. Testar endpoint protegido SEM token
    print_step("2", "Testando endpoint PROTEGIDO (sem token)")
    response = requests.post(f"{BASE_URL}/scraping/trigger")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✅ Bloqueado corretamente! (esperado)")
        error_detail = response.json().get("detail", "Not authenticated")
        print(f"   📝 Mensagem: {error_detail}")
    else:
        print(f"   ⚠️  Status inesperado: {response.status_code}")
    
    # 3. Obter token JWT
    print_step("3", "Obtendo token JWT (fazendo login)")
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": "admin", "password": "secret"},
            timeout=5
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data["access_token"]
            print(f"   ✅ Login realizado com sucesso!")
            print(f"   🔑 Token obtido (primeiros 50 chars): {token[:50]}...")
            print(f"   ⏱️  Token expira em: {token_data.get('expires_in', 'N/A')} minutos")
        else:
            print(f"   ❌ Erro no login: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ Erro ao fazer login: {e}")
        sys.exit(1)
    
    # 4. Testar endpoint protegido COM token
    print_step("4", "Testando endpoint PROTEGIDO (com token)")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/scraping/trigger",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Funcionou! Endpoint protegido acessado com sucesso!")
        result = response.json()
        print(f"   📝 Resposta:")
        print(f"      - Status: {result.get('status')}")
        print(f"      - Mensagem: {result.get('message')}")
        print(f"      - Usuário: {result.get('triggered_by')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
        print(f"   Resposta: {response.text}")
    
    # 5. Obter informações do usuário autenticado
    print_step("5", "Obtendo informações do usuário autenticado")
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   ✅ Informações do usuário obtidas!")
        print(f"   👤 Usuário: {user_data.get('username')}")
        print(f"   📧 Email: {user_data.get('email')}")
        print(f"   👨‍💼 Nome: {user_data.get('full_name')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # 6. Testar renovação de token
    print_step("6", "Renovando token JWT")
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        new_token_data = response.json()
        new_token = new_token_data["access_token"]
        print(f"   ✅ Token renovado com sucesso!")
        print(f"   🔑 Novo token (primeiros 50 chars): {new_token[:50]}...")
    else:
        print(f"   ❌ Erro: {response.status_code}")
    
    # 7. Testar endpoint de ML protegido
    print_step("7", "Testando endpoint ML protegido (POST /ml/predictions)")
    prediction_data = [
        {
            "book_id": 1,
            "prediction": 4.5,
            "confidence": 0.85,
            "model_version": "v1.0"
        }
    ]
    response = requests.post(
        f"{BASE_URL}/ml/predictions",
        headers={**headers, "Content-Type": "application/json"},
        json=prediction_data,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Predições enviadas com sucesso!")
        print(f"   📊 Predições retornadas: {len(response.json())}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
        print(f"   Resposta: {response.text}")
    
    # Resumo final
    print_header("RESUMO DA DEMONSTRAÇÃO")
    print("""
    ✅ Endpoints PÚBLICOS funcionam sem autenticação
    ✅ Endpoints PROTEGIDOS bloqueiam acesso sem token (401)
    ✅ Login retorna token JWT válido
    ✅ Endpoints PROTEGIDOS funcionam com token (200)
    ✅ Token pode ser renovado
    ✅ Informações do usuário podem ser obtidas
    
    📋 Endpoints Protegidos:
       - POST /api/v1/auth/refresh
       - GET  /api/v1/auth/me
       - POST /api/v1/scraping/trigger
       - POST /api/v1/scraping/reload
       - POST /api/v1/ml/predictions
    
    📋 Endpoints Públicos:
       - GET  /api/v1/books
       - GET  /api/v1/books/{id}
       - GET  /api/v1/books/search
       - GET  /api/v1/categories
       - GET  /api/v1/health
       - GET  /api/v1/stats/overview
       - GET  /api/v1/ml/features
       - GET  /api/v1/ml/training-data
    """)
    
    print_header("DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO! 🎉")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstração interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)

