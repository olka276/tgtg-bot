from Core.File.FileHandler import FileHandler
from definitions import CONFIG_PATH


def get_config_value(value=None):
    if value is None:
        return FileHandler(CONFIG_PATH).get_json_data()
    return FileHandler(CONFIG_PATH).get_json_data()[value]
