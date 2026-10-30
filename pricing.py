"""Normalização de preços para as fontes existentes, sem acesso à rede."""
import math
import re


def limpar_preco(valor):
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return float(valor) if math.isfinite(valor) and valor >= 0 else None
    text = str(valor).strip()
    match = re.search(r"-?\d[\d.,]*", text)
    if not match:
        return None
    number = match.group()
    if number.startswith('-'):
        return None
    if ',' in number and '.' in number:
        decimal = ',' if number.rfind(',') > number.rfind('.') else '.'
        number = number.replace('.' if decimal == ',' else ',', '')
        number = number.replace(decimal, '.')
    elif ',' in number:
        number = number.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(?:\.\d{3})+', number):
        number = number.replace('.', '')
    try:
        result = float(number)
        return result if math.isfinite(result) else None
    except ValueError:
        return None
