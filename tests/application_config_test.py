from datetime import datetime

import freezegun
from pytz import timezone

from application_config import process_slides

display_time_zone = timezone("Pacific/Auckland")


def get_start_time():
    """Helper function to get a start time like ApplicationConfig.start_time."""
    return display_time_zone.fromutc(datetime.utcnow())


class TestProcessSlides:
    """Test suite for process_slides function."""

    def test_process_slides_returns_list(self):
        """Test that process_slides returns a list."""
        items = []
        slides = process_slides(items, display_time_zone, get_start_time())
        assert isinstance(slides, list)
        assert len(slides) == 0

    def test_process_slides_webcam_item(self):
        """Test processing of webcam items (no times array)."""
        items = [
            {"name": "Test Webcam 1", "url": "https://example.com/webcam1.jpg"},
            {"name": "Test Webcam 2", "url": "https://example.com/webcam2.jpg"},
        ]
        slides = process_slides(items, display_time_zone, get_start_time())

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

        assert slides[0]["hidden"] is False
        assert slides[1]["hidden"] is False

    @freezegun.freeze_time("2024-07-20 11:00:00")
    def test_process_slides_weather_item_with_time_zones(self):
        """Test processing of weather items with multiple times."""
        items = [
            {
                "name": "Surface Pressure",
                "url": "https://www.metservice.com/publicData/surfacePressureImage?time=%Y%m%d-%H%M-00.000&analysis=%Y%m%d-%H%M-00.000",
                "times": ["1800"],
                "time_zone": "UTC",
                "url_time_zone": "Pacific/Auckland",
                "url_offset": -12,
                "show_by_default": True,
            }
        ]
        slides = process_slides(items, display_time_zone, get_start_time())
        assert isinstance(slides, list)
        assert len(slides) == 1

        assert slides[0]["slide_number"] == 1
        assert slides[0]["title"] == "Surface Pressure 0600"
        assert slides[0]["file_name"] == "001 Surface Pressure 0600"
        assert (
            slides[0]["url"]
            == "https://www.metservice.com/publicData/surfacePressureImage?time=20240719-1800-00.000&analysis=20240719-1800-00.000"
        )
        assert slides[0]["hidden"] is False
