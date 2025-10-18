from application_config import ApplicationConfig
from briefing import Briefing
from downloader import Downloader
from utils import get_config_path


def run(config):
    Downloader(config).run()
    Briefing(config).save_as("briefing.pptx")


if __name__ == "__main__":
    app_config = ApplicationConfig(get_config_path())
    run(app_config)
    input("\nPress Enter to finish")
