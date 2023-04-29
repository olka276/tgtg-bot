import re
import time
from datetime import datetime

from Core.Exception.ConfigException import ConfigException
from Core.File.FileHandler import FileHandler
from FoodsiBundle.Api.FoodsiApi import FoodsiApi
from TelegramBundle.Api import TelegramApi
from definitions import CONFIG_PATH

coordinates_regex = "^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$";


class FoodsiHandler:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._foodsi_api = FoodsiApi()
        self._stock = []
        self._config = (self._file_handler.get_json_data())

    def handle(self):
        coordinates = self._config["coordinates"]

        if coordinates.get("latitude") is None or coordinates.get("longitude") is None or coordinates.get(
                "radius") is None:
            self.set_coordinates()

        item_data = self._foodsi_api.fetch_items()
        self.compare_stock(item_data)
        self._stock = item_data
        print(f"{datetime.now().strftime('%H:%M:%S')} - Foodsi: 200(OK). Items: {len(item_data)}")
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
                old_stock = \
                    [stock['package_day']['meals_left'] for stock in self._stock if stock['id'] == item['id']][
                        0]
            except IndexError:
                old_stock = 0
            try:
                item['msg_id'] = [stock['msg_id'] for stock in self._stock if stock['id'] == item['id']][0]
            except:
                pass

            new_stock = item['package_day']['meals_left']

            # Check, if the stock has changed. Send a message if so.
            if new_stock != old_stock:
                # Check if the stock was replenished, send an encouraging image message
                if old_stock == 0 and new_stock > 0:
                    if not any(x in item['name'] for x in blacklist):
                        # TODO: tommorrow date
                        message = f"🍽 [{item['name']}]({item['url']})\n" \
                                  f"💰 {item['meal']['price']}PLN/{item['meal']['original_price']}PLN\n" \
                                  f"🫱 {new_stock}\n" \
                                  f"⏰ {item['opened_at']}-{item['closed_at']}\n" \
                                  "ℹ️ Foodsi"
                        # message += f"\ndebug id: {item['id']}"
                        TelegramApi.send(message)
                elif old_stock > new_stock and new_stock != 0:
                    # customer feedback: This message is not needed
                    pass
                    ## Prepare a generic string, but with the important info
                    # message = f" 📉 Decrease from {old_stock} to {new_stock} available goodie bags at {[item['name'] for item in new_api_result if item['id'] == item_id][0]}."
                    # telegram_bot_sendtext(message)
                elif old_stock > new_stock and new_stock == 0:
                    if not any(x in item['name'] for x in blacklist):
                        message = f" ⭕ Paczki wyprzedane: {item['name']}."
                        TelegramApi.send(message)
                        try:
                            pass
                            # telegram_bot_delete_message(
                            #     [stock['msg_id'] for stock in self._stock if stock['id'] == item['id']][0])
                        except:
                            print(f"Failed to remove message for item id: {item['id']}")
                            # print(traceback.format_exc())
                else:
                    if not any(x in item['store_name'] for x in blacklist):
                        # Prepare a generic string, but with the important info
                        message = f"There was a change of number of goodie bags in stock from {old_stock} to {new_stock} at {item['name']}."
                        TelegramApi.send(message)
