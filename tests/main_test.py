from os import path
from shutil import rmtree

import pytest
from pptx import Presentation

from application_config import ApplicationConfig
from main import run

temp_dir = path.join("tests", "test_run")


@pytest.fixture(autouse=True)
def teardown():
    yield temp_dir

    if path.exists(temp_dir):
        rmtree(temp_dir)


def test_it_creates_expected_files():
    config = ApplicationConfig(path.join("tests", "fixtures", "config.json"))
    config.img_dir = temp_dir

    run(config)
    assert path.isfile(path.join(temp_dir, "001 Flying to Mt Cook.jpeg"))
    assert path.isfile(path.join(temp_dir, "briefing.pptx"))

    pres = Presentation(path.join(temp_dir, "briefing.pptx"))
    assert len(pres.slides) == 1
