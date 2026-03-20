from scrapers.base_scraper import BaseScraper


class MagaluScraper(BaseScraper):

    def coletar(self):
        print("MagaluScraper desativado temporariamente (bloqueio por CAPTCHA/anti-bot).")
        return []