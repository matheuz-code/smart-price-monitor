import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def coletar_dados():

    print("Coletando dados...")

    url = "https://books.toscrape.com/"

    resposta = requests.get(url)

    soup = BeautifulSoup(resposta.text, "html.parser")

    livros = []

    for livro in soup.select(".product_pod"):

        titulo = livro.h3.a["title"]
        preco = livro.select_one(".price_color").text

        livros.append({
            "Titulo": titulo,
            "Preco": preco
        })

    df = pd.DataFrame(livros)

    df.to_excel("livros_auto.xlsx", index=False)

    print(f"{len(livros)} livros coletados!")


while True:

    coletar_dados()

    print("Esperando 60 segundos...\n")

    time.sleep(60)