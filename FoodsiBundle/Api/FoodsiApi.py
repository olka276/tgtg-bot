import json
import requests
from FoodsiBundle.Parser import FoodsiApiResponseParser
from Core.Config.ConfigGetter import get_config_value


def fetch_items():
    config = get_config_value("coordinates")
    request_body = {
        "page": 1,
        "per_page": 15,
        "distance": {
            "lat": config['latitude'],
            "lng": config['longitude'],
            "range": int(config['radius']) * 1000
        },
        "hide_unavailable": False,
        "food_type": [],
        "collection_time": {
            "from": "00:00:00",
            "to": "23:59:59"
        }
    }
    credentials = get_config_value("foodsi")

    foodsi_login = requests.post(
        'https://api.foodsi.pl/api/v2/auth/sign_in',
        headers={
            'Content-type': 'application/json',
            'system-version': 'android_3.0.0',
            'user-agent': 'okhttp/3.12.0'
        }, data=json.dumps(credentials))

    headers = foodsi_login.headers

    foodsi_api = requests.post(
        'https://api.foodsi.pl/api/v2/restaurants',
        headers={
            'Content-type': 'application/json',
            'system-version': 'android_3.0.0',
            'user-agent': 'okhttp/3.12.0',
            'Access-Token': headers["Access-Token"],
            'Client': headers["Client"],
            'Uid': headers["Uid"]
        },

        data=json.dumps(request_body))

    return FoodsiApiResponseParser.parse(foodsi_api.json())
