import requests

import api.api_keys


class GoogleLocationAPI:
    """
    Reads coordinates for given location name from Google Geocode API
    """

    def __init__(self):
        self._url = "https://maps.googleapis.com/maps/api/geocode/json"
        self._key = api.api_keys.google_key

    def get_coordinates(self, name):
        data = {
            "key": self._key,
            "address": name
        }
        response = requests.get(self._url, data)

        if response.status_code != 200:
            raise ValueError("Error with connecting to Google API, HTTP status code: {}".format(response.status_code))

        coordinates = response.json()["results"][0]["geometry"]["location"]
        return coordinates
