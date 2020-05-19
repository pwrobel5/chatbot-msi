from api.currency import CurrencyAPI
from conversations.common_adapter import CommonAdapter


class CurrencyAdapter(CommonAdapter):
    """
    returns current exchange rate for given currency
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "kurs wymiany:",
            "waluta:",
            "podaj kurs wymiany:"
        ])

        negative = kwargs.get("negative", [
            "która jest godzina?",
            "jaka jest pogoda",
            "podaj prognozę pogody"
        ])

        critical = kwargs.get("critical", [
            "pogoda",
            "pogody",
            "pogodę",
            "prognoza",
            "prognozy",
            "godzina",
            "czas",
            "dziękuję",
            "żart"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        currency_name = self.verify_argument(statement)
        currency_api = CurrencyAPI()

        if self.response.confidence == 1.0:
            try:
                currency_rate = currency_api.get_currency_rate(currency_name)
                self.response.text = currency_rate
            except ValueError as err:
                msg, = err.args
                self.response.text = "Błąd: {}".format(msg)

        return self.response
