import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Hospitalar",
    layout="wide"
)

st.title("🏥 Dashboard Hospitalar")
st.markdown("Análise dos atendimentos por tipo, cidade e bairro")


# CARREGAR DADOS


@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_limpos.csv")

    df['tipo_atendimento'] = (
        df['tipo_atendimento']
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df['cidade'] = (
        df['cidade']
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df['bairro'] = (
        df['bairro']
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return df

df = carregar_dados()


# FILTROS


st.subheader("🔎 Filtros")

f1, f2 = st.columns(2)

cidades = sorted(df['cidade'].dropna().unique())
bairros = sorted(df['bairro'].dropna().unique())

with f1:
    cidade = st.selectbox(
        "Cidade",
        ["Todas"] + cidades
    )

if cidade != "Todas":
    bairros_filtrados = sorted(
        df[df["cidade"] == cidade]["bairro"]
        .dropna()
        .unique()
    )
else:
    bairros_filtrados = bairros

with f2:
    bairro = st.selectbox(
        "Bairro",
        ["Todos"] + bairros_filtrados
    )

df_filtrado = df.copy()

if cidade != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["cidade"] == cidade
    ]

if bairro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["bairro"] == bairro
    ]


# MÉTRICAS

st.subheader("📌 Indicadores")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total de Atendimentos",
        len(df_filtrado)
    )

with c2:
    st.metric(
        "Cidades Únicas",
        df_filtrado["cidade"].nunique()
    )

with c3:
    st.metric(
        "Bairros Únicos",
        df_filtrado["bairro"].nunique()
    )

# DADOS DOS GRÁFICOS

tipos = (
    df_filtrado["tipo_atendimento"]
    .value_counts()
    .reset_index()
)

tipos.columns = ["Tipo", "Quantidade"]

cidades_df = (
    df_filtrado["cidade"]
    .value_counts()
    .head(10)
    .reset_index()
)

cidades_df.columns = ["Cidade", "Quantidade"]

bairros_df = (
    df_filtrado["bairro"]
    .value_counts()
    .head(10)
    .reset_index()
)

bairros_df.columns = ["Bairro", "Quantidade"]


# GRÁFICOS


col1, col2 = st.columns(2)

with col1:

    fig_pizza = px.pie(
        tipos,
        names="Tipo",
        values="Quantidade",
        title="Distribuição dos Tipos de Atendimento"
    )

    st.plotly_chart(
        fig_pizza,
        use_container_width=True
    )

with col2:

    fig_tipos = px.bar(
        tipos,
        x="Tipo",
        y="Quantidade",
        text="Quantidade",
        title="Tipos de Atendimento"
    )

    st.plotly_chart(
        fig_tipos,
        use_container_width=True
    )


# CIDADE E BAIRRO

col3, col4 = st.columns(2)

with col3:

    fig_cidades = px.bar(
        cidades_df,
        x="Cidade",
        y="Quantidade",
        text="Quantidade",
        title="Top 10 Cidades"
    )

    st.plotly_chart(
        fig_cidades,
        use_container_width=True
    )

with col4:

    fig_bairros = px.bar(
        bairros_df,
        x="Quantidade",
        y="Bairro",
        orientation="h",
        text="Quantidade",
        title="Top 10 Bairros"
    )

    st.plotly_chart(
        fig_bairros,
        use_container_width=True
    )


# INSIGHT AUTOMÁTICO

if not tipos.empty:

    tipo_top = tipos.iloc[0]["Tipo"]
    qtd_top = tipos.iloc[0]["Quantidade"]

    st.success(
        f"O tipo de atendimento mais frequente é '{tipo_top}', "
        f"com {qtd_top} registros."
    )

# TABELA

st.subheader("📋 Dados Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)