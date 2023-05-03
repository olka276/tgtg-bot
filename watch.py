import time
import traceback
import schedule
from FoodsiBundle.Handler.FoodsiHandler import FoodsiHandler
from TooGoodToGoBundle.Handler.TgtgHandler import TgtgHandler

tgtg_handler = TgtgHandler()
foodsi_handler = FoodsiHandler()


def watch():
    try:
        tgtg_handler.handle()
        foodsi_handler.handle()
    except:
        print(traceback.format_exc())


schedule.every(2).seconds.do(watch)
watch()
while True:
    schedule.run_pending()
    time.sleep(1)
