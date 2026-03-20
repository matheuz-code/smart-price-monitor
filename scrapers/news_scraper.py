import requests
from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class NewsScraper(BaseScraper):

    def coletar(self):

        url = "https://news.ycombinator.com/"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        noticias = []

        titulos = soup.select(".titleline")

        for item in titulos:

            titulo = item.get_text()

            link = item.find("a")["href"]

            noticias.append({
                "titulo": titulo,
                "link": link
            })

        return noticias