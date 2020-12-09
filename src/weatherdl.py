import json
import datetime
import requests
import os
import magic
import pytz
import glob

class downloader(object):

    def __init__(self):
        configfile = open("config.json", "r")
        self.config = json.loads(configfile.read())
        configfile.close()
        self.tz = pytz.timezone(self.config["timezone"])
        self.startTime = self.tz.fromutc(datetime.datetime.utcnow())
        self.imgDir = os.path.join(os.getcwd(), self.startTime.strftime("Weather Images %y%m%d"))
        if not os.path.exists(self.imgDir):
            os.mkdir(self.imgDir)
        self.download()

    def download(self):
        """
        Download the images
        """
        index = 0
        successCount = 0
        failedItems = []
        for item in self.config["items"]:
            for time in item["times"]:
                index += 1
                basename = f"{index:03d} {item['name']} {time}"
                if len(glob.glob(f"{os.path.join(self.imgDir, basename)}*")) == 0:
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
                        ext = typ[1]
                        name = f"{basename}.{ext}"
                        path = os.path.join(self.imgDir, name)
                        if typ[0] != "image":
                            raise Exception("Not an image")
                        open(path, "wb").write(myfile.content)
                        print(f"Success! - {name}")
                        successCount += 1
                    except Exception as e:
                        print(f"Failed to download - {str(e)} - {url}")
                        failedItems.append(f"{name} --- {url}")
        td = self.tz.fromutc(datetime.datetime.utcnow()) - self.startTime
        print(f"{successCount} images downloaded in {td}.\n\n{len(failedItems)} images failed:")
        for fail in failedItems:
            print(fail)

if __name__ == "__main__":
    dl = downloader()