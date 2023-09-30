import json
from datetime import datetime, timedelta
from glob import glob
from os import mkdir, path

import requests
from magic import from_buffer
from pytz import timezone

from presentation import create_pptx_from_images


class config(object):

    def __init__(self, config_file_path):
        config_file = open(config_file_path, "r")
        self.config = json.loads(config_file.read())
        config_file.close()

        self.time_zone = timezone(self.read("time_zone"))
        self.start_time = self.time_zone.fromutc(datetime.utcnow())

        img_dir_path = path.join(path.expanduser(
            '~'), *self.read("working_dir"))
        self.img_dir = self.start_time.strftime(img_dir_path)

    def read(self, key):
        return self.config[key]


def download_images(config):
    if not path.exists(config.img_dir):
        mkdir(config.img_dir)

    index = 0
    success_count = 0
    failed_items = []

    def handle_unavailable_image(exception, basename, url):
        print(f"Failed to download - {str(exception)} - {url}")
        failed_items.append(f"{basename} --- {url}")

    for item in config.read("items"):
        for time in item.get("times", [""]):
            index += 1
            basename = ' '.join(
                filter(None, [f"{index:03d}", item['name'], time]))
            if len(glob(f"{path.join(config.img_dir, basename)}*")) == 0:
                url_date_time = config.start_time
                if len(time) > 0:
                    url_date_time = url_date_time.replace(
                        hour=int(time[0:2]), minute=int(time[2:4]))
                if len(time) > 4:
                    url_date_time = url_date_time + \
                        timedelta(days=int(time[5:6]))
                if item.get("utc"):
                    url_date_time = url_date_time - url_date_time.utcoffset()
                url = url_date_time.strftime(item["url"])

                try:
                    buffer = requests.get(url)
                except Exception as e:
                    handle_unavailable_image(e, basename, url)

                mime_type = from_buffer(
                    buffer.content, mime=True).split('/')

                if mime_type[0] == "image":
                    extension = mime_type[1]
                    file_name = f"{basename}.{extension}"
                    file_path = path.join(config.img_dir, file_name)

                    file = open(file_path, "wb")
                    file.write(buffer.content)
                    file.close()

                    print(f"Success! - {file_name}")
                    success_count += 1
                else:
                    handle_unavailable_image(
                        Exception("Not an image"), basename, url)

    time_taken = config.time_zone.fromutc(
        datetime.utcnow()) - config.start_time
    print(
        f"{success_count} images downloaded in {time_taken}.\n")
    if failed_items:
        print(f"{len(failed_items)} images failed:")
        for failure in failed_items:
            print(failure)


if __name__ == "__main__":
    config = config("config.json")
    download_images(config)
    create_pptx_from_images(config.img_dir, config.read("items"))
    input("\nPress Enter to finish")
