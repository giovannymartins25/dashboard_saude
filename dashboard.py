import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard Hospitalar",
    layout="centered"
)

st.title("🏥 Dashboard de Atendimentos")

# CARREGAR DADOS

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados_limpos.csv')
    
    df['tipo_atendimento'] = df['tipo_atendimento'].astype(str).str.lower().str.strip()
    df['cidade'] = df['cidade'].astype(str).str.lower().str.strip()
    df['bairro'] = df['bairro'].astype(str).str.lower().str.strip()

    return df

df = carregar_dados()

# FILTROS 

st.subheader("🔎 Filtros")

cidade = st.selectbox(
    "Cidade",
    ["Todas"] + sorted(df['cidade'].dropna().unique())
)

bairro = st.selectbox(
    "Bairro",
    ["Todos"] + sorted(df['bairro'].dropna().unique())
)

df_filtrado = df.copy()

if cidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado['cidade'] == cidade]

if bairro != "Todos":
    df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]

# MÉTRICAS

st.subheader("📌 Resumo")

st.metric("Total de Atendimentos", len(df_filtrado))
st.metric("Cidades únicas", df_filtrado['cidade'].nunique())
st.metric("Bairros únicos", df_filtrado['bairro'].nunique())

# GRÁFICOS 

st.subheader("📊 Tipos de Atendimento")
st.bar_chart(df_filtrado['tipo_atendimento'].value_counts().head(5))

st.subheader("🌆 Atendimentos por Cidade")
st.bar_chart(df_filtrado['cidade'].value_counts().head(5))

st.subheader("🏠 Atendimentos por Bairro")
st.bar_chart(df_filtrado['bairro'].value_counts().head(5))

# TABELA

st.subheader("📋 Dados (amostra)")
st.dataframe(df_filtrado.head(50))