import freezegun
from pytz import timezone

from slides_parser import SlidesParser
from utils import current_time

display_time_zone = timezone("Pacific/Auckland")


class TestSlidesParser:
    """Test suite for SlidesParser class."""

    def test_returns_list(self):
        items = []
        slides = SlidesParser(
            items, display_time_zone, current_time(display_time_zone)
        ).parse()
        assert isinstance(slides, list)
        assert len(slides) == 0

    def test_webcam_item(self):
        items = [
            {"name": "Test Webcam 1", "url": "https://example.com/webcam1.jpg"},
            {"name": "Test Webcam 2", "url": "https://example.com/webcam2.jpg"},
        ]
        slides = SlidesParser(
            items, display_time_zone, current_time(display_time_zone)
        ).parse()
        assert isinstance(slides, list)
        assert len(slides) == 2
        assert slides[0]["slide_number"] == 1
        assert slides[1]["slide_number"] == 2
        assert slides[0]["title"] == "Test Webcam 1"
        assert slides[1]["title"] == "Test Webcam 2"
        assert slides[0]["file_name"] == "001 Test Webcam 1"
        assert slides[1]["file_name"] == "002 Test Webcam 2"
        assert slides[0]["url"] == "https://example.com/webcam1.jpg"
        assert slides[1]["url"] == "https://example.com/webcam2.jpg"
        assert slides[0]["hidden"] is True
        assert slides[1]["hidden"] is True

    @freezegun.freeze_time("2024-07-19 21:20:00", tz_offset=12)
    def test_with_show_by_default(self):
        items = [
            {
                "name": "Sounding",
                "image_includes_caption": True,
                # pylint: disable=line-too-long
                "url": "http://rasp.nz/rasp/regions/NZSOUTH_S+0/%Y/%Y%m%d/sounding1.curr.%H%Mlst.w2.png",
                "times": ["1200", "1300"],
                "show_by_default": ["1300"],
            }
        ]
        start_time = current_time(display_time_zone)
        assert (
            start_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            == "2024-07-20 09:20:00 NZST+1200"
        )
        slides = SlidesParser(items, display_time_zone, start_time).parse()
        assert isinstance(slides, list)
        assert len(slides) == 2
        assert slides[0]["slide_number"] == 1
        assert slides[0]["title"] is None
        assert slides[0]["file_name"] == "001 Sounding 1200"
        assert (
            slides[0]["url"]
            == "http://rasp.nz/rasp/regions/NZSOUTH_S+0/2024/20240720/sounding1.curr.1200lst.w2.png"
        )
        assert slides[0]["hidden"] is True
        assert slides[1]["slide_number"] == 2
        assert slides[1]["title"] is None
        assert slides[1]["file_name"] == "002 Sounding 1300"
        assert (
            slides[1]["url"]
            == "http://rasp.nz/rasp/regions/NZSOUTH_S+0/2024/20240720/sounding1.curr.1300lst.w2.png"
        )
        assert slides[1]["hidden"] is False

    weather_items = [
        {
            "name": "Surface Pressure",
            # pylint: disable=line-too-long
            "url": "https://www.metservice.com/publicData/surfacePressureImage?time=%Y%m%d-%H%M-00.000&analysis=%Y%m%d-%H%M-00.000",
            "times": ["1800"],
            "time_zone": "UTC",
            "url_time_zone": "Pacific/Auckland",
            "url_offset": -12,
            "show_by_default": True,
        }
    ]

    @freezegun.freeze_time("2024-07-19 21:20:00", tz_offset=12)
    def test_weather_item_nzst(self):
        start_time = current_time(display_time_zone)
        assert (
            start_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            == "2024-07-20 09:20:00 NZST+1200"
        )
        slides = SlidesParser(self.weather_items, display_time_zone, start_time).parse()
        assert isinstance(slides, list)
        assert len(slides) == 1
        assert slides[0]["slide_number"] == 1
        assert slides[0]["title"] == "Surface Pressure 0600"
        assert slides[0]["file_name"] == "001 Surface Pressure 0600"
        assert (
            slides[0]["url"]
            # pylint: disable=line-too-long
            == "https://www.metservice.com/publicData/surfacePressureImage?time=20240719-1800-00.000&analysis=20240719-1800-00.000"
        )
        assert slides[0]["hidden"] is False

    @freezegun.freeze_time("2024-01-19 20:20:00", tz_offset=13)
    def test_weather_item_nzdt(self):
        start_time = current_time(display_time_zone)
        assert (
            start_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            == "2024-01-20 09:20:00 NZDT+1300"
        )
        slides = SlidesParser(self.weather_items, display_time_zone, start_time).parse()
        assert isinstance(slides, list)
        assert len(slides) == 1
        assert slides[0]["slide_number"] == 1
        assert slides[0]["title"] == "Surface Pressure 0700"
        assert slides[0]["file_name"] == "001 Surface Pressure 0700"
        assert (
            slides[0]["url"]
            # pylint: disable=line-too-long
            == "https://www.metservice.com/publicData/surfacePressureImage?time=20240119-1900-00.000&analysis=20240119-1900-00.000"
        )
        assert slides[0]["hidden"] is False

    @freezegun.freeze_time("2024-01-19 20:20:00", tz_offset=13)
    def test_with_day_shift(self):
        items = [
            {
                "name": "Surface Pressure",
                # pylint: disable=line-too-long
                "url": "https://www.metservice.com/publicData/surfacePressureImage?time=%Y%m%d-%H%M-00.000&analysis=%Y%m%d-%H%M-00.000",
                "times": ["1200+1"],
                "time_zone": "UTC",
                "url_time_zone": "Pacific/Auckland",
                "url_offset": -12,
                "show_by_default": True,
            }
        ]
        start_time = current_time(display_time_zone)
        assert (
            start_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            == "2024-01-20 09:20:00 NZDT+1300"
        )
        slides = SlidesParser(items, display_time_zone, start_time).parse()
        assert isinstance(slides, list)
        assert len(slides) == 1
        assert slides[0]["slide_number"] == 1
        assert slides[0]["title"] == "Surface Pressure 0100 Sunday"
        assert slides[0]["file_name"] == "001 Surface Pressure 0100 Sunday"
        assert (
            slides[0]["url"]
            # pylint: disable=line-too-long
            == "https://www.metservice.com/publicData/surfacePressureImage?time=20240120-1300-00.000&analysis=20240120-1300-00.000"
        )
        assert slides[0]["hidden"] is False
