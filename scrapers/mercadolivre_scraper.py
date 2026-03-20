from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from scrapers.base_scraper import BaseScraper


class MercadoLivreScraper(BaseScraper):

    def coletar(self):

        produtos = []

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            page = context.new_page()

            try:
                page.goto("https://lista.mercadolivre.com.br/notebook", timeout=60000)

                page.wait_for_timeout(5000)

                url_atual = page.url.lower()

                if "login" in url_atual or "registration" in url_atual or "account-verification" in url_atual:
                    print("MercadoLivreScraper bloqueado pelo site (login/verificação exigidos).")
                    browser.close()
                    return []

                page.wait_for_selector("li.ui-search-layout__item", timeout=20000)

                items = page.query_selector_all("li.ui-search-layout__item")

                print(f"{len(items)} produtos encontrados na página")

                titulos = page.query_selector_all("h2")
                precos = page.query_selector_all(".andes-money-amount__fraction")
                links = page.query_selector_all("a.ui-search-link")

                print(f"{len(titulos)} títulos encontrados")
                print(f"{len(precos)} preços encontrados")
                print(f"{len(links)} links encontrados")

                limite = min(len(titulos), len(precos), len(links))

                for i in range(limite):
                    try:
                        titulo = titulos[i].inner_text().strip()
                        preco_texto = precos[i].inner_text().replace(".", "").strip()
                        preco = float(preco_texto)
                        link = links[i].get_attribute("href")

                        produtos.append({
                            "titulo": titulo,
                            "preco": preco,
                            "link": link
                        })
                    except:
                        continue

            except PlaywrightTimeout:
                print("MercadoLivreScraper não conseguiu carregar os produtos a tempo.")
                produtos = []

            except Exception as e:
                print(f"MercadoLivreScraper falhou: {e}")
                produtos = []

            browser.close()

        print(f"{len(produtos)} produtos coletados com sucesso")

        return produtos