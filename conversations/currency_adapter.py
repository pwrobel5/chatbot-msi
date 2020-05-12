from conversations.common_adapter import CommonAdapter
from chatterbot.conversation import Statement
from api.currency import CurrencyAPI


class CurrencyAdapter(CommonAdapter):
    """
    returns current exchange rate for given currency
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "exchange rate:",
            "currency:",
            "give me exchange rate for:"
        ])

        negative = kwargs.get("negative", [
            "what time is it",
            "give me current weather",
            "give me forecast"
        ])

        critical = kwargs.get("critical", [
            "weather",
            "forecast",
            "time",
            "thank",
            "joke"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        result = Statement(text="Currency mode")
        result.confidence = self.determine_confidence(statement)
        currency_name = statement.text.split(":", 1)

        if len(currency_name) != 2 or currency_name[1].strip() == "":
            result.confidence = 0
            result.text = "No given currency name"
            return result

        currency_name = currency_name[1].strip()
        currency_api = CurrencyAPI()

        if result.confidence == 1:
            try:
                currency_rate = currency_api.get_currency_rate(currency_name)
                result.text = currency_rate
            except ValueError as err:
                msg, = err.args
                result.text = "Error: {}".format(msg)

        return result
