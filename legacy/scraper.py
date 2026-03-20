import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox


def coletar_dados():

    log.delete(1.0, tk.END)

    url = "https://books.toscrape.com/"

    log.insert(tk.END, "Conectando ao site...\n")
    janela.update()

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

        log.insert(tk.END, f"Coletado: {titulo}\n")
        janela.update()

    df = pd.DataFrame(livros)

    df.to_excel("livros.xlsx", index=False)

    messagebox.showinfo(
        "Concluído",
        f"{len(livros)} livros coletados!"
    )


janela = tk.Tk()
janela.title("Web Data Collector")
janela.geometry("500x400")


titulo = tk.Label(
    janela,
    text="Coletor de Dados da Web",
    font=("Arial", 14)
)

titulo.pack(pady=10)


botao = tk.Button(
    janela,
    text="Coletar dados do site",
    command=coletar_dados,
    height=2,
    width=25
)

botao.pack(pady=10)


log = tk.Text(janela, height=15, width=60)
log.pack(pady=10)


janela.mainloop()