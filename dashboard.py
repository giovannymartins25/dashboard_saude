import pandas as pd
import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Hospitalar",
    layout="wide"
)

st.title("🏥 Dashboard de Atendimentos")

# =========================
# CARREGAR DADOS
# =========================
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados_limpos.csv')
    
    # padronizar texto
    df['tipo_atendimento'] = df['tipo_atendimento'].astype(str).str.lower().str.strip()
    df['cidade'] = df['cidade'].astype(str).str.lower().str.strip()
    df['bairro'] = df['bairro'].astype(str).str.lower().str.strip()

    return df

df = carregar_dados()

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("🔎 Filtros")

cidade = st.sidebar.selectbox(
    "Cidade",
    ["Todas"] + sorted(df['cidade'].dropna().unique())
)

bairro = st.sidebar.selectbox(
    "Bairro",
    ["Todos"] + sorted(df['bairro'].dropna().unique())
)

# aplicar filtros
df_filtrado = df.copy()

if cidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado['cidade'] == cidade]

if bairro != "Todos":
    df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]

# =========================
# MÉTRICAS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total de Atendimentos", len(df_filtrado))
col2.metric("Cidades únicas", df_filtrado['cidade'].nunique())
col3.metric("Bairros únicos", df_filtrado['bairro'].nunique())

# =========================
# GRÁFICOS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Tipos de Atendimento")
    st.bar_chart(df_filtrado['tipo_atendimento'].value_counts())

with col2:
    st.subheader("🌆 Atendimentos por Cidade")
    st.bar_chart(df_filtrado['cidade'].value_counts().head(10))

st.subheader("🏠 Atendimentos por Bairro")
st.bar_chart(df_filtrado['bairro'].value_counts().head(10))

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")
st.dataframe(df_filtrado.head(100))