import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🏨 Inteligência de Preços – Serra de Petrópolis")

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

# ranking visual

st.subheader("📊 Ranking de preços")

ranking = df.sort_values("preco")

fig_rank = px.bar(
ranking,
x="hotel",
y="preco",
text="preco",
color="preco",
)

st.plotly_chart(fig_rank,use_container_width=True)

# competitividade

st.subheader("📉 Competitividade de preço")

df["vs_media"] = df["preco"] - media

fig_comp = px.scatter(
df,
x="hotel",
y="vs_media",
size="preco",
color="vs_media",
)

st.plotly_chart(fig_comp,use_container_width=True)

st.divider()

# histórico

st.subheader("📈 Evolução de tarifas")

hist = pd.read_csv("historico.csv")

fig_hist = px.line(
hist,
x="data",
y="preco",
color="hotel",
markers=True
)

st.plotly_chart(fig_hist,use_container_width=True)

st.divider()

# mapa (coordenadas simples)

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
