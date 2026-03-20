import streamlit as st
import psycopg2
import pandas as pd
import re


# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Smart Price Monitor",
    page_icon="📈",
    layout="wide"
)


# -------------------------------
# CONEXÃO COM BANCO
# -------------------------------
def conectar():
    conn = psycopg2.connect(
        host="localhost",
        database="scraper_db",
        user="postgres",
        password="postgres"
    )
    return conn


# -------------------------------
# LIMPEZA DE PREÇO
# -------------------------------
def limpar_preco(valor):
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor == "" or valor.lower() in ["sem preço", "none"]:
        return None

    valor = valor.replace("£", "")
    valor = valor.replace("R$", "")
    valor = valor.replace("Â", "")
    valor = valor.replace(",", ".")

    numero = re.findall(r"\d+\.\d+|\d+", valor)

    if numero:
        try:
            return float(numero[0])
        except:
            return None

    return None


# -------------------------------
# CARREGAR PRODUTOS
# -------------------------------
@st.cache_data(ttl=60)
def carregar_produtos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, preco, link, data_coleta, fonte
        FROM produtos
        ORDER BY data_coleta DESC
    """)

    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=colunas)


# -------------------------------
# CARREGAR QUEDAS
# -------------------------------
@st.cache_data(ttl=60)
def carregar_quedas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, preco_anterior, preco_atual, fonte, tipo, link, data_detectada
        FROM quedas_detectadas
        ORDER BY data_detectada DESC
    """)

    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=colunas)


# -------------------------------
# DADOS
# -------------------------------
df_produtos = carregar_produtos()
df_quedas = carregar_quedas()

if not df_produtos.empty:
    df_produtos["preco_limpo"] = df_produtos["preco"].apply(limpar_preco)
    df_produtos["data_coleta"] = pd.to_datetime(df_produtos["data_coleta"], errors="coerce")
    df_produtos = df_produtos.dropna(subset=["data_coleta"]).copy()

    df_validos = df_produtos.dropna(subset=["preco_limpo"]).copy()
    df_validos = df_validos[df_validos["preco_limpo"] > 0]
else:
    df_validos = pd.DataFrame(columns=["titulo", "fonte", "preco_limpo", "data_coleta", "link"])

if not df_quedas.empty:
    df_quedas["data_detectada"] = pd.to_datetime(df_quedas["data_detectada"], errors="coerce")
    df_quedas["variacao"] = df_quedas["preco_anterior"] - df_quedas["preco_atual"]
else:
    df_quedas = pd.DataFrame(columns=[
        "titulo", "preco_anterior", "preco_atual", "fonte", "tipo", "link", "data_detectada", "variacao"
    ])


# -------------------------------
# TÍTULO
# -------------------------------
st.title("Smart Price Monitor")
st.caption("Monitoramento automatizado de preços, histórico e detecção de quedas")


# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Filtros")

fontes_disponiveis = ["Todas"]
if not df_validos.empty and "fonte" in df_validos.columns:
    fontes_disponiveis += sorted(df_validos["fonte"].dropna().unique().tolist())

fonte_escolhida = st.sidebar.selectbox("Fonte", fontes_disponiveis)

mostrar_news = st.sidebar.checkbox("Mostrar NewsScraper", value=False)

busca = st.sidebar.text_input("Buscar produto pelo título", value="")

min_registros = st.sidebar.slider(
    "Mínimo de registros por produto",
    min_value=1,
    max_value=20,
    value=1
)

ordenacao = st.sidebar.selectbox(
    "Ordenar produtos por",
    ["Nome (A-Z)", "Menor preço", "Maior preço"]
)


# -------------------------------
# FILTRAR PRODUTOS
# -------------------------------
df_filtrado = df_validos.copy()

if not mostrar_news:
    df_filtrado = df_filtrado[df_filtrado["fonte"] != "NewsScraper"]

if fonte_escolhida != "Todas":
    df_filtrado = df_filtrado[df_filtrado["fonte"] == fonte_escolhida]

if busca.strip():
    df_filtrado = df_filtrado[
        df_filtrado["titulo"].str.contains(busca, case=False, na=False)
    ]

if not df_filtrado.empty:
    contagem = (
        df_filtrado.groupby(["titulo", "fonte"])
        .size()
        .reset_index(name="qtd_registros")
    )

    df_filtrado = df_filtrado.merge(contagem, on=["titulo", "fonte"], how="left")
    df_filtrado = df_filtrado[df_filtrado["qtd_registros"] >= min_registros]
else:
    df_filtrado["qtd_registros"] = 0


# -------------------------------
# MÉTRICAS
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Registros válidos", len(df_filtrado))

with c2:
    st.metric("Produtos únicos", df_filtrado["titulo"].nunique() if not df_filtrado.empty else 0)

with c3:
    if not df_filtrado.empty:
        st.metric("Menor preço global", f"R$ {df_filtrado['preco_limpo'].min():.2f}")
    else:
        st.metric("Menor preço global", "Sem dados")

with c4:
    if not df_filtrado.empty:
        ultima = df_filtrado["data_coleta"].max().strftime("%Y-%m-%d %H:%M:%S")
        st.metric("Última coleta", ultima)
    else:
        st.metric("Última coleta", "Sem dados")


# -------------------------------
# QUEDAS DETECTADAS
# -------------------------------
st.subheader("Quedas detectadas")

if df_quedas.empty:
    st.info("Nenhuma queda detectada foi registrada ainda.")
else:
    df_quedas_filtrado = df_quedas.copy()

    if not mostrar_news:
        df_quedas_filtrado = df_quedas_filtrado[df_quedas_filtrado["fonte"] != "NewsScraper"]

    if fonte_escolhida != "Todas":
        df_quedas_filtrado = df_quedas_filtrado[df_quedas_filtrado["fonte"] == fonte_escolhida]

    col_real, col_sus = st.columns(2)

    with col_real:
        st.markdown("### ✅ Quedas reais")
        reais = df_quedas_filtrado[df_quedas_filtrado["tipo"] == "real"].copy()

        if reais.empty:
            st.write("Nenhuma queda real registrada.")
        else:
            reais = reais.sort_values(by="variacao", ascending=False)
            st.dataframe(
                reais[["titulo", "fonte", "preco_anterior", "preco_atual", "variacao", "data_detectada"]],
                width="stretch",
                hide_index=True
            )

    with col_sus:
        st.markdown("### ⚠ Quedas suspeitas")
        suspeitas = df_quedas_filtrado[df_quedas_filtrado["tipo"] == "suspeita"].copy()

        if suspeitas.empty:
            st.write("Nenhuma queda suspeita registrada.")
        else:
            suspeitas = suspeitas.sort_values(by="variacao", ascending=False)
            st.dataframe(
                suspeitas[["titulo", "fonte", "preco_anterior", "preco_atual", "variacao", "data_detectada"]],
                width="stretch",
                hide_index=True
            )


# -------------------------------
# TABELA DE PRODUTOS
# -------------------------------
st.subheader("Produtos coletados")

if df_filtrado.empty:
    st.warning("Nenhum produto com preço válido encontrado com os filtros atuais.")
    st.stop()

tabela = df_filtrado[[
    "titulo", "fonte", "preco_limpo", "data_coleta", "qtd_registros"
]].copy()

tabela = tabela.rename(columns={
    "titulo": "Título",
    "fonte": "Fonte",
    "preco_limpo": "Preço",
    "data_coleta": "Data da coleta",
    "qtd_registros": "Qtd. registros"
})

if ordenacao == "Nome (A-Z)":
    tabela = tabela.sort_values(by="Título", ascending=True)
elif ordenacao == "Menor preço":
    tabela = tabela.sort_values(by="Preço", ascending=True)
elif ordenacao == "Maior preço":
    tabela = tabela.sort_values(by="Preço", ascending=False)

st.dataframe(tabela, width="stretch", hide_index=True)


# -------------------------------
# BASE DE PRODUTOS PARA SELEÇÃO
# -------------------------------
produtos_base = (
    df_filtrado.groupby(["titulo", "fonte"])["preco_limpo"]
    .agg(["min", "max", "count"])
    .reset_index()
    .rename(columns={"count": "qtd"})
)

if ordenacao == "Nome (A-Z)":
    produtos_base = produtos_base.sort_values(by="titulo", ascending=True)
elif ordenacao == "Menor preço":
    produtos_base = produtos_base.sort_values(by="min", ascending=True)
elif ordenacao == "Maior preço":
    produtos_base = produtos_base.sort_values(by="max", ascending=False)

produtos_disponiveis = [
    f"{row['titulo']} | {row['fonte']}"
    for _, row in produtos_base.iterrows()
]

st.subheader("Análise de preço por produto")

if not produtos_disponiveis:
    st.warning("Nenhum produto disponível para análise com os filtros atuais.")
    st.stop()

produto_escolhido = st.selectbox(
    "Selecione um produto",
    produtos_disponiveis
)

titulo_escolhido, fonte_produto = produto_escolhido.rsplit(" | ", 1)

df_produto = df_filtrado[
    (df_filtrado["titulo"] == titulo_escolhido) &
    (df_filtrado["fonte"] == fonte_produto)
].copy()

df_produto = df_produto.sort_values(by="data_coleta", ascending=True)

if df_produto.empty:
    st.warning("Esse produto ficou sem dados válidos após os filtros aplicados.")
    st.stop()


# -------------------------------
# MÉTRICAS DO PRODUTO
# -------------------------------
preco_atual = df_produto["preco_limpo"].iloc[-1]
preco_min = df_produto["preco_limpo"].min()
preco_max = df_produto["preco_limpo"].max()
qtd_pontos = len(df_produto)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Preço atual", f"R$ {preco_atual:.2f}")

with m2:
    st.metric("Menor preço", f"R$ {preco_min:.2f}")

with m3:
    st.metric("Maior preço", f"R$ {preco_max:.2f}")

with m4:
    st.metric("Coletas do produto", qtd_pontos)

if qtd_pontos < 2:
    st.info("Esse produto ainda tem poucos registros. O gráfico ficará mais útil após novas coletas.")
elif preco_min == preco_max:
    st.info("Até agora, o preço desse produto não variou entre as coletas.")
else:
    variacao = preco_max - preco_min
    st.success(f"Variação detectada no histórico: R$ {variacao:.2f}")


# -------------------------------
# GRÁFICO
# -------------------------------
st.subheader("Histórico de preços")

grafico = df_produto[["data_coleta", "preco_limpo"]].copy()
grafico = grafico.set_index("data_coleta")
grafico = grafico.rename(columns={"preco_limpo": "Preço"})

st.line_chart(grafico, width="stretch")


# -------------------------------
# HISTÓRICO DETALHADO
# -------------------------------
st.subheader("Histórico detalhado do produto")

historico = df_produto[["data_coleta", "preco_limpo", "link"]].copy()
historico = historico.rename(columns={
    "data_coleta": "Data",
    "preco_limpo": "Preço",
    "link": "Link"
})

st.dataframe(historico, width="stretch", hide_index=True)