import os
import re
from datetime import datetime

from Core.Exception.ConfigException import ConfigException
from Core.File.FileHandler import FileHandler
from TelegramBundle.Api import TelegramApi
from TooGoodToGoBundle.Api.TgtgAPI import TgtgAPI
from definitions import CONFIG_PATH

coordinates_regex = "^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$";


class TgtgHandler:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._tgtg_api = TgtgAPI()
        self._stock = []
        self._config = (self._file_handler.get_json_data())

    def handle(self):
        coordinates = self._config["coordinates"]

        if coordinates.get("latitude") is None or coordinates.get("longitude") is None or coordinates.get(
                "radius") is None:
            self.set_coordinates()

        client = self._tgtg_api.get_client()
        item_data = (
            TgtgAPI.fetch_items(client, coordinates["latitude"], coordinates["longitude"], coordinates["radius"]))
        self.compare_stock(item_data)
        self._stock = item_data
        print(f"{datetime.now().strftime('%H:%M:%S')} - TGTG: 200(OK). Items: {len(item_data)}")
        return item_data

    def set_coordinates(self):
        lat = input("Type your latitude: ")

        if re.search(coordinates_regex, lat) is None:
            raise ConfigException("Latitude format is invalid")

        lng = input("Type your longitude: ")

        if re.search(coordinates_regex, lng) is None:
            raise ConfigException("Longitude format is invalid")

        rad = input("Type radius of searching: ")
        if not rad.isnumeric():
            raise ConfigException("Radius format is invalid")

        config = (self._file_handler.get_json_data())

        config['coordinates'] = {
            "latitude": lat,
            "longitude": lng,
            "radius": rad
        }

        self._file_handler.save(config)

    def compare_stock(self, items):
        blacklist = self._config["blacklist"]
        for item in items:
            try:
                old_stock = [stock['items_available'] for stock in self._stock if stock['id'] == item['id']][0]
            except IndexError:
                old_stock = 0
            try:
                item['msg_id'] = [stock['msg_id'] for stock in self._stock if stock['id'] == item['id']][0]
            except:
                pass

            new_stock = item['items_available']

            # Check, if the stock has changed. Send a message if so.
            if new_stock != old_stock:
                # Check if the stock was replenished, send an encouraging image message
                if old_stock == 0 and new_stock > 0:
                    if not any(x in item['store_name'] for x in blacklist):
                        message = f"🍽 [{item['store_name']}](https://share.toogoodtogo.com/item/{item['id']})\n"
                        # f"_{item['description']}_\n"\

                        message += f"🫱 {new_stock}\n"
                        message += f"💰 {item['price_including_taxes']}/{item['value_including_taxes']}\n"
                        if 'rating' in item:
                            message += f"⭐️ {item['rating']}/5\n"
                        if 'pickup_start' and 'pickup_end' in item:
                            message += f"⏰ {item['pickup_start']} - {item['pickup_end']}\n"
                        message += "ℹ️ TooGoodToGo"
                        TelegramApi.send(message)
                elif old_stock > new_stock != 0:
                    pass
                    # # customer feedback: This message is not needed
                    # pass
                    # ## Prepare a generic string, but with the important info
                    # message = f" 📉 Decrease from {old_stock} to {new_stock} available goodie bags at {[item['store_name'] for item in new_api_result if item['item_id'] == item_id][0]}."
                    # TelegramApi.send(message)
                elif old_stock > new_stock == 0:
                    if not any(x in item['store_name'] for x in blacklist):
                        message = f" ⭕ Paczki wyprzedane: {item['store_name']}."
                        TelegramApi.send(message)
                        # telegram_bot_sendtext(message)
                        try:
                            print("delete message")
                            # tg = telegram_bot_delete_message(
                            #     [stock['msg_id'] for stock in self._stock if stock['id'] == item['id']][0])
                        except:
                            print(f"Failed to remove message for item id: {item['id']}")
                            # print(traceback.format_exc())
                else:
                    if not any(x in item['store_name'] for x in blacklist):
                        # Prepare a generic string, but with the important info
                        message = f"There was a change of number of goodie bags in stock from {old_stock} to {new_stock} at {item['store_name']}."
                        TelegramApi.send(message)
                        # telegram_bot_sendtext(message)
