import time
import traceback

import schedule

from TooGoodToGoBundle.Handler.TgtgHandler import TgtgHandler

handler = TgtgHandler()


def refresh():
    try:
        handler.handle()
        print("refreshed")
    except:
        print(traceback.format_exc())


schedule.every(30).seconds.do(refresh)
refresh()
while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
