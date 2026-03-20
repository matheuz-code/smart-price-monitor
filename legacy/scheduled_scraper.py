import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def coletar_dados():

    print("Coletando dados...")
    print("Pasta atual:", os.getcwd())

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

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M")

    nome_arquivo = f"livros_{agora}.xlsx"
    
    caminho_arquivo = os.path.join(BASE_DIR, nome_arquivo)
    df.to_excel(caminho_arquivo, index=False)

    print("Coleta finalizada!")
    print(f"Arquivo salvo: {caminho_arquivo}")


coletar_dados()