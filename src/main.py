from application_config import ApplicationConfig
from downloader import Downloader
from briefing import create_pptx_from_images

if __name__ == "__main__":
    config = ApplicationConfig("config.json")
    Downloader(config).run()
    create_pptx_from_images(config.img_dir, config.items)
    input("\nPress Enter to finish")
