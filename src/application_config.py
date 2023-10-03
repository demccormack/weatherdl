import json
from datetime import datetime
from os import path

from pytz import timezone


class ApplicationConfig:
    """
    Class for managing application configuration settings.

    Attributes:
        config (dict): A dictionary containing the configuration settings.
        time_zone (string): User's time zone
        start_time (string): Time the application was started.
          This is calculated, not read from JSON.
        img_dir (string): Directory to download images to.
          Substitutes the start_time if configured (see readme).
        items (array): The items to be downloaded. See the readme.
    """

    def __init__(self, config_file_path):
        with open(config_file_path, "r") as config_file:
            self.config = json.loads(config_file.read())

        home = path.expanduser('~')
        img_dir_path = path.join(home, *self.config["working_dir"])

        self.time_zone = timezone(self.config["time_zone"])
        self.start_time = self.time_zone.fromutc(datetime.utcnow())
        self.img_dir = self.start_time.strftime(img_dir_path)
        self.items = self.config["items"]
