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
            "lon": location["lng"]
        }
        response = requests.get(self._url_current, data)

        if response.status_code != 200:
            raise ValueError("Error with connection to Weather API, HTTP status code: {}".format(response.status_code))

        response_data = response.json()["data"][0]
        result = "Weather for {}, {},\n\ttime: {},\n\tweather condition: {},\n\ttemperature: {},\n\tsunrise: {},\n\t" \
                 "sunset: {}".format(
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
            "days": "5"
        }
        response = requests.get(self._url_forecast, data)

        if response.status_code != 200:
            raise ValueError("Error with connection to Weather API, HTTP status code: {}".format(response.status_code))

        response_json = response.json()
        city_name = response_json["city_name"]
        country = response_json["country_code"]
        result = "Forecast for {}, {}:\n".format(city_name, country)

        forecasts = response_json["data"]
        for forecast in forecasts:
            sunrise = datetime.utcfromtimestamp(forecast["sunrise_ts"]).strftime(time_format)
            sunset = datetime.utcfromtimestamp(forecast["sunset_ts"]).strftime(time_format)
            result += "\t{},\n\t\tweather condition: {},\n\t\tmin temperature: {},\n\t\tmax temperature: {},\n\t\t" \
                      "average temperature: {},\n\t\tsunrise: {},\n\t\tsunset: {}\n".format(
                forecast["valid_date"], forecast["weather"]["description"], forecast["min_temp"],
                forecast["max_temp"], forecast["temp"], sunrise, sunset
            )

        return result
