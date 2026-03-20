import requests
from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):

    URL = "https://books.toscrape.com/"

    def coletar(self):

        response = requests.get(self.URL)

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