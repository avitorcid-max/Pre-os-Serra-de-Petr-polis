import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

hoteis = [
"Castelo de Itaipava",
"Kastel Itaipava Hotel",
"Arcadia Pousada Itaipava",
"Hotel Caminhos de Itaipava",
"Grande Hotel Petrópolis",
"Altenhaus Pousada",
"Villa Itaipava Resort",
"Tankamana",
"Flat Itaipava"
]

data_hoje = datetime.now().strftime("%Y-%m-%d")

precos = []

for hotel in hoteis:

    print("Buscando:", hotel)

    busca = hotel.replace(" ", "+")

    url = f"https://www.google.com/search?q={busca}+hotel+price"

    headers = {
        "User-Agent":"Mozilla/5.0"
    }

    try:

        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.text,"html.parser")

        preco = None

        for span in soup.find_all("span"):

            texto = span.text

            if "R$" in texto:

                preco = texto.replace("R$","").replace(".","").replace(",","")

                break

        if preco:
            preco = float(preco)
        else:
            preco = None

    except:

        preco = None

    precos.append({
        "hotel":hotel,
        "preco":preco,
        "data":data_hoje,
        "hora":datetime.now().strftime("%H:%M")
    })

    time.sleep(2)

df = pd.DataFrame(precos)

df.to_csv("tarifas.csv",index=False)

# =============================
# HISTÓRICO
# =============================

try:

    hist = pd.read_csv("historico.csv")

    hist = pd.concat([hist,df])

except:

    hist = df

hist.to_csv("historico.csv",index=False)

print("✔ Preços coletados")
