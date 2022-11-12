import json
from datetime import datetime, timedelta
from glob import glob
from os import getcwd, mkdir, path

import requests
from magic import from_buffer
from pptx import Presentation
from pytz import timezone


class downloader(object):

    def __init__(self):
        config_file = open("config.json", "r")
        self.config = json.loads(config_file.read())
        config_file.close()
        self.time_zone = timezone(self.config["timezone"])
        self.start_time = self.time_zone.fromutc(datetime.utcnow())
        self.img_dir = path.join(
            getcwd(), self.start_time.strftime("Weather Images %y%m%d"))
        if not path.exists(self.img_dir):
            mkdir(self.img_dir)
        self.download()

    def download(self):
        """
        Download the images
        """
        index = 0
        success_count = 0
        failed_items = []
        for item in self.config["items"]:
            for time in item["times"]:
                index += 1
                basename = ' '.join(
                    filter(None, [f"{index:03d}", item['name'], time]))
                if len(glob(f"{path.join(self.img_dir, basename)}*")) == 0:
                    try:
                        url_date_time = self.start_time
                        if len(time) > 0:
                            url_date_time = url_date_time.replace(
                                hour=int(time[0:2]), minute=int(time[2:4]))
                        if len(time) > 4:
                            url_date_time = url_date_time + \
                                timedelta(days=int(time[5:6]))
                        if int(item["utc"]):
                            url_date_time = url_date_time - url_date_time.utcoffset()
                        url = url_date_time.strftime(item["url"])

                        buffer = requests.get(url)
                        mime_type = from_buffer(
                            buffer.content, mime=True).split('/')
                        extension = mime_type[1]
                        file_name = f"{basename}.{extension}"
                        file_path = path.join(self.img_dir, file_name)
                        if mime_type[0] != "image":
                            raise Exception("Not an image")

                        open(file_path, "wb").write(buffer.content)

                        print(f"Success! - {file_name}")
                        success_count += 1
                    except Exception as e:
                        print(f"Failed to download - {str(e)} - {url}")
                        failed_items.append(f"{basename} --- {url}")

        time_taken = self.time_zone.fromutc(
            datetime.utcnow()) - self.start_time
        print(
            f"{success_count} images downloaded in {time_taken}.\n\n{len(failed_items)} images failed:")
        for failure in failed_items:
            print(failure)


def create_presentation():
    prs = Presentation()


if __name__ == "__main__":
    dl = downloader()
    create_presentation()
