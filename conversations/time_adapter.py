from datetime import datetime

from chatterbot.conversation import Statement

from conversations.common_adapter import CommonAdapter


class TimeAdapter(CommonAdapter):
    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "Która jest godzina?",
            "Jaki mamy czas?",
            "Czas"
        ])

        negative = kwargs.get("negative", [
            "bieżąca pogoda:",
            "jaka jest pogoda:",
            "podaj pogodę:",
            "prognoza pogody:",
            "dziękuję",
            "waluta",
            "kurs wymiany"
        ])

        critical = kwargs.get("critical", [
            "pogoda",
            "pogody",
            "żart",
            "dowcip",
            "kawał",
            "prognoza",
            "prognozy",
            "kurs",
            "waluta",
            "wymiany",
            "walut"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        now = datetime.now()
        self.response = Statement(text="Jest godzina {}".format(now.strftime('%I:%M %p')))
        self.response.confidence = self.determine_confidence(statement)
        return self.response
