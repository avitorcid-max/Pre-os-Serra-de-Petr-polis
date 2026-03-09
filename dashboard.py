import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")

# ==========================
# DATA E HORA
# ==========================

agora = datetime.now()

st.title("🏨 Inteligência de Preços – Serra de Petrópolis")

col1,col2 = st.columns(2)

col1.metric("📅 Data atual", agora.strftime("%d/%m/%Y"))
col2.metric("⏰ Hora atual", agora.strftime("%H:%M:%S"))

st.divider()

# ==========================
# CARREGAR TARIFAS
# ==========================

df = pd.read_csv("tarifas.csv")

df = df.dropna(subset=["preco"])
df["preco"] = pd.to_numeric(df["preco"])

# Detectar Castelo automaticamente
df["grupo"] = df["hotel"].apply(
    lambda x: "Castelo de Itaipava" if "castelo" in x.lower() else "Outros"
)

# Média da região
media = df["preco"].mean()

barato = df.loc[df["preco"].idxmin()]
caro = df.loc[df["preco"].idxmax()]

col1,col2,col3 = st.columns(3)

col1.metric("Tarifa média da região",f"R$ {media:.0f}")
col2.metric("Hotel mais barato",barato.hotel,f"R$ {barato.preco}")
col3.metric("Hotel mais caro",caro.hotel,f"R$ {caro.preco}")

st.divider()

# ==========================
# RANKING
# ==========================

st.subheader("📊 Ranking de preços")

# Castelo sempre primeiro
castelo = df[df["grupo"] == "Castelo de Itaipava"]
outros = df[df["grupo"] == "Outros"].sort_values("preco")

ranking = pd.concat([castelo, outros])

fig_rank = px.bar(
    ranking,
    x="hotel",
    y="preco",
    text="preco",
    color="grupo",
    color_discrete_map={
        "Castelo de Itaipava":"orange",
        "Outros":"blue"
    }
)

st.plotly_chart(fig_rank,use_container_width=True)

st.divider()

# ==========================
# COMPETITIVIDADE
# ==========================

st.subheader("📉 Competitividade de preço")

df["vs_media"] = df["preco"] - media

fig_comp = px.scatter(
    df,
    x="hotel",
    y="vs_media",
    size="preco",
    color="grupo",
    color_discrete_map={
        "Castelo de Itaipava":"orange",
        "Outros":"blue"
    }
)

st.plotly_chart(fig_comp,use_container_width=True)

st.divider()

# ==========================
# HISTÓRICO
# ==========================

st.subheader("📈 Evolução de tarifas")

hist = pd.read_csv("historico.csv")

hist["data"] = pd.to_datetime(hist["data"])

# Filtrar último ano
hist = hist[hist["data"] >= (datetime.now() - pd.DateOffset(years=1))]

# Calendário
inicio = st.date_input(
"Início do período",
hist["data"].min()
)

fim = st.date_input(
"Fim do período",
hist["data"].max()
)

hist = hist[(hist["data"] >= pd.to_datetime(inicio)) & (hist["data"] <= pd.to_datetime(fim))]

fig_hist = px.line(
hist,
x="data",
y="preco",
color="hotel",
markers=True
)

st.plotly_chart(fig_hist,use_container_width=True)

st.divider()

# ==========================
# MAPA DE HOTÉIS
# ==========================

st.subheader("🗺️ Mapa de hotéis")

coords = {
"Castelo de Itaipava":(-22.389,-43.134),
"Kastel Itaipava Hotel":(-22.391,-43.133),
"Flat Itaipava":(-22.390,-43.132),
"Villa Itaipava Resort":(-22.394,-43.130),
"Altenhaus Pousada":(-22.401,-43.118),
"Arcadia Pousada Itaipava":(-22.398,-43.121),
"Tankamana":(-22.365,-43.100),
"Hotel Caminhos de Itaipava":(-22.388,-43.129),
"Grande Hotel Petrópolis":(-22.509,-43.178)
}

df["lat"] = df["hotel"].apply(lambda x: coords.get(x,(None,None))[0])
df["lon"] = df["hotel"].apply(lambda x: coords.get(x,(None,None))[1])

st.map(df[["lat","lon"]])
