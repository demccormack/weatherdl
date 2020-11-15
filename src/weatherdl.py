import json
import datetime
import requests
import os
import magic
import pytz

class downloader(object):

    def __init__(self):
        configfile = open("config.json", "r")
        self.config = json.loads(configfile.read())
        configfile.close()
        self.tz = pytz.timezone(self.config["timezone"])
        self.startTime = self.tz.fromutc(datetime.datetime.utcnow())
        self.imgDir = os.path.join(os.getcwd(), "Images")
        self.download()

    def download(self):
        """
        Download the images
        """
        index = 1
        failCount = 0
        for item in self.config["items"]:
            for time in item["times"]:
                try:
                    dt = self.startTime
                    if len(time) > 0:
                        dt = dt.replace(hour=int(time[0:2]), minute=int(time[2:4]))
                        if len(time) > 4:
                            dt = dt + datetime.timedelta(days=int(time[5:6]))
                    if int(item["utc"]):
                        dt = dt - dt.utcoffset()
                    url = dt.strftime(item["url"])
                    myfile = requests.get(url)
                    typ = magic.from_buffer(myfile.content, mime=True).split('/')
                    if typ[0] != "image":
                        raise Exception("Not an image")
                    ext = typ[1]
                    name = f"{index:03d} {item['name']} {time}.{ext}"
                    path = os.path.join(self.imgDir, name)
                    open(path, "wb").write(myfile.content)
                    print(f"Success! - {name}")
                    index += 1
                except Exception as e:
                    print(f"Failed to download - {str(e)} - {url}")
                    failCount += 1
        td = self.tz.fromutc(datetime.datetime.utcnow()) - self.startTime
        print(f"{str(index - 1)} images downloaded, {failCount} failed, in {str(td)}")

if __name__ == "__main__":
    dl = downloader()