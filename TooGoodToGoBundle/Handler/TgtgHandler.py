from datetime import datetime
from Core.Config.ConfigGetter import get_config_value
from Core.File.FileHandler import FileHandler
from Core.Utils.CoordinatesManager import CoordinatesManager
from TelegramBundle.Api import TelegramApi
from TooGoodToGoBundle.Api.TgtgAPI import TgtgAPI
from definitions import CONFIG_PATH


class TgtgHandler:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._tgtg_api = TgtgAPI()
        self._stock = []
        self._coordinates_manager = CoordinatesManager()

    def handle(self):
        coordinates = self._coordinates_manager.get_coordinates()
        client = self._tgtg_api.get_client()
        item_data = TgtgAPI.fetch_items(client, coordinates["latitude"], coordinates["longitude"], coordinates["radius"])
        self.compare_stock(item_data)
        self._stock = item_data
        print(f"{datetime.now().strftime('%H:%M:%S')} - TGTG: 200(OK). Items: {len(item_data)}")
        return item_data

    def compare_stock(self, items):
        blacklist = get_config_value("blacklist")
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

            if new_stock != old_stock:
                if old_stock == 0 and new_stock > 0:
                    if not any(x in item['store_name'] for x in blacklist):
                        message = f"🍽 [{item['store_name']}](https://share.toogoodtogo.com/item/{item['id']})\n"
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
                elif old_stock > new_stock == 0:
                    if not any(x in item['store_name'] for x in blacklist):
                        message = f" ⭕ Paczki wyprzedane: {item['store_name']}."
                        TelegramApi.send(message)
                        try:
                            print("delete message")
                            TelegramApi.remove([stock['msg_id'] for stock in self._stock if stock['id'] == item['id']][0])
                        except:
                            print(f"Failed to remove message for item id: {item['id']}")
                            # print(traceback.format_exc())
                else:
                    if not any(x in item['store_name'] for x in blacklist):
                        # Prepare a generic string, but with the important info
                        message = f"There was a change of number of goodie bags in stock from {old_stock} to {new_stock} at {item['store_name']}."
                        TelegramApi.send(message)
