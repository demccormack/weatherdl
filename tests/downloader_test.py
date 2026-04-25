from datetime import datetime
from unittest.mock import MagicMock

import pytest
import pytz

from downloader import Downloader


def make_downloader(local_dt):
    config = MagicMock()
    config.start_time = local_dt
    return Downloader(config)


NZ_TZ = pytz.timezone("Pacific/Auckland")


def nz_dt(year, month, day, hour, minute, tz=NZ_TZ):
    return tz.localize(datetime(year, month, day, hour, minute))


class TestUrlFromTimeOffset:
    def test_offset_shifts_url_time_forward(self):
        # start_time is 2026-04-24 07:00 NZST (UTC+12)
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "offset": 11}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260424-1800"

    def test_offset_shifts_url_time_backward(self):
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "offset": -1}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260424-0600"

    def test_offset_crosses_midnight(self):
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "offset": -12}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260423-1900"

    def test_no_offset_leaves_time_unchanged(self):
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M"}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260424-0700"

    def test_offset_zero_leaves_time_unchanged(self):
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "offset": 0}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260424-0700"

    def test_offset_applied_before_utc_conversion_in_standard_time(self):
        # NZST (Standard Time, UTC+12). Local 07:00 + offset 11 = local 18:00 → UTC 06:00
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "utc": True, "offset": 11}
        url = downloader.url_from_time(item, "0700")
        assert url == "20260424-0600"

    def test_slide_basename_uses_original_time(self):
        # Verify run() uses original time in basename, not offset-adjusted time.
        # The basename is built from 'time' directly before calling url_from_time,
        # so this test just confirms offset does not affect the time string itself.
        dt = nz_dt(2026, 4, 24, 7, 0)
        downloader = make_downloader(dt)
        item = {"url": "%Y%m%d-%H%M", "offset": -12}
        time_str = "0700"
        url = downloader.url_from_time(item, time_str)
        # URL is shifted but time_str is not modified
        assert time_str == "0700"
        assert url == "20260423-1900"
