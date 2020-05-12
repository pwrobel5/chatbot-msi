from datetime import datetime

import requests

import api.api_keys


class WeatherAPI:
    """
    Gets current weather conditions or weather forecast for given place coordinates from WeatherBit API
    """

    def __init__(self):
        self._url_current = "https://api.weatherbit.io/v2.0/current"
        self._url_forecast = "https://api.weatherbit.io/v2.0/forecast/daily"
        self._key = api.api_keys.weatherbit_key

    def get_current_weather(self, location):
        data = {
            "key": self._key,
            "lat": location["lat"],
            "lon": location["lng"],
            "lang": "pl"
        }
        response = requests.get(self._url_current, data)

        if response.status_code != 200:
            raise ValueError("Błąd połączenia z API pogodowym, status HTTP: {}".format(response.status_code))

        response_data = response.json()["data"][0]
        result = "Pogoda dla {}, {}:\n\tdata: {}\n\tpogoda: {}\n\ttemperatura: {}\n\twschód słońca: {}\n\t" \
                 "zachód słońca: {}".format(
            response_data["city_name"], response_data["country_code"],
            response_data["ob_time"], response_data["weather"]["description"], response_data["temp"],
            response_data["sunrise"], response_data["sunset"]
        )
        return result

    def get_weather_forecast(self, location):
        time_format = "%H:%M"
        data = {
            "key": self._key,
            "lat": location["lat"],
            "lon": location["lng"],
            "days": "5",
            "lang": "pl"
        }
        response = requests.get(self._url_forecast, data)

        if response.status_code != 200:
            raise ValueError("Błąd połączenia z API pogodowym, status HTTP: {}".format(response.status_code))

        response_json = response.json()
        city_name = response_json["city_name"]
        country = response_json["country_code"]
        result = "Prognoza pogody dla {}, {}:\n".format(city_name, country)

        forecasts = response_json["data"]
        for forecast in forecasts:
            sunrise = datetime.utcfromtimestamp(forecast["sunrise_ts"]).strftime(time_format)
            sunset = datetime.utcfromtimestamp(forecast["sunset_ts"]).strftime(time_format)
            result += "\t{}\n\t\tpogoda: {}\n\t\ttemperatura minimalna: {}\n\t\ttemperatura maksymalna: {}\n\t\t" \
                      "temperatura średnia: {}\n\t\twschód słońca: {}\n\t\tzachód słońca: {}\n".format(
                forecast["valid_date"], forecast["weather"]["description"], forecast["min_temp"],
                forecast["max_temp"], forecast["temp"], sunrise, sunset
            )

        return result
