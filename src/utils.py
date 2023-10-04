from os import path


def unused_file_name_like(name, dir_listing):
    if name not in dir_listing:
        return name

    i = 1
    parts = path.splitext(name)
    while ''.join([f"{parts[0]} ({i})", parts[1]]) in dir_listing:
        i = i + 1

    return ''.join([f"{parts[0]} ({i})", parts[1]])
