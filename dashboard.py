import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🏨 Inteligência de Preços – Serra de Petrópolis")

df = pd.read_csv("tarifas.csv")

# remover hotéis sem preço
df = df.dropna(subset=["preco"])

# garantir que preço é número
df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

media = df["preco"].mean()

barato = df.loc[df["preco"].idxmin()]
caro = df.loc[df["preco"].idxmax()]

col1,col2,col3 = st.columns(3)

col1.metric("Tarifa média da região",f"R$ {media:.0f}")
col2.metric("Hotel mais barato",barato.hotel,f"R$ {barato.preco}")
col3.metric("Hotel mais caro",caro.hotel,f"R$ {caro.preco}")

st.divider()

st.subheader("📊 Ranking de preços")

ranking = df.sort_values("preco")

st.dataframe(ranking,use_container_width=True)

st.subheader("📈 Comparação de preços")

fig = px.bar(
ranking,
x="hotel",
y="preco",
color="preco",
text="preco"
)

st.plotly_chart(fig,use_container_width=True)

st.subheader("📉 Diferença da média")

df["dif_media"] = df["preco"] - media

fig2 = px.scatter(
    df,
    x="hotel",
    y="dif_media",
    size="preco",
    color="dif_media",
)

fig2.update_layout(
    yaxis_title="Diferença da média (R$)"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("📅 Histórico de preços")

hist = pd.read_csv("historico.csv")

fig3 = px.line(
hist,
x="data",
y="preco",
color="hotel"
)

st.plotly_chart(fig3,use_container_width=True)