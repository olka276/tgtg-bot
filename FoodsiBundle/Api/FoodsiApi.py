import json

import requests

from Core.File.FileHandler import FileHandler
from FoodsiBundle.Parser import FoodsiApiResponseParser
from definitions import CONFIG_PATH


class FoodsiApi:

    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._config = self._file_handler.get_json_data()

    def fetch_items(self):
        request_body = {
            "page": 1,
            "per_page": 15,
            "distance": {
                "lat": self._config['coordinates']['latitude'],
                "lng": self._config['coordinates']['longitude'],
                "range": int(self._config['coordinates']['radius']) * 1000
            },
            "hide_unavailable": False,
            "food_type": [],
            "collection_time": {
                "from": "00:00:00",
                "to": "23:59:59"
            }
        }

        foodsi_api = requests.post \
            ('https://api.foodsi.pl/api/v2/restaurants',
             headers={'Content-type': 'application/json', 'system-version': 'android_3.0.0',
                      'user-agent': 'okhttp/3.12.0'}, data=json.dumps(request_body))

        return FoodsiApiResponseParser.parse(foodsi_api.json())