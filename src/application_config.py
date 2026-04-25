import json
from datetime import datetime, timedelta
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
    slides = []
    slide_number = 1

    for item in items:
        # Get times list, default to single empty string for items without times
        times = item.get("times", [""])

        for time in times:
            # Process title - for items with times, append the time
            title = item["name"]
            if time:
                # Convert time from UTC to display timezone for title
                if item.get("time_zone") == "UTC":
                    hour = int(time[:2])
                    minute = int(time[2:4])
                    # Apply the url_offset for time conversion (usually negative)
                    url_offset = item.get("url_offset", 0)
                    adjusted_hour = hour + url_offset
                    # Handle day rollover
                    adjusted_hour = adjusted_hour % 24
                    time_str = f"{adjusted_hour:02d}{minute:02d}"
                else:
                    time_str = time
                title = f"{item['name']} {time_str}"

            # Generate file name
            file_name_parts = [f"{slide_number:03d}", title]
            file_name = " ".join(file_name_parts)

            # Use the time specified, or current time if no time specified
            if time:
                hour = int(time[:2])
                minute = int(time[2:4])
                url_time = start_time.replace(hour=hour, minute=minute)
            else:
                url_time = start_time

            # Convert to UTC if needed for URL
            if item.get("time_zone") == "UTC":
                # Following original downloader logic: subtract utcoffset to get UTC
                url_time = url_time - url_time.utcoffset()
                # Apply URL offset if specified
                url_offset = item.get("url_offset", 0)
                if url_offset:
                    url_time = url_time + timedelta(hours=url_offset)

            url = url_time.strftime(item["url"])

            # Determine hidden status
            hidden = not item.get("show_by_default", True)

            slide = {
                "slide_number": slide_number,
                "title": title,
                "file_name": file_name,
                "url": url,
                "hidden": hidden,
            }
            slides.append(slide)
            slide_number += 1

    return slides


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
