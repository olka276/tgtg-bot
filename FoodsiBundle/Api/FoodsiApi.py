import json
from datetime import timezone, datetime

import requests
import math

from Core.Exception.ConfigException import ConfigException
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

    if not credentials["email"] or not credentials["password"]:
        raise ConfigException('Add foodsi credentials to config.json')

    foodsi_login = requests.post(
        'https://api.foodsi.pl/api/v2/auth/sign_in',
        headers={
            'Content-type': 'application/json',
            'system-version': 'android_3.0.0',
            'user-agent': 'okhttp/3.12.0'
        }, data=json.dumps(credentials))

    headers = foodsi_login.headers

    utc = timezone.utc
    waw_dt = datetime.now(utc)
    timestamp_string = waw_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    timestamp_string = "{0}:{1}".format(
        timestamp_string[:-2],
        timestamp_string[-2:]
    )

    radius = 10000
    coef = radius / 111320.0
    config_coordinates = get_config_value("coordinates")

    latitude_min = float(config_coordinates["latitude"]) - coef
    latitude_max = float(config_coordinates["latitude"]) + coef
    longitude_min = float(config_coordinates["longitude"]) - coef / math.cos(
        float(config_coordinates["latitude"]) * 0.01745)
    longitude_max = float(config_coordinates["longitude"]) + coef / math.cos(
        float(config_coordinates["latitude"]) * 0.01745)

    foodsi_api = requests.get(
        'https://api.foodsi.pl/api/v3/user/offers?filter[package_category_ids][not_eq]=[13]&filter'
        '[package_category_ids][eq]=[1,9]&filter[active][eq]=true'
        '&filter[pickup_to][gt]=' + timestamp_string +
        '&filter[current_quantity][gt]=0&page[size]=100&filter[active][eq]=true'
        '&filter[venue_longitude][gt]=' + str(longitude_min) +
        '&&filter[venue_longitude][lt]=' + str(longitude_max) +
        '&filter[venue_latitude][gt]=' + str(latitude_min) +
        '&&filter[venue_latitude][lt]=' + str(latitude_max),
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
