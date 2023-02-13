import json
import os
import time
from pytube import YouTube, exceptions
import pathlib
import threading
import shutil

THUMBNAILS = os.listdir(pathlib.Path("Downloads\\.thumbnails"))


def search_directory(*args, files_and_folders=[]):
    """Algortithm description:
    Gets the current path and parnet from args else gets the root directory with parent 'Downloads'
    Separates folders from files and append each folder found to a folder_to_be_searched list
    """

    folders_in_current_dir = []
    if not args:
        current_path, parent = pathlib.Path("Downloads"), "Downloads"
    else:
        current_path, parent = args[0], args[1]

    for item in os.listdir(current_path):
        if item != ".thumbnails":
            if os.path.isdir(current_path / item):
                files_and_folders.append(
                    {
                        "item_name": item,
                        "type": "FOLDER",
                        "path": current_path / item,
                        "thumbnail": pathlib.Path("Icons") / "folder.jpg",
                        "parent": parent,
                    }
                )
                folders_in_current_dir.append(files_and_folders[-1])
            else:
                thumbnail = "{}.jpg".format(item.split(".")[0])
                if thumbnail in THUMBNAILS:
                    thumbnail = pathlib.Path("Downloads\\.thumbnails") / thumbnail
                else:
                    thumbnail = pathlib.Path("Icons") / "black.jpg"
                files_and_folders.append(
                    {
                        "item_name": item,
                        "type": "FILE",
                        "path": current_path / item,
                        "thumbnail": thumbnail,
                        "parent": parent,
                    }
                )

    for folder in folders_in_current_dir:
        search_directory(folder["path"], folder["item_name"])

    return files_and_folders


def check_file_exists(filename) -> bool:
    if filename in os.listdir(pathlib.Path("Data")):
        return True
    return False


def create_directory(path):
    os.mkdir(path)


def move_directory(file_path, destination):
    shutil.move(file_path, destination)


def rename_directory(original_path_name, new_path_name, thumbnail):
    os.rename(original_path_name, new_path_name)

    if "folder.jpg" in str(thumbnail).split("\\")[-1]:
        return
    else:
        new_thumbnail = str(thumbnail).replace(
            str(original_path_name).split("\\")[-1], str(new_path_name).split("\\")[-1]
        )
        os.rename(thumbnail, new_thumbnail)


def delete_directory(path):
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.unlink(path)


def filter_streams(streams) -> dict:
    """Gets a quality/itag dictionary from the streams"""
    quality_itag_dict = {
        "144p": 17,
        "360p": 18,
        "720p": 22,
        "1080p": 137,
        "128kbps": 140,
        "160kbps": 251,
    }

    qualities = list(quality_itag_dict.keys())
    for quality in qualities:
        streams_with_resolution = (
            streams.filter(res=f"{quality}")
            if "kbps" not in quality
            else streams.filter(abr=f"{quality}")
        )

        if streams_with_resolution is None:
            quality_itag_dict.pop(quality)
        else:
            quality_itag_dict[quality] = streams_with_resolution[0].itag

    return quality_itag_dict


def download_stream(itag, streams, sentinel) -> None:
    """Function meant to run on another processor"""
    with open(pathlib.Path("Data\\Global_Settings.json")) as f:
        global_settings = json.load(f)

    stream = streams.get_by_itag(itag)
    stream.download(output_path=global_settings["download_path"])
    title = stream.title

    convert_stream(title)

    sentinel.value = 1


def convert_stream(title) -> None:
    for file in os.listdir("Downloads"):
        if title in file:
            original_filename = pathlib.Path("Downloads") / file
            new_filename = pathlib.Path(f"Downloads") / f"{title}.mp3"
            thumbnail_path = pathlib.Path(f"Downloads\\.thumbnails") / f"{title}.jpg"

            os.system(
                f'ffmpeg -i "{str(original_filename)}" -ss 00:00:00.000 -vframes 1 "{str(thumbnail_path)}"'
            )

            if file.endswith(".webm"):
                os.system(f'ffmpeg -i "{str(original_filename)}" "{str(new_filename)}"')

                while not os.path.exists(new_filename):
                    time.sleep(1)
                os.unlink(original_filename)


def get_streams(container, url, sentinel) -> None:
    """Function meant to run on another processor"""
    try:
        streams = YouTube(url).streams
        sentinel.value = 1

        container.put(streams)

    except exceptions.RegexMatchError:
        sentinel.value = 2


def multithread_task(decorated):
    def inner(*args, **kwargs):
        thread = threading.Thread(
            target=decorated, args=args, kwargs=kwargs, daemon=True
        )
        thread.start()

    return inner


if __name__ == "__main__":
    print(search_directory())
