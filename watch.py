import logging
import time
import traceback
import schedule

from Core.Config.ConfigGetter import get_config_value
from Core.File.FileHandler import FileHandler
from Core.Utils.TerminalColor import TerminalColor
from Core.Utils.TerminalPrint import color_print
from FoodsiBundle.Handler.FoodsiHandler import FoodsiHandler
from TelegramBundle.Api import TelegramApi
from TooGoodToGoBundle.Handler.TgtgHandler import TgtgHandler
from definitions import CONFIG_PATH

tgtg_handler = TgtgHandler()
foodsi_handler = FoodsiHandler()


def hello():
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    # print("Hello! Welcome to FoodBot.")
    config = get_config_value()
    if len(config["telegram"]["bot_token"]) == 0:
        color_print(TerminalColor.FAIL, "Telegram token not found in config!")
        bot_token = input("Type your telegram bot token: ")
        config["telegram"] = {
            "bot_token": bot_token,
            "bot_chat_id": config["telegram"]["bot_chat_id"]
        }

        FileHandler(CONFIG_PATH).save(config)
    #
    # print("[1] Start watching")
    # print("[2] Add chat ID")
    # option = input("")
    #
    # if option == "2":
    #     config = get_config_value()
    #     TelegramApi.add_bot_chat_id(config)
    # elif option == "1":
    schedule.every(15).seconds.do(watch)
    watch()
    while True:
        schedule.run_pending()
        time.sleep(1)


def watch():
    try:
        tgtg_handler.handle()
        foodsi_handler.handle()
    except:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())


hello()
