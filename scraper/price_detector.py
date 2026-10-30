from database.db import buscar_ultimo_preco
import re


TITULOS_SUSPEITOS = [
    "mais informações",
    "ver mais",
    "comprar",
    "saiba mais",
]


from pricing import limpar_preco

def titulo_suspeito(titulo):
    if not titulo:
        return True

    titulo_limpo = titulo.strip().lower()

    for termo in TITULOS_SUSPEITOS:
        if termo in titulo_limpo:
            return True

    if len(titulo_limpo) < 8:
        return True

    return False


def preco_suspeito(preco):
    if preco is None:
        return True

    if preco <= 0:
        return True

    # filtro simples para notebook / marketplace
    if preco < 150:
        return True

    return False


def detectar_quedas(produtos, fonte):

    quedas_reais = []
    quedas_suspeitas = []

    for produto in produtos:

        titulo = produto.get("titulo")
        link = produto.get("link", "Sem link")
        preco_atual = limpar_preco(produto.get("preco"))

        if not titulo:
            continue

        preco_anterior = buscar_ultimo_preco(titulo, fonte)
        preco_anterior = limpar_preco(preco_anterior)

        if preco_anterior is None or preco_atual is None:
            continue

        if preco_atual < preco_anterior:

            queda = {
                "titulo": titulo,
                "preco_anterior": preco_anterior,
                "preco_atual": preco_atual,
                "fonte": fonte,
                "link": link
            }

            if titulo_suspeito(titulo) or preco_suspeito(preco_atual):
                quedas_suspeitas.append(queda)
            else:
                quedas_reais.append(queda)

    return quedas_reais, quedas_suspeitas