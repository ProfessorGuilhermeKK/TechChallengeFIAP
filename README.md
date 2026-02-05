# Books API - Tech Challenge FIAP

API RESTful pública para consulta de livros com sistema de web scraping, autenticação JWT e endpoints preparados para Machine Learning.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Links Importantes

- **API em Produção:** [https://techchallengefiap-1.onrender.com](https://techchallengefiap-1.onrender.com)
- **Dashboard Streamlit:** [https://techchallengefiap-inxmwiezovxzpqct9cprge.streamlit.app](https://techchallengefiap-inxmwiezovxzpqct9cprge.streamlit.app)
- **Documentação Swagger:** [https://techchallengefiap-1.onrender.com/api/v1/docs](https://techchallengefiap-1.onrender.com/api/v1/docs)
- **Vídeo de Apresentação:** [https://www.youtube.com/watch?v=dH2-AEd1Zm8](https://www.youtube.com/watch?v=dH2-AEd1Zm8)

## Sobre o Projeto

Este projeto foi desenvolvido como parte do Tech Challenge da FIAP, focado em criar uma infraestrutura completa de extração, transformação e disponibilização de dados via API pública. O objetivo é fornecer dados estruturados de livros para cientistas de dados e serviços de recomendação.

### Características Principais

- **Web Scraping Robusto**: Extração automatizada de dados de https://books.toscrape.com/
- **API RESTful Completa**: Implementada com FastAPI e documentação Swagger automática
- **Autenticação JWT**: Sistema de autenticação seguro para endpoints protegidos
- **ML-Ready**: Endpoints específicos para consumo de modelos de Machine Learning
- **Dashboard Interativo**: Visualização de dados com Streamlit
- **Monitoramento**: Sistema de logs estruturados em JSON
- **Deploy em Produção**: API e Dashboard deployados e funcionais
- **Documentação Completa**: Swagger UI e ReDoc inclusos

## Índice

- [Links Importantes](#links-importantes)
- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints da API](#endpoints-da-api)
- [Autenticação](#autenticação)
- [Machine Learning](#machine-learning)
- [Exemplos de Uso](#exemplos-de-uso)
- [Monitoramento](#monitoramento)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Roadmap Futuro](#roadmap-futuro)
- [Autores](#autores)
- [Certificações Google Cloud](#certificações-google-cloud)

## Arquitetura do Sistema

O sistema segue uma arquitetura modular e escalável. Para visualizar o diagrama completo da arquitetura, consulte o arquivo **[arquitetura.jfif](./arquitetura.jfif)** na raiz do repositório.

### Componentes Principais:

1. **Web Scraping Layer**
   - Extração de dados de books.toscrape.com
   - BeautifulSoup4 para parsing HTML
   - Armazenamento em CSV

2. **Data Processing Layer**
   - Pandas para manipulação de dados
   - Transformação e limpeza
   - Validação com Pydantic

3. **API Layer (FastAPI)**
   - Endpoints de Books
   - Sistema de Autenticação JWT
   - Endpoints ML-Ready
   - Documentação Swagger automática

4. **Visualization & Consumption**
   - Dashboard Streamlit interativo
   - Swagger UI para testes
   - Preparado para integração com modelos ML

### Cenários de Uso:
- Cientistas de dados consumindo features para treinar modelos
- Sistemas de recomendação obtendo dados de livros
- Análise de preços e tendências de mercado
- Dashboard gerencial para insights de negócio

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/henriquewschuler/TechChallengeFIAP.git
cd TechChallengeFIAP
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

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
API_VERSION=v1
API_TITLE=Books API
HOST=0.0.0.0
PORT=8000

# IMPORTANTE: Altere em produção!
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development

# Usuários de autenticação (formato: username:password:fullname:email)
# IMPORTANTE: Altere as senhas padrão em produção!
AUTH_USERS=admin:secret:Admin User:admin@booksapi.com,testuser:secret:Test User:test@booksapi.com
```

> **Dica de Segurança:** Gere uma chave secreta forte:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

## Uso

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

## Variáveis de Ambiente

Para documentação completa sobre variáveis de ambiente, consulte [ENV_VARS.md](ENV_VARS.md).

**Variáveis principais:**
- `SECRET_KEY` - Chave secreta JWT (obrigatório alterar em produção)
- `AUTH_USERS` - Lista de usuários autorizados (formato: `user:pass:name:email`)
- `ENVIRONMENT` - Ambiente de execução (`development`, `production`)
- `DATA_PATH` - Caminho do arquivo CSV de dados

## Endpoints da API

### Endpoints Core (Obrigatórios)

#### Livros

| Método | Endpoint                       | Descrição                        |
| ------- | ------------------------------ | -------------------------------- |
| GET     | `/api/v1/books`                | Lista todos os livros (paginado) |
| GET     | `/api/v1/books/{id}`           | Detalhes de um livro específico  |
| GET     | `/api/v1/books/search`         | Busca livros por filtros         |
| GET     | `/api/v1/books/top-rated`      | Livros mais bem avaliados        |
| GET     | `/api/v1/books/price-range`    | Filtra por faixa de preço        |

#### Categorias

| Método | Endpoint               | Descrição               |
| ------- | ---------------------- | ------------------------- |
| GET     | `/api/v1/categories` | Lista todas as categorias |

#### Health Check

| Método | Endpoint           | Descrição           |
| ------- | ------------------ | --------------------- |
| GET     | `/api/v1/health` | Status da API e dados |

#### Métricas (Prometheus)

| Método | Endpoint      | Descrição                                |
| ------- | ------------- | ------------------------------------------ |
| GET     | `/metrics`  | Métricas Prometheus para monitoramento |

> **Nota:** O endpoint `/metrics` expõe métricas no formato Prometheus, incluindo informações sobre requisições HTTP, latência, e outras métricas de performance da aplicação.

### Endpoints de Insights (Opcionais)

#### Estatísticas

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

| Método | Endpoint                     | Descrição                    | Status |
| ------- | ---------------------------- | ------------------------------ | -------- |
| GET     | `/api/v1/ml/features`      | Features formatadas para ML    | Implementado |
| GET     | `/api/v1/ml/training-data` | Dataset para treinamento       | Implementado |
| POST    | `/api/v1/ml/predictions`   | Submeter predições           | Mockado* |
| GET     | `/api/v1/ml/stats`         | Estatísticas para análise ML | Implementado |

**\* Nota sobre /predictions:** Este endpoint está implementado com dados mockados para demonstração. Ele recebe predições e as retorna como confirmação. A integração real com modelos de ML será implementada em fases futuras do projeto.

### Endpoints Administrativos (Protegidos)

| Método | Endpoint                     | Descrição      | Autenticação |
| ------- | ---------------------------- | ---------------- | -------------- |
| POST    | `/api/v1/scraping/trigger` | Iniciar scraping | Requerida   |
| POST    | `/api/v1/scraping/reload`  | Recarregar dados | Requerida   |

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação.

### Credenciais de Teste

> **Importante:** As credenciais padrão devem ser configuradas via variáveis de ambiente em produção.

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

## Machine Learning

A API foi projetada pensando em consumo por modelos de ML.

> **Status de Implementação:**
> - **Endpoints de Features e Training Data:** Totalmente implementados e funcionais
> - **Endpoint de Predictions:** Implementado com dados mockados para demonstração
> - **Próximos Passos:** Integração com modelos de ML reais (recomendação, classificação, previsão de preços)

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

### Submeter Predições (Mockado)

> **Importante:** Este endpoint atualmente retorna os dados mockados enviados como confirmação. A integração com modelos de ML reais será implementada nas próximas fases do projeto.

```python
# Exemplo de uso do endpoint /predictions
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

# Response (mockado - retorna o que foi enviado)
print(response.json())  # Retorna a lista de predições enviada
```

**Implementação Futura:**
- Integração com modelos de recomendação (Collaborative Filtering, Content-Based)
- Pipeline de predição de ratings
- Sistema de cache para predições frequentes
- Versionamento de modelos

## Exemplos de Uso

### Listar Todos os Livros

```bash
curl -X GET "http://localhost:8000/api/v1/books?page=1&page_size=10"
```

### Buscar Livros por Título

```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=Python"
```

### Filtrar por Categoria e Preço

```bash
curl -X GET "http://localhost:8000/api/v1/books/search?category=Science&min_price=10&max_price=50"
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
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=5"
```

## Monitoramento

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
- Métricas principais (total de livros, categorias, preços, ratings)
- Visualizações interativas (gráficos de barras, pizza, scatter)
- Análise por categoria
- Análise de preços e ratings
- Tabela de dados com filtros
- Download de dados filtrados

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

## Cenários de Uso

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

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Streamlit**: Dashboard interativo para visualização de dados
- **Pandas**: Manipulação e análise de dados
- **BeautifulSoup4**: Web scraping
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **Uvicorn**: Servidor ASGI
- **Python-JSON-Logger**: Logs estruturados
- **Plotly**: Visualizações interativas

## Roadmap Futuro

- Integração com banco de dados PostgreSQL
- Cache com Redis
- Rate limiting
- Webhooks para notificações
- API GraphQL
- Dashboard Streamlit (Concluído)
- Containerização com Docker
- CI/CD com GitHub Actions
- Modelos ML pré-treinados

## Autores

Este projeto foi desenvolvido por:

- **Bernardo Barro**
  - Email: bernardo.barro@gmail.com

- **Carlos Eduardo Araujo Del Isola**
  - Email: carlos.ed3@hotmail.com

- **Guilherme Klein Klug**
  - Email: guilherme.kleinklug@gmail.com

- **Henrique Walmir Schuler**
  - Email: henriquewschuler@gmail.com

- **Karina Marques de Oliveira**
  - Email: karinamarquesp@outlook.com.br

## Certificações Google Cloud

Como parte do Tech Challenge, os integrantes concluíram o curso **"Beginner: Introduction to Generative AI Learning Path"** da Google Cloud Skills Boost.

### Perfis Públicos com Certificações:

**Guilherme Klein Klug**
- Perfil: [https://www.skills.google/public_profiles/11c43c9b-f2f9-4541-9dd9-3014d33eb482](https://www.skills.google/public_profiles/11c43c9b-f2f9-4541-9dd9-3014d33eb482)
- Pontuação: 478 points - Silver League

**Badges conquistadas:**
- Introduction to Generative AI
- Introduction to Large Language Models
- Introduction to Responsible AI
- Prompt Design in Vertex AI
- Responsible AI: Applying AI Principles with Google Cloud

---

**Bernardo Barro**
- Perfil: [https://www.skills.google/public_profiles/2f3f83c2-b22d-4c6e-9866-f935221f3903](https://www.skills.google/public_profiles/2f3f83c2-b22d-4c6e-9866-f935221f3903)
- Pontuação: 468 points - Silver League

**Badges conquistadas:**
- Introduction to Generative AI
- Introduction to Large Language Models
- Introduction to Responsible AI
- Prompt Design in Vertex AI
- Responsible AI: Applying AI Principles with Google Cloud

---

**Carlos Eduardo Araujo Del Isola**
- Perfil: [https://www.skills.google/public_profiles/ec0d4b51-5b19-4a23-82de-680dae201a7f](https://www.skills.google/public_profiles/ec0d4b51-5b19-4a23-82de-680dae201a7f)
- Pontuação: 1363 points - Silver League

**Badges conquistadas:**
- Introduction to Generative AI
- Introduction to Large Language Models
- Introduction to Responsible AI
- Prompt Design in Vertex AI
- Responsible AI: Applying AI Principles with Google Cloud
