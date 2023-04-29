import traceback

from Core.File.FileHandler import FileHandler
from Core.Utils.TerminalColor import *
from tgtg import TgtgClient
from Core.Utils.TerminalPrint import color_print
from TooGoodToGoBundle.Parser.TgtgApiResponseParser import parse
from definitions import CONFIG_PATH


class TgtgAPI:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)
        self._config = self._file_handler.get_json_data()

    def get_client(self):
        try:
            config = self._config
        except FileNotFoundError:
            print("Config.json file not found.")
            print(traceback.format_exc())
            exit(1)
        except:
            color_print(TerminalColor.FAIL, "Unexpected error.")
            print(traceback.format_exc())
            exit(1)

        try:
            client = TgtgClient(
                access_token=config['tgtg']['access_token'],
                refresh_token=config['tgtg']['refresh_token'],
                user_id=config['tgtg']['user_id'],
                cookie=config['tgtg']['cookie']
            )
        except KeyError:
            try:
                email = input("Type your TooGoodToGo email address: ")
                client = TgtgClient(email=email)
                credentials = client.get_credentials()
                print(credentials)
                config['tgtg'] = credentials
                self._file_handler.save(config)
                client = TgtgClient(
                    access_token=config['tgtg']['access_token'],
                    refresh_token=config['tgtg']['refresh_token'],
                    user_id=config['tgtg']['user_id'])
            except:
                color_print(TerminalColor.FAIL, "Error during logging into polling.")
                exit(1)

        return client

    @staticmethod
    def fetch_items(client, latitude, longitude, radius):
        api_response = client.get_items(
            favorites_only=False,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            page_size=300
        )

        return parse(api_response)
