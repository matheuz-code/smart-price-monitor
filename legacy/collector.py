import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def coletar_livros():

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    livros = []

    for livro in soup.select(".product_pod"):

        titulo = livro.h3.a["title"]
        preco = livro.select_one(".price_color").text

        livros.append({
            "titulo": titulo,
            "preco": preco
        })

    return livros