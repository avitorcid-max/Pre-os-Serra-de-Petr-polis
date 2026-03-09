from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib.parse
import re
from datetime import datetime

hoteis = [
"Castelo de Itaipava",
"Kastel Itaipava Hotel",
"Flat Itaipava",
"Villa Itaipava Resort",
"Altenhaus Pousada",
"Arcadia Pousada Itaipava",
"Tankamana",
"Hotel Caminhos de Itaipava",
"Grande Hotel Petrópolis"
]

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(
service=Service(ChromeDriverManager().install()),
options=options
)

dados = []

for hotel in hoteis:

    busca = urllib.parse.quote(hotel + " hotel")
    url = f"https://www.google.com/travel/hotels?q={busca}"

    driver.get(url)

    time.sleep(6)

    preco = None

    try:
        elementos = driver.find_elements(By.XPATH,"//span[contains(text(),'R$')]")

        if elementos:
            texto = elementos[0].text
            numero = re.sub(r"[^\d]", "", texto)

            if numero:
                preco = int(numero)

    except:
        pass

    dados.append({
        "hotel":hotel,
        "preco":preco
    })

driver.quit()

df = pd.DataFrame(dados)

df.to_csv("tarifas.csv",index=False)

# salvar histórico
agora = datetime.now()

df["data"] = agora.date()

try:
    hist = pd.read_csv("historico.csv")
    hist = pd.concat([hist,df])
except:
    hist = df

hist.to_csv("historico.csv",index=False)

print("Coleta concluída")