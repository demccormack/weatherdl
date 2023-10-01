from os import path

from application_config import ApplicationConfig
from downloader import Downloader
from presentation import create_pptx_from_images


def test_it_creates_expected_files():
    config = ApplicationConfig(path.join("tests", "fixtures", "config.json"))
    config.img_dir = path.join("tests", "test_run")

    Downloader(config).run()
    assert path.isfile(path.join("tests", "test_run", "sample.jpg"))

    create_pptx_from_images(config.img_dir, config.items)
    assert path.isfile(path.join("tests", "test_run", "briefing.pptx"))
