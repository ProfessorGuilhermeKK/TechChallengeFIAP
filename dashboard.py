import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from api.core.auth import authenticate_user
from api.infra.storage.database import get_database

st.set_page_config(
    page_title="Books API Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_password():
    VALID_CREDENTIALS = {
        "admin": "secret",
        "testuser": "secret"
    }
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Tela de login
        st.title("🔐 Login - Books API Dashboard")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.subheader("Acesso ao Dashboard")
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                submitted = st.form_submit_button("🚀 Entrar", width='stretch')
                
                if submitted:
                    if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
                        st.info("💡 Credenciais padrão: `admin` / `secret`")
        
        st.markdown("---")
        st.info("💡 **Credenciais de teste:**\n- Usuário: `admin`\n- Senha: `secret`")
        st.stop()
    
    return True

check_password()

def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Tela de login
        st.title("🔐 Login - Books API Dashboard")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.subheader("Acesso ao Dashboard")
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
                
                if submitted:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
                        st.info("💡 Credenciais padrão: `admin` / `secret`")
        
        st.markdown("---")
        st.info("💡 **Credenciais de teste:**\n- Usuário: `admin`\n- Senha: `secret`")
        st.stop()
    
    return True

check_password()

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    /* Estilizar cards de métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }
    div[data-testid="stMetricContainer"] {
        background-color: #f8f9fa !important;
        padding: 1.5rem !important;
        border-radius: 0.75rem !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15) !important;
        border: 2px solid #dee2e6 !important;
        margin: 0.5rem 0 !important;
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid #5a67d8 !important;
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        border: 2px solid #e91e63 !important;
    }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: 2px solid #0288d1 !important;
    }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
        border: 2px solid #00c853 !important;
    }
    div[data-testid="stMetricContainer"] [data-testid="stMetricValue"],
    div[data-testid="stMetricContainer"] [data-testid="stMetricLabel"],
    div[data-testid="stMetricContainer"] [data-testid="stMetricDelta"] {
        color: white !important;
    }
    [data-testid="stMetricValue"] {
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📚 Books API Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    try:
        db = get_database()
        if db.is_available():
            return db.df, db.get_stats_overview(), db.get_category_stats()
        else:
            return None, None, None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

df, stats, category_stats = load_data()

with st.sidebar:
    st.header("⚙️ Configurações")
    
    if 'username' in st.session_state:
        st.success(f"👤 Logado como: **{st.session_state.username}**")
    
    if st.button("🚪 Logout", width='stretch', type="secondary"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Atualizar Dados", width='stretch'):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.header("ℹ️ Informações")
    if stats:
        st.success("✅ Dados carregados com sucesso")
        st.info(f"📊 Total de livros: {stats['total_books']}")
        st.info(f"📁 Total de categorias: {stats['total_categories']}")
    else:
        st.error("❌ Dados não disponíveis")
        st.warning("Execute o scraping primeiro: `python run_scraping.py`")
    
    st.markdown("---")
    
    st.header("🔗 Links Úteis")
    st.markdown("""
    - [API Docs](http://localhost:8000/api/v1/docs)
    - [Health Check](http://localhost:8000/api/v1/health)
    - [GitHub](https://github.com)
    """)

if df is None or stats is None:
    st.error("⚠️ Dados não disponíveis. Por favor, execute o scraping primeiro:")
    st.code("python run_scraping.py", language="bash")
    st.stop()

st.header("📊 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

colors = [
    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
]

with col1:
    st.markdown(f"""
    <div style="background: {colors[0]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">📚 Total de Livros</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{stats['total_books']:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: {colors[1]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">📁 Categorias</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{stats['total_categories']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: {colors[2]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">💰 Preço Médio</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">£{stats['average_price']:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: {colors[3]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">⭐ Rating Médio</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{stats['average_rating']:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

colors2 = [
    "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
    "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
    "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
]

with col1:
    percent_in_stock = stats['books_in_stock']/stats['total_books']*100
    st.markdown(f"""
    <div style="background: {colors2[0]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">✅ Em Estoque</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{stats['books_in_stock']:,}</div>
            <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 0.5rem;">{percent_in_stock:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    percent_out_stock = stats['books_out_of_stock']/stats['total_books']*100
    st.markdown(f"""
    <div style="background: {colors2[1]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">❌ Fora de Estoque</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{stats['books_out_of_stock']:,}</div>
            <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 0.5rem;">{percent_out_stock:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: {colors2[2]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: #333; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">💵 Preço Mínimo</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);">£{stats['min_price']:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: {colors2[3]}; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
        <div style="color: #333; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">💵 Preço Máximo</div>
            <div style="font-size: 2rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);">£{stats['max_price']:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("📈 Visualizações")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribuições",
    "📁 Por Categoria",
    "💰 Análise de Preços",
    "⭐ Análise de Ratings",
    "📋 Tabela de Dados"
])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Distribuição de Ratings")
        rating_dist = stats['rating_distribution']
        rating_df = pd.DataFrame({
            'Rating': [f"{k} estrelas" for k in rating_dist.keys()],
            'Quantidade': list(rating_dist.values())
        })
        
        fig_rating = px.bar(
            rating_df,
            x='Rating',
            y='Quantidade',
            color='Quantidade',
            color_continuous_scale='Blues',
            title="Distribuição de Ratings"
        )
        fig_rating.update_layout(showlegend=False)
        st.plotly_chart(fig_rating, width='stretch')
    
    with col2:
        st.subheader("📦 Distribuição de Disponibilidade")
        availability_data = {
            'Status': ['Em Estoque', 'Fora de Estoque'],
            'Quantidade': [stats['books_in_stock'], stats['books_out_of_stock']]
        }
        availability_df = pd.DataFrame(availability_data)
        
        fig_availability = px.pie(
            availability_df,
            values='Quantidade',
            names='Status',
            color='Status',
            color_discrete_map={'Em Estoque': '#2ecc71', 'Fora de Estoque': '#e74c3c'},
            title="Livros em Estoque vs Fora de Estoque"
        )
        st.plotly_chart(fig_availability, width='stretch')

with tab2:
    st.subheader("📁 Estatísticas por Categoria")
    
    cat_df = pd.DataFrame(category_stats)
    
    if not cat_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔝 Top 10 Categorias (por quantidade)")
            top_categories = cat_df.nlargest(10, 'total_books')
            
            fig_top = px.bar(
                top_categories,
                x='total_books',
                y='category',
                orientation='h',
                color='total_books',
                color_continuous_scale='Viridis',
                title="Top 10 Categorias"
            )
            fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top, width='stretch')
        
        with col2:
            st.subheader("💰 Preço Médio por Categoria (Top 10)")
            top_price = cat_df.nlargest(10, 'average_price')
            
            fig_price = px.bar(
                top_price,
                x='category',
                y='average_price',
                color='average_price',
                color_continuous_scale='Greens',
                title="Preço Médio por Categoria"
            )
            fig_price.update_xaxes(tickangle=45)
            st.plotly_chart(fig_price, width='stretch')
        
        st.subheader("📋 Tabela Completa de Categorias")
        st.dataframe(
            cat_df.sort_values('total_books', ascending=False),
            width='stretch',
            hide_index=True
        )

with tab3:
    st.subheader("💰 Análise de Preços")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição de Preços")
        fig_hist = px.histogram(
            df,
            x='price',
            nbins=50,
            title="Distribuição de Preços",
            labels={'price': 'Preço (£)', 'count': 'Quantidade'}
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, width='stretch')
    
    with col2:
        st.subheader("📦 Box Plot de Preços")
        fig_box = px.box(
            df,
            y='price',
            title="Distribuição de Preços (Box Plot)",
            labels={'price': 'Preço (£)'}
        )
        st.plotly_chart(fig_box, width='stretch')
    
    st.subheader("💰 Preço por Categoria")
    price_by_cat = df.groupby('category')['price'].mean().sort_values(ascending=False).head(15)
    price_cat_df = pd.DataFrame({
        'Categoria': price_by_cat.index,
        'Preço Médio': price_by_cat.values
    })
    
    fig_price_cat = px.bar(
        price_cat_df,
        x='Categoria',
        y='Preço Médio',
        color='Preço Médio',
        color_continuous_scale='Reds',
        title="Preço Médio por Categoria (Top 15)"
    )
    fig_price_cat.update_xaxes(tickangle=45)
    st.plotly_chart(fig_price_cat, width='stretch')

with tab4:
    st.subheader("⭐ Análise de Ratings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Rating Médio por Categoria (Top 10)")
        rating_by_cat = df.groupby('category')['rating'].mean().sort_values(ascending=False).head(10)
        rating_cat_df = pd.DataFrame({
            'Categoria': rating_by_cat.index,
            'Rating Médio': rating_by_cat.values
        })
        
        fig_rating_cat = px.bar(
            rating_cat_df,
            x='Categoria',
            y='Rating Médio',
            color='Rating Médio',
            color_continuous_scale='YlOrRd',
            title="Rating Médio por Categoria"
        )
        fig_rating_cat.update_xaxes(tickangle=45)
        st.plotly_chart(fig_rating_cat, width='stretch')
    
    with col2:
        st.subheader("📊 Distribuição de Ratings")
        rating_counts = df['rating'].value_counts().sort_index()
        rating_dist_df = pd.DataFrame({
            'Rating': rating_counts.index,
            'Quantidade': rating_counts.values
        })
        
        fig_rating_dist = px.pie(
            rating_dist_df,
            values='Quantidade',
            names='Rating',
            title="Distribuição de Ratings",
            labels={'Rating': 'Estrelas'}
        )
        st.plotly_chart(fig_rating_dist, width='stretch')
    
    st.subheader("📈 Preço vs Rating")
    fig_scatter = px.scatter(
        df.sample(min(1000, len(df))),
        x='price',
        y='rating',
        color='in_stock',
        size='quantity',
        hover_data=['title', 'category'],
        title="Relação entre Preço e Rating",
        labels={'price': 'Preço (£)', 'rating': 'Rating', 'in_stock': 'Em Estoque'},
        color_discrete_map={True: '#2ecc71', False: '#e74c3c'}
    )
    st.plotly_chart(fig_scatter, width='stretch')

with tab5:
    st.subheader("📋 Dados Completos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories_filter = st.multiselect(
            "Filtrar por Categoria",
            options=df['category'].unique(),
            default=[]
        )
    
    with col2:
        rating_filter = st.slider(
            "Rating Mínimo",
            min_value=0,
            max_value=5,
            value=0
        )
    
    with col3:
        price_range = st.slider(
            "Faixa de Preço (£)",
            min_value=float(df['price'].min()),
            max_value=float(df['price'].max()),
            value=(float(df['price'].min()), float(df['price'].max()))
        )
    
    filtered_df = df.copy()
    
    if categories_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(categories_filter)]
    
    filtered_df = filtered_df[
        (filtered_df['rating'] >= rating_filter) &
        (filtered_df['price'] >= price_range[0]) &
        (filtered_df['price'] <= price_range[1])
    ]
    
    st.info(f"📊 Mostrando {len(filtered_df)} de {len(df)} livros")
    
    display_columns = ['id', 'title', 'category', 'price', 'rating', 'in_stock', 'quantity']
    st.dataframe(
        filtered_df[display_columns],
        width='stretch',
        hide_index=True
    )
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"books_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📚 Books API Dashboard - Tech Challenge FIAP</p>
    <p>Última atualização: {}</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)

