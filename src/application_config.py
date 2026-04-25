import json
from datetime import datetime
from os import path

from pytz import timezone

# pylint: disable=too-few-public-methods


def process_slides(items, display_time_zone, start_time):
    """
    Convert config items into processed slides with all metadata.

    Args:
        items (list): List of config items to process
        display_time_zone (pytz.timezone): User's time zone for display
        start_time (datetime): Start time of application in user's time zone
    Returns:
        list: List of slide dictionaries with keys:
            - slide_number (int): Sequential number starting from 1
            - title (str|None): Slide title, null when omitting
            - file_name (str): Generated filename for download
            - url (str): Fully processed URL ready for download
            - hidden (bool): Whether slide should be hidden
    """
    # TODO: Implement slide processing logic
    return []


class ApplicationConfig:
    """
    Class for managing application configuration settings.

    Attributes:
        config (dict): A dictionary containing the configuration settings.
        display_time_zone (string): User's time zone
        start_time (string): Time the application was started.
          This is calculated, not read from JSON.
        img_dir (string): Directory to download images to.
          Substitutes the start_time if configured (see readme).
        items (array): The items to be downloaded. See the readme.
    """

    def __init__(self, config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            self.config = json.loads(config_file.read())

        home = path.expanduser("~")
        img_dir_path = path.join(home, *self.config["working_dir"])

        self.display_time_zone = timezone(self.config["display_time_zone"])
        self.start_time = self.display_time_zone.fromutc(datetime.utcnow())
        self.img_dir = self.start_time.strftime(img_dir_path)
        self.items = self.config["items"]
        self.slides = process_slides(
            self.config["items"], self.display_time_zone, self.start_time
        )
