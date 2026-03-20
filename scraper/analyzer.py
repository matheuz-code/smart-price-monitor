import re


def limpar_preco(valor):
    if valor is None:
        return None

    valor = str(valor).strip()
    valor = valor.replace("£", "")
    valor = valor.replace("R$", "")
    valor = valor.replace("Â", "")
    valor = valor.replace(",", ".")

    numero = re.findall(r"\d+\.\d+|\d+", valor)

    if numero:
        try:
            return float(numero[0])
        except:
            return None

    return None


def analisar_precos(produtos):

    precos = []

    for produto in produtos:
        preco = limpar_preco(produto.get("preco"))

        if preco is not None and preco > 0:
            precos.append(preco)

    if len(precos) == 0:
        print("Nenhum preço válido encontrado para análise.")
        return

    preco_medio = sum(precos) / len(precos)
    preco_min = min(precos)
    preco_max = max(precos)

    print("\nAnálise de preços:")
    print(f"Preço médio: R$ {preco_medio:.2f}")
    print(f"Preço mínimo: R$ {preco_min:.2f}")
    print(f"Preço máximo: R$ {preco_max:.2f}")