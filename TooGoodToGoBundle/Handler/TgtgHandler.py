import logging
from datetime import datetime
from Core.File.FileHandler import FileHandler
from Core.Utils.CoordinatesManager import CoordinatesManager
from TooGoodToGoBundle.Service import StockService
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
        StockService.compare(self._stock, item_data)
        self._stock = item_data
        logging.info(f"{datetime.now().strftime('%H:%M:%S')} - TGTG: 200(OK). Items: {len(item_data)}")
        print(f"{datetime.now().strftime('%H:%M:%S')} - TGTG: 200(OK). Items: {len(item_data)}")
        return item_data
