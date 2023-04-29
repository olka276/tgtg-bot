import inspect
import json
import os


class FileHandler:
    def __init__(self, file):
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        self._stream = open(os.path.join(path, file), mode='r+')
        pass

    def get_json_data(self):
        return json.load(self._stream)

    def save(self, data):
        self._stream.seek(0)
        json.dump(data, self._stream, indent=4)
        self._stream.truncate()

    def get_stream(self):
        return self._stream
