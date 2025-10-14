import os
from application_config import ApplicationConfig
from downloader import Downloader
from briefing import Briefing


def run(config):
    Downloader(config).run()
    Briefing(config).save_as("briefing.pptx")


if __name__ == "__main__":
    # Find config.json relative to the script location, not the current working directory
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(script_dir, "config.json")
    app_config = ApplicationConfig(config_path)
    run(app_config)
    input("\nPress Enter to finish")
