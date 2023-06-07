import logging
from datetime import datetime
from Core.File.FileHandler import FileHandler
from Core.Utils.CoordinatesManager import CoordinatesManager
from FoodsiBundle.Api.FoodsiApi import fetch_items
from FoodsiBundle.Service import StockService
from definitions import CONFIG_PATH

coordinates_regex = "^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$";


def get_available_amount(item_data):
    available_amount = 0
    for item in item_data:
        if item.amount != 0:
            available_amount += 1

    return available_amount


class FoodsiHandler:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._stock = []
        self._config = (self._file_handler.get_json_data())
        self._coordinates_manager = CoordinatesManager()

    def handle(self):
        self._coordinates_manager.get_coordinates()

        item_data = fetch_items()
        StockService.compare(self._stock, item_data)

        available_amount = get_available_amount(item_data)
        self._stock = item_data

        logging.info(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Foodsi: 200(OK). Items with stock: {available_amount} All items: {len(item_data)}")
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Foodsi: 200(OK). Items with stock: {available_amount} All items: {len(item_data)}")
        return item_data

