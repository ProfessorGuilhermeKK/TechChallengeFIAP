# 📚 Books API - Tech Challenge FIAP

API RESTful pública para consulta de livros com sistema de web scraping, autenticação JWT e endpoints preparados para Machine Learning.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do Tech Challenge da FIAP, focado em criar uma infraestrutura completa de extração, transformação e disponibilização de dados via API pública. O objetivo é fornecer dados estruturados de livros para cientistas de dados e serviços de recomendação.

### 🌟 Características Principais

- ✅ **Web Scraping Robusto**: Extração automatizada de dados de https://books.toscrape.com/
- ✅ **API RESTful Completa**: Implementada com FastAPI e documentação Swagger automática
- ✅ **Autenticação JWT**: Sistema de autenticação seguro para endpoints protegidos
- ✅ **ML-Ready**: Endpoints específicos para consumo de modelos de Machine Learning
- ✅ **Monitoramento**: Sistema de logs estruturados em JSON
- ✅ **Documentação Completa**: Swagger UI e ReDoc inclusos

## 📋 Índice

- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação](#-autenticação)
- [Deploy](#-deploy)
- [Machine Learning](#-machine-learning)
- [Exemplos](#-exemplos)
- [Testes](#-testes)
- [Monitoramento](#-monitoramento)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Roadmap Futuro](#-roadmap-futuro)
- [Autores](#-autores)
- [Contribuindo](#-contribuindo)

## 🏗️ Arquitetura

```
┌─────────────────┐
│  Web Scraping   │
│ (books.toscrape)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   CSV Storage   │
│  (data/books)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI App   │
│  (REST API)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────┐   ┌─────┐
│Dados│   │ ML  │
│Users│   │Users│
└─────┘   └─────┘
```

### Pipeline de Dados

1. **Ingestão**: Web scraping extrai dados do site Books to Scrape
2. **Processamento**: Dados são limpos, transformados e salvos em CSV
3. **API**: FastAPI serve os dados através de endpoints RESTful
4. **Consumo**: Cientistas de dados e modelos ML consomem a API

### Componentes do Sistema

```
TECH-CHALLENGE/
├── api/                      # Módulo da API
│   ├── routers/             # Endpoints organizados por domínio
│   │   ├── books.py         # Endpoints de livros
│   │   ├── categories.py    # Endpoints de categorias
│   │   ├── stats.py         # Estatísticas e insights
│   │   ├── health.py        # Health check
│   │   ├── auth.py          # Autenticação JWT
│   │   ├── ml.py            # Endpoints ML-Ready
│   │   └── scraping.py      # Trigger de scraping
│   ├── models.py            # Modelos Pydantic
│   ├── database.py          # Gerenciamento de dados
│   └── auth.py              # Sistema de autenticação
├── scripts/                 # Scripts de automação
│   └── scraper.py          # Web scraper
├── utils/                   # Utilitários
│   └── logger.py           # Sistema de logging
├── data/                    # Armazenamento de dados
│   ├── books.csv           # Dados extraídos
│   └── .gitkeep            # Mantém a pasta versionada
├── logs/                    # Logs da aplicação (.gitkeep mantém a pasta)
├── tests/                   # Testes automatizados
├── main.py                  # Aplicação principal
├── dashboard.py            # Dashboard Streamlit
├── config.py               # Configurações
├── requirements.txt        # Dependências Python
├── run_api.py              # Script para subir a API
├── run_dashboard.py        # Script para subir o dashboard
├── run_scraping.py         # Script para executar o scraping
├── demo_jwt.py             # Demonstração de JWT
├── test_auth.py            # Testes de autenticação
├── API_EXAMPLES.md         # Exemplos de chamadas
├── ARCHITECTURE.md         # Documentação arquitetural
├── Procfile                # Configuração para Heroku
├── render.yaml             # Configuração para Render
├── fly.toml                # Configuração para Fly.io
├── railway.json            # Configuração para Railway
└── vercel.json             # Configuração para Vercel
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/tech-challenge.git
cd tech-challenge
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
API_VERSION=v1
API_TITLE=Books API
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
```

## 💻 Uso

### 1. Executar Web Scraping

Primeiro, extraia os dados do site:

```bash
python run_scraping.py
```

Isso irá:

- Extrair todos os livros de todas as categorias
- Salvar os dados em `data/books.csv`
- Exibir estatísticas dos dados coletados

**Tempo estimado**: 5-10 minutos (depende da conexão)

### 2. Iniciar a API

```bash
python run_api.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### 3. Acessar Documentação

Acesse a documentação interativa:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 📡 Endpoints da API

### Endpoints Core (Obrigatórios)

#### 📚 Livros

| Método | Endpoint                             | Descrição                      |
| ------- | ------------------------------------ | -------------------------------- |
| GET     | `/api/v1/books`                    | Lista todos os livros (paginado) |
| GET     | `/api/v1/books/{id}`               | Detalhes de um livro específico |
| GET     | `/api/v1/books/search/query`       | Busca livros por filtros         |
| GET     | `/api/v1/books/top-rated/list`     | Livros mais bem avaliados        |
| GET     | `/api/v1/books/price-range/filter` | Filtra por faixa de preço       |

#### 🏷️ Categorias

| Método | Endpoint               | Descrição               |
| ------- | ---------------------- | ------------------------- |
| GET     | `/api/v1/categories` | Lista todas as categorias |

#### 💚 Health Check

| Método | Endpoint           | Descrição           |
| ------- | ------------------ | --------------------- |
| GET     | `/api/v1/health` | Status da API e dados |

### Endpoints de Insights (Opcionais)

#### 📊 Estatísticas

| Método | Endpoint                     | Descrição                       |
| ------- | ---------------------------- | --------------------------------- |
| GET     | `/api/v1/stats/overview`   | Estatísticas gerais da coleção |
| GET     | `/api/v1/stats/categories` | Estatísticas por categoria       |

### Endpoints de Autenticação (Bônus)

| Método | Endpoint                 | Descrição               |
| ------- | ------------------------ | ------------------------- |
| POST    | `/api/v1/auth/login`   | Obter token JWT           |
| POST    | `/api/v1/auth/refresh` | Renovar token             |
| GET     | `/api/v1/auth/me`      | Informações do usuário |

### Endpoints ML-Ready (Bônus)

| Método | Endpoint                     | Descrição                    |
| ------- | ---------------------------- | ------------------------------ |
| GET     | `/api/v1/ml/features`      | Features formatadas para ML    |
| GET     | `/api/v1/ml/training-data` | Dataset para treinamento       |
| POST    | `/api/v1/ml/predictions`   | Submeter predições           |
| GET     | `/api/v1/ml/stats`         | Estatísticas para análise ML |

### Endpoints Administrativos (Protegidos)

| Método | Endpoint                     | Descrição      | Autenticação |
| ------- | ---------------------------- | ---------------- | -------------- |
| POST    | `/api/v1/scraping/trigger` | Iniciar scraping | ✅ Requerida   |
| POST    | `/api/v1/scraping/reload`  | Recarregar dados | ✅ Requerida   |

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação.

### Credenciais de Teste

```
Usuário: admin
Senha: secret
```

### Obter Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

Resposta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 30
}
```

### Usar Token

Inclua o token no header `Authorization`:

```bash
curl -X GET "http://localhost:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📦 Deploy

### **Arquivos de Configuração Criados:**

- ✅ `Procfile` - Para Heroku
- ✅ `render.yaml` - Para Render
- ✅ `fly.toml` - Para Fly.io
- ✅ `railway.json` - Para Railway

### **Guia Completo:**

Consulte o arquivo **[GUIA_DEPLOY.md](GUIA_DEPLOY.md)** para instruções detalhadas de deploy em cada plataforma.

### **Deploy Rápido (Render - Recomendado):**

1. Acesse https://render.com
2. Crie conta e conecte GitHub
3. Selecione "New Web Service"
4. Conecte seu repositório
5. Render detectará `render.yaml` automaticamente
6. Adicione variáveis de ambiente:
   - `SECRET_KEY` (gere uma chave aleatória)
   - `ENVIRONMENT=production`
7. Clique em "Create Web Service"
8. Aguarde deploy (2-5 minutos)

**URL da API:** `https://seu-app.onrender.com`

**Documentação:** `https://seu-app.onrender.com/api/v1/docs`

> **Nota:** Após deploy, você pode executar o scraping via API (endpoint protegido) ou fazer upload do arquivo `data/books.csv`.

## 🤖 Machine Learning

A API foi projetada pensando em consumo por modelos de ML.

### Features Disponíveis

- `price_normalized`: Preço normalizado (0-1)
- `rating_normalized`: Rating normalizado (0-1)
- `category_encoded`: Categoria codificada numericamente
- `in_stock`: Disponibilidade (boolean)

### Exemplo de Uso com Python

```python
import requests
import pandas as pd

# Obter features para treinamento
response = requests.get('http://localhost:8000/api/v1/ml/training-data')
data = response.json()

# Converter para DataFrame
df = pd.DataFrame(data['features'])

# Features e target
X = df[['price_normalized', 'rating_normalized', 'category_encoded']]
y = df['rating']  # Exemplo: prever rating

# Treinar modelo
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X, y)
```

### Submeter Predições

```python
predictions = [
    {
        "book_id": 1,
        "prediction": 4.5,
        "confidence": 0.85,
        "model_version": "v1.0"
    }
]

# Requer autenticação
headers = {"Authorization": "Bearer SEU_TOKEN"}
response = requests.post(
    'http://localhost:8000/api/v1/ml/predictions',
    json=predictions,
    headers=headers
)
```

## 📝 Exemplos de Uso

### Listar Todos os Livros

```bash
curl -X GET "http://localhost:8000/api/v1/books?page=1&page_size=10"
```

### Buscar Livros por Título

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?title=Python"
```

### Filtrar por Categoria e Preço

```bash
curl -X GET "http://localhost:8000/api/v1/books/search/query?category=Science&min_price=10&max_price=50"
```

### Obter Estatísticas

```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview"
```

Resposta:

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

### Livros Mais Bem Avaliados

```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated/list?limit=5"
```

## 🧪 Testes

Execute os testes automatizados:

```bash
pytest tests/ -v
```

Com cobertura:

```bash
pytest tests/ --cov=api --cov-report=html
```

## 📊 Monitoramento

### Dashboard Streamlit

Execute o dashboard interativo para visualizar métricas e estatísticas:

```bash
python run_dashboard.py
```

Ou diretamente com Streamlit:

```bash
streamlit run dashboard.py
```

O dashboard estará disponível em: **http://localhost:8501**

**Funcionalidades do Dashboard:**
- ✅ Métricas principais (total de livros, categorias, preços, ratings)
- ✅ Visualizações interativas (gráficos de barras, pizza, scatter)
- ✅ Análise por categoria
- ✅ Análise de preços e ratings
- ✅ Tabela de dados com filtros
- ✅ Download de dados filtrados

### Logs

Os logs são salvos em `logs/api_YYYYMMDD.log` no formato JSON:

```json
{
  "timestamp": "2025-11-02T10:30:00.123Z",
  "level": "INFO",
  "name": "api.routers.books",
  "message": "GET /api/v1/books - Status: 200 - Time: 0.045s"
}
```

### Métricas

Cada resposta inclui o header `X-Process-Time` com o tempo de processamento:

```
X-Process-Time: 0.045
```

## 🎯 Cenários de Uso

### 1. Sistema de Recomendação

```python
# Obter features de livros similares
books = api.get('/ml/features')
similar = recommend_similar_books(user_preferences, books)
```

### 2. Análise de Preços

```python
# Comparar preços por categoria
stats = api.get('/stats/categories')
analyze_price_trends(stats)
```

### 3. Dashboard de Insights

```python
# Criar visualizações
import streamlit as st

overview = api.get('/stats/overview')
st.metric("Total de Livros", overview['total_books'])
st.metric("Preço Médio", f"£{overview['average_price']:.2f}")
```

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Streamlit**: Dashboard interativo para visualização de dados
- **Pandas**: Manipulação e análise de dados
- **BeautifulSoup4**: Web scraping
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **Uvicorn**: Servidor ASGI
- **Python-JSON-Logger**: Logs estruturados
- **Plotly**: Visualizações interativas

## 📈 Roadmap Futuro

- [ ] Integração com banco de dados PostgreSQL
- [ ] Cache com Redis
- [ ] Rate limiting
- [ ] Webhooks para notificações
- [ ] API GraphQL
- [x] Dashboard Streamlit ✅
- [ ] Containerização com Docker
- [ ] CI/CD com GitHub Actions
- [ ] Modelos ML pré-treinados

## 👥 Autores

Este projeto foi desenvolvido por:

- **Bernardo Barro**  
  📧 [bernardo.barro@gmail.com](mailto:bernardo.barro@gmail.com)

- **Carlos Eduardo Araujo Del Isola**  
  📧 [carlos.ed3@hotmail.com](mailto:carlos.ed3@hotmail.com)

- **Guilherme Klein Klug**  
  📧 [guilherme.kleinklug@gmail.com](mailto:guilherme.kleinklug@gmail.com)

- **Henrique Walmir Schuler**  
  📧 [henriquewschuler@gmail.com](mailto:henriquewschuler@gmail.com)

- **Karina Marques de Oliveira**  
  📧 [karinamarquesp@outlook.com.br](mailto:karinamarquesp@outlook.com.br)

---

**Tech Challenge FIAP - 2025**

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
