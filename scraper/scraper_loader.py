import os
import importlib
import inspect

from scrapers.base_scraper import BaseScraper


def carregar_scrapers():
    scrapers = []
    pasta = "scrapers"

    for arquivo in os.listdir(pasta):
        if not arquivo.endswith(".py"):
            continue

        if arquivo.startswith("__"):
            continue

        modulo_nome = arquivo[:-3]

        modulo = importlib.import_module(f"scrapers.{modulo_nome}")

        for _, obj in inspect.getmembers(modulo, inspect.isclass):
            if issubclass(obj, BaseScraper) and obj is not BaseScraper:
                scrapers.append(obj())

    return scrapers