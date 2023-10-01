from os import path
from shutil import rmtree

import pytest

from application_config import ApplicationConfig
from downloader import Downloader
from presentation import create_pptx_from_images

temp_dir = path.join("tests", "test_run")


@pytest.fixture(autouse=True)
def teardown():
    yield temp_dir

    if path.exists(temp_dir):
        rmtree(temp_dir)


def test_it_creates_expected_files():
    config = ApplicationConfig(path.join("tests", "fixtures", "config.json"))
    config.img_dir = temp_dir

    Downloader(config).run()
    assert path.isfile(path.join(temp_dir, "001 Flying to Mt Cook.jpeg"))

    create_pptx_from_images(config.img_dir, config.items)
    assert path.isfile(path.join(temp_dir, "briefing.pptx"))
