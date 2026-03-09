import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")

# =============================
# DATA E HORA
# =============================

agora = datetime.now()

st.title("🏨 Inteligência de Preços – Serra de Petrópolis")

col_data, col_hora = st.columns(2)

col_data.metric("📅 Data atual", agora.strftime("%d/%m/%Y"))
col_hora.metric("⏰ Hora atual", agora.strftime("%H:%M:%S"))

st.divider()

# =============================
# CARREGAR DADOS
# =============================

df = pd.read_csv("tarifas.csv")

df = df.dropna(subset=["preco"])
df["preco"] = pd.to_numeric(df["preco"])

media = df["preco"].mean()

barato = df.loc[df["preco"].idxmin()]
caro = df.loc[df["preco"].idxmax()]

col1,col2,col3 = st.columns(3)

col1.metric("Tarifa média da região",f"R$ {media:.0f}")
col2.metric("Hotel mais barato",barato.hotel,f"R$ {barato.preco}")
col3.metric("Hotel mais caro",caro.hotel,f"R$ {caro.preco}")

st.divider()

# =============================
# RANKING
# =============================

st.subheader("📊 Ranking de preços")

ranking = df.sort_values("preco")

ranking["cor"] = ranking["hotel"].apply(
    lambda x: "Castelo de Itaipava" if x == "Castelo de Itaipava" else "Outros"
)

fig_rank = px.bar(
ranking,
x="hotel",
y="preco",
text="preco",
color="cor",
color_discrete_map={
"Castelo de Itaipava":"orange",
"Outros":"steelblue"
}
)

st.plotly_chart(fig_rank,use_container_width=True)

st.divider()

# =============================
# COMPETITIVIDADE
# =============================

st.subheader("📉 Competitividade de preço")

df["vs_media"] = df["preco"] - media

df["cor"] = df["hotel"].apply(
lambda x: "Castelo de Itaipava" if x == "Castelo de Itaipava" else "Outros"
)

fig_comp = px.scatter(
df,
x="hotel",
y="vs_media",
size="preco",
color="cor",
color_discrete_map={
"Castelo de Itaipava":"orange",
"Outros":"blue"
}
)

st.plotly_chart(fig_comp,use_container_width=True)

st.divider()

# =============================
# HISTÓRICO
# =============================

st.subheader("📈 Evolução de tarifas")

hist = pd.read_csv("historico.csv")

hist["data"] = pd.to_datetime(hist["data"])

# FILTRAR 1 ANO
hist = hist[hist["data"] >= (datetime.now() - pd.DateOffset(years=1))]

# CALENDÁRIO
data_inicio = st.date_input(
"Início do período",
hist["data"].min()
)

data_fim = st.date_input(
"Fim do período",
hist["data"].max()
)

hist = hist[(hist["data"] >= pd.to_datetime(data_inicio)) & (hist["data"] <= pd.to_datetime(data_fim))]

fig_hist = px.line(
hist,
x="data",
y="preco",
color="hotel",
markers=True
)

st.plotly_chart(fig_hist,use_container_width=True)

st.divider()

# =============================
# MAPA
# =============================

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

df["lat"] = df["hotel"].apply(lambda x: coords[x][0])
df["lon"] = df["hotel"].apply(lambda x: coords[x][1])

st.map(df[["lat","lon"]])
