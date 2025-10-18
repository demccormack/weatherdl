import os
import sys

from application_config import ApplicationConfig
from briefing import Briefing
from downloader import Downloader


def run(config):
    Downloader(config).run()
    Briefing(config).save_as("briefing.pptx")


if __name__ == "__main__":
    # Handle different execution contexts:
    # - When running as Python script: look for config in repository root
    # - When running as PyInstaller executable: look in same directory as executable
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running as PyInstaller bundle - config should be next to executable
        executable_dir = os.path.dirname(os.path.abspath(sys.executable))
        config_path = os.path.join(executable_dir, "config.json")
    else:
        # Running as Python script - config is in repository root
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(script_dir, "config.json")

    app_config = ApplicationConfig(config_path)
    run(app_config)
    input("\nPress Enter to finish")
