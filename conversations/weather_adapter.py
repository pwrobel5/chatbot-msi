import functools

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

from api.google_location import GoogleLocationAPI
from api.weather import WeatherAPI


class WeatherAdapter(LogicAdapter):
    """
    Abstract class for weather adapters

    :kwargs:
        * *positive* (``list``) --
          Questions related to adapter
        * *negative* (``list``) --
          Questions not related to adapter
        * *critical* (``list``) --
          List of keywords which cannot be in question related to adapter
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.positive = kwargs.get("positive", [])
        self.positive = list(map(lambda x: x.lower().split(":", 1)[0].split(), self.positive))
        self.positive = set(functools.reduce(lambda x, y: x + y, self.positive, []))

        self.negative = kwargs.get("negative", [])
        self.negative = list(map(lambda x: x.lower().split(":", 1)[0].split(), self.negative))
        self.negative = set(functools.reduce(lambda x, y: x + y, self.negative, []))

        self.critical = set(kwargs.get("critical", []))

    def determine_confidence(self, statement):
        """
        :param statement: Statement object to calculate confidence of using current adapter
        :return: 0 if statement contains word from critical list
                 1 if number of words from positive is >= number of words from negative and is > 0
                 0 in other cases
        """

        text = statement.text.lower().split(":", 1)[0]

        for critical_word in self.critical:
            if critical_word in text:
                return 0

        positives_counter = functools.reduce(lambda counter, element: counter + 1 if element in text else counter,
                                             self.positive, 0)
        negatives_counter = functools.reduce(lambda counter, element: counter + 1 if element in text else counter,
                                             self.negative, 0)

        if positives_counter >= negatives_counter and positives_counter > 0:
            return 1
        else:
            return 0


class CurrentWeatherAdapter(WeatherAdapter):
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
            "thank"
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
                return Statement(text="Error: {}".format(msg))

        return result


class WeatherForecastAdapter(WeatherAdapter):
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
            "thank"
        ])

        super().__init__(chatbot, positive=positive, negative=negative, critical=critical, **kwargs)

    def process(self, statement, additional_response_selection_parameters=None):
        result = Statement(text="Wow, you want weather forecast!")
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
                return Statement(text="Error: {}".format(msg))

        return result
