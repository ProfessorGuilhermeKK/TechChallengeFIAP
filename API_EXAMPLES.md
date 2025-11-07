# 📡 Exemplos de Chamadas à API

Este documento contém exemplos práticos de todas as chamadas disponíveis na Books API.

## 🔗 Base URL

```
Local: http://localhost:8000
Produção: configure o domínio conforme a plataforma escolhida (ex.: Render, Railway, Fly.io)
```

## 📋 Índice

- [Health Check](#health-check)
- [Livros](#livros)
- [Categorias](#categorias)
- [Estatísticas](#estatísticas)
- [Autenticação](#autenticação)
- [Machine Learning](#machine-learning)
- [Admin (Scraping)](#admin-scraping)

---

## Health Check

### Verificar Status da API

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

**Resposta:**
```json
{
  "status": "healthy",
  "version": "v1",
  "timestamp": "2025-11-02T10:30:00.123456",
  "data_available": true,
  "total_books": 1000,
  "message": null
}
```

---

## Livros

### 1. Listar Todos os Livros (Paginado)

```bash
curl -X GET "http://localhost:8000/api/v1/books?page=1&page_size=10"
```

**Parâmetros:**
- `page` (opcional): Número da página (padrão: 1)
- `page_size` (opcional): Itens por página (padrão: 50, máx: 100)

**Resposta:**
```json
{
  "total": 1000,
  "page": 1,
  "page_size": 10,
  "books": [
    {
      "id": 1,
      "title": "A Light in the Attic",
      "price": 51.77,
      "price_text": "£51.77",
      "rating": 3,
      "in_stock": true,
      "quantity": 22,
      "availability_text": "In stock (22 available)",
      "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
      "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
      "category": "Poetry"
    }
  ]
}
```

### 2. Obter Livro por ID

```bash
curl -X GET "http://localhost:8000/api/v1/books/1"
```

**Resposta:**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "price_text": "£51.77",
  "rating": 3,
  "in_stock": true,
  "quantity": 22,
  "availability_text": "In stock (22 available)",
  "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
  "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "category": "Poetry"
}
```

**Erro (404):**
```json
{
  "detail": "Book with ID 9999 not found"
}
```

### 3. Buscar Livros

#### Por Título

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?title=Python"
```

#### Por Categoria

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?category=Science"
```

#### Por Título e Categoria

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?title=Python&category=Programming"
```

#### Com Filtros de Preço

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?min_price=10&max_price=50"
```

#### Com Rating Mínimo

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?min_rating=4"
```

#### Apenas Livros em Estoque

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?in_stock=true"
```

#### Busca Complexa

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?title=love&category=Fiction&min_price=15&max_price=30&min_rating=3&in_stock=true&page=1&page_size=20"
```

**Resposta:**
```json
{
  "total": 15,
  "page": 1,
  "page_size": 20,
  "books": [...]
}
```

### 4. Livros Mais Bem Avaliados

```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated/list?limit=10"
```

**Parâmetros:**
- `limit` (opcional): Número de livros (padrão: 10, máx: 100)

**Resposta:**
```json
[
  {
    "id": 234,
    "title": "The Great Book",
    "rating": 5,
    "price": 45.99,
    ...
  }
]
```

### 5. Filtrar por Faixa de Preço

```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range/filter?min=10&max=30"
```

**Parâmetros:**
- `min` (obrigatório): Preço mínimo
- `max` (obrigatório): Preço máximo
- `page` (opcional): Número da página
- `page_size` (opcional): Itens por página

**Resposta:**
```json
{
  "total": 345,
  "page": 1,
  "page_size": 50,
  "books": [...]
}
```

---

## Categorias

### Listar Todas as Categorias

```bash
curl -X GET "http://localhost:8000/api/v1/categories"
```

**Resposta:**
```json
{
  "total": 50,
  "categories": [
    {
      "name": "Fiction",
      "total_books": 65
    },
    {
      "name": "Science",
      "total_books": 42
    },
    {
      "name": "Poetry",
      "total_books": 28
    }
  ]
}
```

---

## Estatísticas

### 1. Visão Geral (Overview)

```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview"
```

**Resposta:**
```json
{
  "total_books": 1000,
  "total_categories": 50,
  "average_price": 35.67,
  "min_price": 10.00,
  "max_price": 59.99,
  "average_rating": 3.8,
  "books_in_stock": 892,
  "books_out_of_stock": 108,
  "rating_distribution": {
    "1": 50,
    "2": 100,
    "3": 250,
    "4": 350,
    "5": 250
  }
}
```

### 2. Estatísticas por Categoria

```bash
curl -X GET "http://localhost:8000/api/v1/stats/categories"
```

**Resposta:**
```json
[
  {
    "category": "Fiction",
    "total_books": 65,
    "average_price": 32.45,
    "min_price": 12.99,
    "max_price": 55.00,
    "average_rating": 3.9,
    "books_in_stock": 58
  },
  {
    "category": "Science",
    "total_books": 42,
    "average_price": 41.23,
    "min_price": 18.50,
    "max_price": 59.99,
    "average_rating": 4.1,
    "books_in_stock": 38
  }
]
```

---

## Autenticação

### 1. Login (Obter Token)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

**Credenciais de Teste:**
- Username: `admin` | Password: `secret`
- Username: `testuser` | Password: `secret`

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYzMDQ4MDAwMH0.xyz...",
  "token_type": "bearer",
  "expires_in": 30
}
```

**Erro (401):**
```json
{
  "detail": "Incorrect username or password"
}
```

### 2. Renovar Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 30
}
```

### 3. Informações do Usuário

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "username": "admin",
  "email": "admin@booksapi.com",
  "full_name": "Admin User",
  "disabled": false
}
```

---

## Machine Learning

### 1. Obter Features para ML

```bash
curl -X GET "http://localhost:8000/api/v1/ml/features"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "category": "Poetry",
    "in_stock": true,
    "price_normalized": 0.834,
    "rating_normalized": 0.6,
    "category_encoded": 12
  }
]
```

### 2. Dataset para Treinamento

```bash
curl -X GET "http://localhost:8000/api/v1/ml/training-data"
```

**Resposta:**
```json
{
  "features": [...],
  "metadata": {
    "total_samples": 1000,
    "total_categories": 50,
    "feature_columns": [
      "price_normalized",
      "rating_normalized",
      "category_encoded",
      "in_stock"
    ],
    "description": "Dataset de livros para treinamento de modelos de recomendação"
  }
}
```

### 3. Submeter Predições

**⚠️ Requer autenticação**

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predictions" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "book_id": 1,
      "prediction": 4.5,
      "confidence": 0.85,
      "model_version": "v1.0"
    },
    {
      "book_id": 2,
      "prediction": 3.8,
      "confidence": 0.72,
      "model_version": "v1.0"
    }
  ]'
```

**Resposta:**
```json
[
  {
    "book_id": 1,
    "prediction": 4.5,
    "confidence": 0.85,
    "model_version": "v1.0"
  },
  {
    "book_id": 2,
    "prediction": 3.8,
    "confidence": 0.72,
    "model_version": "v1.0"
  }
]
```

### 4. Estatísticas ML

```bash
curl -X GET "http://localhost:8000/api/v1/ml/stats"
```

**Resposta:**
```json
{
  "dataset_size": 1000,
  "num_categories": 50,
  "price_distribution": {
    "min": 10.00,
    "q1": 25.50,
    "median": 35.67,
    "q3": 45.80,
    "max": 59.99,
    "mean": 35.67
  },
  "rating_distribution": {
    "1": 50,
    "2": 100,
    "3": 250,
    "4": 350,
    "5": 250
  },
  "stock_balance": {
    "in_stock": 892,
    "out_of_stock": 108,
    "in_stock_percentage": 89.2
  },
  "category_distribution": [
    {"category": "Fiction", "count": 65},
    {"category": "Science", "count": 42}
  ]
}
```

---

## Admin (Scraping)

**⚠️ Todos os endpoints desta seção requerem autenticação**

### 1. Iniciar Scraping

```bash
curl -X POST "http://localhost:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Scraping task started in background",
  "triggered_by": "admin"
}
```

### 2. Recarregar Dados

```bash
curl -X POST "http://localhost:8000/api/v1/scraping/reload" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Data reloaded successfully",
  "total_books": 1000
}
```

---

## 🐍 Exemplos com Python

### Instalação

```bash
pip install requests
```

### Exemplo Básico

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Listar livros
response = requests.get(f"{BASE_URL}/books", params={"page": 1, "page_size": 10})
books = response.json()

print(f"Total de livros: {books['total']}")
for book in books['books']:
    print(f"- {book['title']} (£{book['price']})")
```

### Busca Avançada

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Buscar livros de ficção entre £10 e £30
params = {
    "category": "Fiction",
    "min_price": 10,
    "max_price": 30,
    "min_rating": 3,
    "in_stock": True,
    "page": 1,
    "page_size": 20
}

response = requests.get(f"{BASE_URL}/books/search/query", params=params)
results = response.json()

print(f"Encontrados {results['total']} livros")
```

### Autenticação e Uso de Token

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
login_data = {
    "username": "admin",
    "password": "secret"
}
response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
token = response.json()["access_token"]

# 2. Usar token em requisição protegida
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/scraping/reload", headers=headers)
print(response.json())
```

### Machine Learning - Features

```python
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

BASE_URL = "http://localhost:8000/api/v1"

# 1. Obter dados de treinamento
response = requests.get(f"{BASE_URL}/ml/training-data")
data = response.json()

# 2. Converter para DataFrame
df = pd.DataFrame(data['features'])

# 3. Preparar features e target
X = df[['price_normalized', 'rating_normalized', 'category_encoded']]
y = df['rating']

# 4. Treinar modelo
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

print(f"Modelo treinado com {len(df)} amostras")
print(f"Score: {model.score(X, y):.2f}")
```

---

## 🔧 Testando com HTTPie

HTTPie é uma alternativa mais amigável ao curl.

### Instalação

```bash
pip install httpie
```

### Exemplos

```bash
# GET simples
http GET localhost:8000/api/v1/books page==1 page_size==5

# POST com JSON
http POST localhost:8000/api/v1/auth/login username=admin password=secret

# Com autenticação
http GET localhost:8000/api/v1/scraping/reload "Authorization: Bearer TOKEN"

# Busca com parâmetros
http GET localhost:8000/api/v1/books/search/query title==Python category==Programming
```

---

## 📊 Códigos de Status HTTP

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| 200 | OK | Requisição bem-sucedida |
| 404 | Not Found | Recurso não encontrado |
| 401 | Unauthorized | Token inválido ou ausente |
| 400 | Bad Request | Parâmetros inválidos |
| 422 | Unprocessable Entity | Validação falhou |
| 500 | Internal Server Error | Erro no servidor |
| 503 | Service Unavailable | Dados não disponíveis |

---

## 🎯 Dicas de Uso

### 1. Paginação Eficiente

```bash
# Iterar por todas as páginas
for i in {1..10}; do
  curl "http://localhost:8000/api/v1/books?page=$i&page_size=100"
done
```

### 2. Salvar Resposta em Arquivo

```bash
curl -X GET "http://localhost:8000/api/v1/books" \
  -o books.json
```

### 3. Pretty Print JSON

```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview" | python -m json.tool
```

### 4. Medir Tempo de Resposta

```bash
curl -w "\nTempo total: %{time_total}s\n" \
  -X GET "http://localhost:8000/api/v1/books"
```

---

## 🐛 Troubleshooting

### Erro: Data not available

```json
{
  "detail": "Data not available. Please run scraping first."
}
```

**Solução:** Execute o scraping primeiro:
```bash
python run_scraping.py
```

### Erro: 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

**Solução:** Obtenha um novo token:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=admin&password=secret"
```

### Erro: 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error"
    }
  ]
}
```

**Solução:** Verifique os parâmetros da requisição.

---

## 📚 Recursos Adicionais

- **Documentação Interativa**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

---

**Última atualização**: 2025-11-02  
**Versão da API**: v1



