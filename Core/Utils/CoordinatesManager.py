import re

from Core.Config.ConfigGetter import get_config_value
from Core.Exception.ConfigException import ConfigException
from Core.File.FileHandler import FileHandler
from definitions import CONFIG_PATH

coordinates_regex = "^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$"


class CoordinatesManager:
    def __init__(self):
        self._file_handler = FileHandler(CONFIG_PATH)

    def get_coordinates(self):
        coordinates = get_config_value("coordinates")
        if "latitude" not in coordinates or "longitude" not in coordinates or "radius" not in coordinates:
            self.set_coordinates()
        return coordinates

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

        config = get_config_value()

        config['coordinates'] = {
            "latitude": lat,
            "longitude": lng,
            "radius": rad
        }

        self._file_handler.save(config)
