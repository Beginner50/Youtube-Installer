import json
import requests
import os
import time
from pytube import YouTube, exceptions
import pathlib
import threading
import shutil

THUMBNAILS = os.listdir(pathlib.Path("Downloads\\.thumbnails"))


def search_directory(*args, files_and_folders=[], reset=False):
    """Algortithm description:
    Gets the current path and parnet from args else gets the root directory with parent 'Downloads'
    Separates folders from files and append each folder found to a folder_to_be_searched list
    """
    if reset:
        files_and_folders.clear()

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
                elif thumbnail != pathlib.Path("Icons") / "black.jpg":
                    thumbnail = pathlib.Path("Icons") / "black.jpg"
                    if not item.endswith('.mp3') and not item.endswith('.webm'):
                        convert_stream(title=item.split('.')[0], get_thumbnail=True)
                        thumbnail = pathlib.Path('Downloads\\.thumbnails') / '{}.jpg'.format(item.split('.')[0])
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
    title = stream.title
    for forbidden_character in ('|', '\\', ':', '/'):
        title = title.replace(forbidden_character, '')
    stream.download(output_path=global_settings["download_path"], filename=title)

    convert_stream(title)

    sentinel.value = 1


def convert_stream(title: str, get_thumbnail=False) -> None:
    with open('Data\\Global_Settings.json') as f:
        download_path = pathlib.Path(json.load(f)['download_path'])
    for file in os.listdir(download_path):
        if title in file:
            current_dir = pathlib.Path(os.getcwd())
            original_filename = download_path / file
            new_filename = download_path / f"{title}.mp3"

            if get_thumbnail:
                thumbnail_path = pathlib.Path(f"Downloads\\.thumbnails") / f"{title}.jpg"

                if not file.endswith('.mp3'):
                    os.system(
                        f'ffmpeg -i "{str(current_dir / original_filename)}" -ss 00:00:01.000 -vframes 1 "{str(current_dir / thumbnail_path)}"'
                    )

            if file.endswith(".webm"):
                os.system(f'ffmpeg -i "{str(current_dir / original_filename)}" "{str(current_dir / new_filename)}"')

                while not os.path.exists(new_filename):
                    time.sleep(1)
                os.unlink(original_filename)


def get_streams(container, url, sentinel) -> None:
    """Function meant to run on another processor"""
    try:
        yt = YouTube(url)
        streams = yt.streams
        title = yt.title
        for forbidden_character in ('|', '\\', ':', '/'):
            title = title.replace(forbidden_character, '')

        thumbnail_url = yt.thumbnail_url
        with open(f'Downloads\\.thumbnails\\{title}.jpg', 'wb') as f:
            f.write(requests.get(thumbnail_url).content)
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
