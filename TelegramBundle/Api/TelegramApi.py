import random
import string
import time
from urllib.parse import quote
import requests
from Core.Exception.ConfigException import ConfigException
from Core.File.FileHandler import FileHandler
from definitions import CONFIG_PATH


def get_config():
    config = FileHandler(CONFIG_PATH).get_json_data()
    return config


def send(message):
    config = get_config()["telegram"]
    print(config)
    for chat_id in config['bot_chat_id']:
        send_text = 'https://api.telegram.org/bot' + config[
            "bot_token"] + '/sendMessage?chat_id=' + chat_id.get("id") + '&parse_mode=Markdown&text=' + quote(
            message) + '&disable_web_page_preview=true'
        requests.get(send_text)


def remove(message_id):
    config = get_config()["telegram"]
    for chat_id in config['bot_chat_id']:
        send_text = 'https://api.telegram.org/bot' + config[
            "bot_token"] + '/sendMessage?chat_id=' + chat_id.get("id") + '&parse_mode=Markdown&text=' + quote(
            message_id) + '&disable_web_page_preview=true'
        requests.get(send_text)


def add_bot_chat_id(config):
    bot_token = config["telegram"]["bot_token"]

    if not bot_token:
        raise ConfigException('Add bot token into your config.json file.')

    pin = ''.join(random.choice(string.digits) for x in range(6))
    print("Please type \"" + pin + "\" to the bot.")

    response = requests.get('https://api.telegram.org/bot' + bot_token + '/getUpdates?limit=1&offset=-1')
    while not response.json()['result'] or (response.json()['result'][0]['message']['text'] != pin):
        time.sleep(1)
        response = requests.get('https://api.telegram.org/bot' + bot_token + '/getUpdates?limit=1&offset=-1')

    bot_chat_id = str(response.json()['result'][0]['message']['chat']['id'])
    print("Your chat id:" + str(bot_chat_id))

    config["telegram"]['bot_chat_id'].append({
        "id": bot_chat_id
    })
    FileHandler(CONFIG_PATH).save(config)
