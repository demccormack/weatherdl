from application_config import ApplicationConfig
from downloader import Downloader
from briefing import Briefing


def run(config):
    Downloader(config).run()
    Briefing(config).save_as('briefing.pptx')


if __name__ == "__main__":
    app_config = ApplicationConfig("config.json")
    run(app_config)
    input("\nPress Enter to finish")
