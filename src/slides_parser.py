from datetime import timedelta

from pytz import timezone

# pylint: disable=too-few-public-methods


class SlidesParser:
    """
    Parses configuration items into slide dictionaries with all metadata for weatherdl.

    Args:
        items (list): List of config items to process
        display_time_zone (pytz.timezone): User's time zone for display
        start_time (datetime): Start time of application in user's time zone
    Returns:
        list: List of slide dictionaries with keys:
            - slide_number (int): Sequential number starting from 1
            - title (str|None): Slide title, null when omitting
            - file_name (str): Generated filename for download, without the extension
            - url (str): Fully processed URL ready for download
            - hidden (bool): Whether slide should be hidden
    """

    def __init__(self, items, display_time_zone, start_time):
        self.items = items
        self.display_time_zone = display_time_zone
        self.start_time = start_time

    def parse(self):
        slides = []
        slide_number = 1
        for item in self.items:
            times = item.get("times", [""])
            for time in times:
                slide = self._build_slide(item, time, slide_number)
                slides.append(slide)
                slide_number += 1
        return slides

    def _build_slide(self, item, time, slide_number):
        reference_datetime = self._get_reference_datetime(item, time)
        title = self._get_title(item, time, reference_datetime)
        file_name = self._get_file_name(slide_number, title)
        url = self._get_url(item, reference_datetime)
        hidden = self._get_hidden(item, time)
        return {
            "slide_number": slide_number,
            "title": None if item.get("image_includes_caption") else title,
            "file_name": file_name,
            "url": url,
            "hidden": hidden,
        }

    def _get_reference_datetime(self, item, time):
        if not time:
            return None
        hour = int(time[:2])
        minute = int(time[2:4])
        day_shift = int(time[5:6]) if len(time) > 5 else 0
        item_tz_name = item.get("time_zone", self.display_time_zone.zone)
        item_tz = timezone(item_tz_name)
        reference_datetime = self.start_time.astimezone(item_tz).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        ) + timedelta(days=day_shift)
        return reference_datetime

    def _get_title(self, item, time, reference_datetime):
        if reference_datetime is not None:
            day_shift = int(time[5:6]) if len(time) > 5 else 0
            title_datetime = reference_datetime.astimezone(self.display_time_zone)
            time_str = title_datetime.strftime("%H%M" if day_shift == 0 else "%H%M %A")
            return f"{item['name']} {time_str}"
        return item["name"]

    def _get_file_name(self, slide_number, title):
        return f"{slide_number:03d} {title}"

    def _get_url(self, item, reference_datetime):
        url = item["url"]
        if reference_datetime is not None:
            url_time_zone_name = item.get("url_time_zone")
            url_offset = item.get("url_offset", 0)
            if url_time_zone_name:
                url_time_zone = timezone(url_time_zone_name)
                url_time = reference_datetime.astimezone(url_time_zone)
                url_time = url_time + timedelta(hours=url_offset)
            else:
                url_time = reference_datetime + timedelta(hours=url_offset)
        else:
            url_time = self.start_time
        return url_time.strftime(url)

    def _get_hidden(self, item, time):
        show_by_default = item.get("show_by_default") and (
            item.get("show_by_default") is True
            or item.get("show_by_default").count(time) > 0
        )
        return not show_by_default
