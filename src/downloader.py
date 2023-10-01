from datetime import datetime, timedelta
from glob import glob
from os import mkdir, path

import requests
from magic import from_buffer

# pylint: disable=missing-function-docstring


class Downloader:
    """
    Class for downloading images from specified sources using configurations.

    Attributes:
        config (ApplicationConfig)
    """

    def __init__(self, config):
        self.config = config
        self.success_count = 0
        self.failed_items = []

    def handle_unavailable_image(self, exception, basename, url):
        print(f"Failed to download - {str(exception)} - {url}")
        self.failed_items.append(f"{basename} --- {url}")

    def file_exists_with_basename(self, basename):
        allowed_names = f"{path.join(self.config.img_dir, basename)}*"
        return len(glob(allowed_names)) > 0

    def is_provided(self, time):
        return len(time) > 0

    def includes_day_shift(self, time):
        return len(time) > 4

    def run(self):
        img_dir = self.config.img_dir
        if not path.exists(img_dir):
            mkdir(img_dir)

        index = 0

        for item in self.config.items:
            is_utc = item.get("utc")
            url_from_config = item.get("url")

            for time in item.get("times", [""]):
                index += 1

                padded_slide_number = f"{index:03d}"
                slide_name = item['name']
                basename = ' '.join(
                    filter(None, [padded_slide_number, slide_name, time]))

                if not self.file_exists_with_basename(basename):
                    date_time_for_url = self.config.start_time

                    if self.is_provided(time):
                        hour = int(time[0:2])
                        minute = int(time[2:4])
                        date_time_for_url = date_time_for_url.replace(
                            hour=hour, minute=minute)

                    if self.includes_day_shift(time):
                        days = int(time[5:6])
                        date_time_for_url = date_time_for_url + \
                            timedelta(days=days)

                    if is_utc:
                        date_time_for_url -= date_time_for_url.utcoffset()

                    url = date_time_for_url.strftime(url_from_config)

                    buffer = None
                    try:
                        buffer = requests.get(url)
                    except Exception as e:
                        self.handle_unavailable_image(e, basename, url)
                        continue

                    mime_type = from_buffer(
                        buffer.content, mime=True).split('/')

                    if mime_type[0] == "image":
                        extension = mime_type[1]
                        file_name = f"{basename}.{extension}"
                        file_path = path.join(self.config.img_dir, file_name)

                        file = open(file_path, "wb")
                        file.write(buffer.content)
                        file.close()

                        print(f"Success! - {file_name}")
                        self.success_count += 1
                    else:
                        self.handle_unavailable_image(
                            Exception("Not an image"), basename, url)

        time_taken = self.config.time_zone.fromutc(
            datetime.utcnow()) - self.config.start_time
        print(
            f"{self.success_count} images downloaded in {time_taken}.\n")
        if self.failed_items:
            print(f"{len(self.failed_items)} images failed:")
            for failure in self.failed_items:
                print(failure)
