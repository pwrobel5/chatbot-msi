import requests
import api.api_keys
from datetime import datetime


class CurrencyAPI:
    BASE_CURRENCY = "PLN"

    def __init__(self):
        self._url = "http://data.fixer.io/api/latest"
        self._key = api.api_keys.datafixer_key

    def get_currency_rate(self, currency):
        time_format = "%Y-%m-%d %H:%M"
        requested_currency = currency

        if self.BASE_CURRENCY not in currency:
            currency = "{},{}".format(currency, self.BASE_CURRENCY)

        data = {
            "access_key": self._key,
            "symbols": currency
        }
        response = requests.get(self._url, data)

        if response.status_code != 200:
            raise ValueError("Error with connection to Currency API, HTTP status code: {}".format(response.status_code))

        response_json = response.json()
        date = datetime.utcfromtimestamp(response_json["timestamp"]).strftime(time_format)
        base_rate = float(response_json["rates"][self.BASE_CURRENCY])
        exchange_rate = float(response_json["rates"][requested_currency])
        exchange_rate = base_rate / exchange_rate

        return "Exchange rate for date: {}, 1 {} = {} {}".format(
            date,
            requested_currency,
            exchange_rate,
            self.BASE_CURRENCY
        )
