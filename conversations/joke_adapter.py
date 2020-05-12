import random

from chatterbot.conversation import Statement

from conversations.common_adapter import CommonAdapter


class JokeAdapter(CommonAdapter):
    JOKES = [
        """Porucznik sprawdza umiejętności 3 nowych szeregowych:
        - Powiedzcie nam, co potraficie zrobić pożytecznego?
        Pierwszy mówi:
        - Ja potrafię obsługiwać komputer.
        - Dobrze, może być, a Ty?
        - Ja znam się na gotowaniu - mówi drugi.
        - Nieźle. A co Ty potrafisz? - pyta trzeciego.
        - Ja potrafię zrobić bulbulator.
        - A co to jest?
        - Proszę o kawałek blachy, gwoździe, młotek i szklankę wody to pokażę.
        Otrzymał to, o co prosił, wbił gwoździe w blachę, robiąc w niej dziurki, zalał to wodą i mówi:
        - Robi bulbul? No to bulbulator!
        Zirytowany porucznik:
        - Ty głupi jesteś, będziesz hańbą dla wojska!
        I wyrzuca blachę przez okno. Po chwili przychodzi major:
        - KTÓRY WYRZUCIŁ NOWY BULBULATOR!?""",
        """- dziadku czy oglądasz dziś mecz??
        - A KTO GRA
        - Polska i Brazylia
        - A Z KIM???""",
        """Jaka jest różnica między teologiem a geologiem?
        Jeden z nich zaczyna się na 't', zaś drugi na 'g'.""",
        """Facet wchodzi do baru i zamawia poncz owocowy.
        Barman mówi do niego 'Kolego, jak chcesz dostać ponczu musisz ustawić się w kolejce'
        Facet rozgląda się dookoła ale nie ma kolejki do ponczu"""
    ]

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "Rozśmiesz mnie",
            "Opowiedz żart",
            "Opowiedz dowcip",
            "Opowiedz kawał"
        ])

        negative = kwargs.get("negative", [
            "Podaj prognozę pogody",
            "Jaka jest pogoda",
            "Która jest godzina",
            "Czas",
            "kurs walut"
        ])

        critical = kwargs.get("critical", [
            "pogoda",
            "pogody",
            "czas",
            "godzina",
            "kurs",
            "walut",
            "waluta",
            "wymiany"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical)

    def process(self, statement, additional_response_selection_parameters=None):
        self.response = Statement(text="")
        self.response.confidence = self.determine_confidence(statement)
        self.response.text = random.choice(self.JOKES)

        return self.response
