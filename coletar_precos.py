from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib.parse
import re
from datetime import datetime

# hotéis monitorados
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

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

dados = []

for hotel in hoteis:

    print("Buscando:", hotel)

    busca = urllib.parse.quote(hotel + " hotel")

    url = f"https://www.google.com/travel/hotels?q={busca}"

    driver.get(url)

    time.sleep(8)

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
        "preco":preco,
        "data":datetime.now().strftime("%Y-%m-%d"),
        "hora":datetime.now().strftime("%H:%M")
    })

driver.quit()

df = pd.DataFrame(dados)

# salvar tarifas atuais
df.to_csv("tarifas.csv",index=False)

# atualizar histórico
try:

    hist = pd.read_csv("historico.csv")

    hist = pd.concat([hist,df])

except:

    hist = df

hist.to_csv("historico.csv",index=False)

print("✔ Coleta finalizada")