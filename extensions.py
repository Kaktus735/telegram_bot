import requests
import json
import re
from config import keys

currency_pattern = re.compile('[А-Яа-яЁё]+')

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Проверим, что введеный текст соответствует кириллице
        if currency_pattern.fullmatch(quote) is None:
            raise APIException(f'Вы должны использовать кириллицу при вводе валюты `{quote}`.')

        if currency_pattern.fullmatch(base) is None:
            raise APIException(f'Вы должны использовать кириллицу при вводе валюты `{base}`.')

        # Приведем валюту к одному регистру
        quote = quote.lower()
        base = base.lower()

        if quote == base:
            raise APIException(f'Невозможно привести одинаковые валюты `{base}`.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту `{quote}`.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту `{base}`.')

        try:
            amount = float(amount)
            if amount.is_integer():
                amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество `{amount}`.')

        if amount <= 0:
            raise APIException(f'Введеное количество `{amount}` должно быть больше нуля.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        if total_base.is_integer():
            total_base = int(total_base)

        return total_base
