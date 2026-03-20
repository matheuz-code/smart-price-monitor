from scraper.scraper_loader import carregar_scrapers
from scraper.analyzer import analisar_precos
from scraper.price_detector import detectar_quedas
from database.db import salvar_produtos, salvar_quedas


def executar_agente():

    print("Agente iniciando...")

    scrapers = carregar_scrapers()

    print(f"{len(scrapers)} scrapers encontrados.")

    for scraper in scrapers:

        nome = scraper.__class__.__name__

        print(f"\nExecutando scraper: {nome}")

        try:
            dados = scraper.coletar()

            if dados:

                salvar_produtos(dados, nome)

                print("Dados salvos no banco de dados.")

                analisar_precos(dados)

                quedas_reais, quedas_suspeitas = detectar_quedas(dados, nome)

                salvar_quedas(quedas_reais, "real")
                salvar_quedas(quedas_suspeitas, "suspeita")

                if quedas_reais:
                    print("\n✅ Quedas reais detectadas:")
                    for queda in quedas_reais:
                        print(
                            f"- {queda['titulo']} | "
                            f"de R$ {queda['preco_anterior']:.2f} "
                            f"para R$ {queda['preco_atual']:.2f}"
                        )
                else:
                    print("Nenhuma queda real detectada.")

                if quedas_suspeitas:
                    print("\n⚠ Quedas suspeitas detectadas:")
                    for queda in quedas_suspeitas:
                        print(
                            f"- {queda['titulo']} | "
                            f"de R$ {queda['preco_anterior']:.2f} "
                            f"para R$ {queda['preco_atual']:.2f}"
                        )
                else:
                    print("Nenhuma queda suspeita detectada.")

            else:
                print("Nenhum dado coletado.")

        except Exception as e:
            print(f"Scraper {nome} falhou, mas o agente continuou: {e}")