from chatterbot.conversation import Statement

from api.google_location import GoogleLocationAPI
from api.weather import WeatherAPI
from conversations.common_adapter import CommonAdapter


class CurrentWeatherAdapter(CommonAdapter):
    """
    returns current weather at given place using public APIs from
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "current weather:",
            "What is the weather now:",
            "give me the weather:",
            "what is the weather like:"
        ])

        negative = kwargs.get("negative", [
            "What time is it",
            "forecast",
            "Give me the weather forecast",
            "weather forecast"
        ])

        critical = kwargs.get("critical", [
            "forecast",
            "time",
            "joke",
            "thank",
            "exchange",
            "currency"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        result = Statement(text="")
        result.confidence = self.determine_confidence(statement)
        place_name = statement.text.split(":", 1)

        if len(place_name) != 2 or place_name[1].strip() == "":
            result.confidence = 0
            result.text = "No place for checking weather given!"
            return result

        place_name = place_name[1].strip()
        google_api = GoogleLocationAPI()
        weather_api = WeatherAPI()

        if result.confidence == 1:
            try:
                location = google_api.get_coordinates(place_name)
                weather = weather_api.get_current_weather(location)
                result.text = weather
            except ValueError as err:
                msg, = err.args
                result.text = "Error: {}".format(msg)

        return result


class WeatherForecastAdapter(CommonAdapter):
    """
    returns weather forecast for a given place name
    """

    def __init__(self, chatbot, **kwargs):
        positive = kwargs.get("positive", [
            "forecast:",
            "Give me the weather forecast:",
            "weather forecast:"
        ])

        negative = kwargs.get("negative", [
            "current weather:",
            "What is the weather now:",
            "give me the weather:",
            "what is the weather like:"
            "What time is it"
        ])

        critical = kwargs.get("critical", [
            "time",
            "now",
            "current",
            "joke",
            "thank",
            "exchange",
            "currency"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        result = Statement(text="")
        result.confidence = self.determine_confidence(statement)
        place_name = statement.text.split(":", 1)

        if len(place_name) != 2 or place_name[1].strip() == "":
            result.confidence = 0
            result.text = "No place for checking weather forecast given!"
            return result

        place_name = place_name[1].strip()
        google_api = GoogleLocationAPI()
        weather_api = WeatherAPI()

        if result.confidence == 1:
            try:
                location = google_api.get_coordinates(place_name)
                forecast = weather_api.get_weather_forecast(location)
                result.text = forecast
            except ValueError as err:
                msg, = err.args
                result.text = "Error: {}".format(msg)

        return result
