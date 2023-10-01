import json
from datetime import datetime
from os import path

from pytz import timezone


class ApplicationConfig:

    def __init__(self, config_file_path):
        config_file = open(config_file_path, "r")
        self.config = json.loads(config_file.read())
        config_file.close()

        home = path.expanduser('~')
        img_dir_path = path.join(home, *self.read("working_dir"))

        self.time_zone = timezone(self.read("time_zone"))
        self.start_time = self.time_zone.fromutc(datetime.utcnow())
        self.img_dir = self.start_time.strftime(img_dir_path)
        self.items = self.read("items")

    def read(self, key):
        return self.config[key]
