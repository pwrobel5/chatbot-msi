from api.google_location import GoogleLocationAPI
from api.weather import WeatherAPI
from conversations.common_adapter import CommonAdapter


class CurrentWeatherAdapter(CommonAdapter):
    """
    returns current weather at given place using public APIs from
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "bieżąca pogoda:",
            "jaka jest teraz pogoda:",
            "podaj pogodę:"
        ])

        negative = kwargs.get("negative", [
            "Która jest godzina",
            "prognoza",
            "prognozy",
            "prognozę",
            "podaj prognozę pogody",
            "prognoza pogody"
        ])

        critical = kwargs.get("critical", [
            "prognoza",
            "prognozę",
            "prognozy",
            "godzina",
            "czas",
            "żart",
            "dziękuję",
            "dzięki",
            "kurs",
            "wymiany",
            "waluta",
            "walut"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        place_name = self.verify_argument(statement)
        google_api = GoogleLocationAPI()
        weather_api = WeatherAPI()

        if self.response.confidence == 1.0:
            try:
                location = google_api.get_coordinates(place_name)
                weather = weather_api.get_current_weather(location)
                self.response.text = weather
            except ValueError as err:
                msg, = err.args
                self.response.text = "Błąd: {}".format(msg)

        return self.response


class WeatherForecastAdapter(CommonAdapter):
    """
    returns weather forecast for a given place name
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "prognoza:",
            "podaj prognozę:",
            "prognoza pogody:"
        ])

        negative = kwargs.get("negative", [
            "bieżąca pogoda:",
            "jaka jest teraz pogoda:",
            "podaj pogodę:",
            "która jest godzina"
        ])

        critical = kwargs.get("critical", [
            "godzina",
            "czas",
            "teraz",
            "bieżąca",
            "bieżącą",
            "żart",
            "dziękuję",
            "dzięki",
            "kurs",
            "wymiany",
            "walut",
            "waluta"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        place_name = self.verify_argument(statement)
        google_api = GoogleLocationAPI()
        weather_api = WeatherAPI()

        if self.response.confidence == 1.0:
            try:
                location = google_api.get_coordinates(place_name)
                forecast = weather_api.get_weather_forecast(location)
                self.response.text = forecast
            except ValueError as err:
                msg, = err.args
                self.response.text = "Błąd: {}".format(msg)

        return self.response
