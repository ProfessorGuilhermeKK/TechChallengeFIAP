"""
Script para testar autenticação JWT
"""
import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 70)
print("TESTE DE AUTENTICAÇÃO JWT")
print("=" * 70)

# Testar login
print("\n1️⃣ Testando login...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "admin", "password": "secret"},
        timeout=5
    )
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print("   ✅ Login realizado com SUCESSO!")
        print(f"   🔑 Token obtido: {token[:50]}...")
        print(f"   ⏱️  Expira em: {token_data.get('expires_in')} minutos")
        
        # Testar endpoint protegido
        print("\n2️⃣ Testando endpoint protegido com token...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BASE_URL}/scraping/trigger",
            headers=headers,
            timeout=5
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Endpoint protegido acessado com SUCESSO!")
            print(f"   📝 Resposta: {response.json()}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   📝 Resposta: {response.text}")
            
    else:
        print(f"   ❌ Login FALHOU!")
        print(f"   📝 Resposta: {response.text}")
        print("\n💡 Verifique:")
        print("   - Username: 'admin' (exatamente assim)")
        print("   - Password: 'secret' (exatamente assim)")
        print("   - API está rodando? (python run_api.py)")
        
except requests.exceptions.ConnectionError:
    print("   ❌ ERRO: Não foi possível conectar à API!")
    print("   💡 Certifique-se de que a API está rodando:")
    print("      python run_api.py")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Erro inesperado: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("TESTE CONCLUÍDO")
print("=" * 70)



