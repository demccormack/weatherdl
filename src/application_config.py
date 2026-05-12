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
            # Create timezone-aware reference datetime if time is specified
            reference_datetime = None
            if time:
                # Create timezone-aware reference datetime from time and time_zone
                hour = int(time[:2])
                minute = int(time[2:4])

                # Get the timezone for this item
                item_tz_name = item.get("time_zone", display_time_zone.zone)
                item_tz = timezone(item_tz_name)

                # Create reference datetime directly in the item's timezone
                reference_datetime = start_time.astimezone(item_tz).replace(
                    hour=hour, minute=minute, second=0, microsecond=0
                )

                # For title: Convert reference datetime to display timezone
                title_datetime = reference_datetime.astimezone(display_time_zone)
                time_str = title_datetime.strftime("%H%M")
                title = f"{item['name']} {time_str}"
            else:
                title = item["name"]

            # Generate file name
            file_name_parts = [f"{slide_number:03d}", title]
            file_name = " ".join(file_name_parts)

            # Process URL - substitute datetime placeholders if present
            url = item["url"]
            if reference_datetime is not None:
                # For URL processing: handle url_time_zone and url_offset
                url_time_zone_name = item.get("url_time_zone")
                url_offset = item.get("url_offset", 0)

                if url_time_zone_name:
                    # Convert reference time to URL timezone first
                    url_time_zone = timezone(url_time_zone_name)
                    url_time = reference_datetime.astimezone(url_time_zone)

                    # Then apply offset if specified
                    if url_offset:
                        url_time = url_time + timedelta(hours=url_offset)
                else:
                    # No url_time_zone, just apply offset to reference time
                    if url_offset:
                        url_time = reference_datetime + timedelta(hours=url_offset)
                    else:
                        url_time = reference_datetime
            else:
                url_time = start_time

            url = url_time.strftime(item["url"])

            # Determine hidden status
            hidden = not item.get("show_by_default", True)

            slide = {
                "slide_number": slide_number,
                "title": None if item.get("image_includes_caption") else title,
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
