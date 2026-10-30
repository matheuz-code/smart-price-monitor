import unittest
from demo import comparar, PRODUCTS
from pricing import limpar_preco


class PriceTests(unittest.TestCase):
    def test_brazilian_currency(self):
        self.assertEqual(limpar_preco('R$ 1.234,56'), 1234.56)

    def test_international_currency(self):
        self.assertEqual(limpar_preco('£1,234.56'), 1234.56)

    def test_decimal_and_thousands(self):
        self.assertEqual(limpar_preco('£51.77'), 51.77)
        self.assertEqual(limpar_preco('1.234'), 1234)
        self.assertEqual(limpar_preco('89,90'), 89.9)

    def test_invalid_prices(self):
        for value in (None, '', 'sem preço', -1, float('nan'), True):
            self.assertIsNone(limpar_preco(value))

    def test_filter_and_no_result(self):
        self.assertEqual(len(comparar('NOTEBOOK')), 2)
        self.assertEqual(comparar('inexistente'), [])

    def test_comparison(self):
        rows = comparar('Notebook')
        self.assertEqual(rows[0]['preco'], 2650)
        self.assertTrue(all(p['menor_preco'] == 2650 for p in rows))

    def test_does_not_mutate_source(self):
        comparar()
        self.assertTrue(all('menor_preco' not in p for p in PRODUCTS))


if __name__ == '__main__':
    unittest.main()
