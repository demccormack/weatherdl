import sys
from os import path


def get_config_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # PyInstaller bundle
        config_dir = path.dirname(path.abspath(sys.executable))
    else:
        # Python script
        config_dir = path.dirname(path.dirname(path.abspath(__file__)))

    return path.join(config_dir, "config.json")


def unused_file_name_like(name, dir_listing):
    if name not in dir_listing:
        return name

    i = 1
    parts = path.splitext(name)
    while "".join([f"{parts[0]} ({i})", parts[1]]) in dir_listing:
        i = i + 1

    return "".join([f"{parts[0]} ({i})", parts[1]])
