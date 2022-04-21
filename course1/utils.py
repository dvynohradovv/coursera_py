"""
Всячина.
"""
import re


def is_number(str):
    if str is None:
        return False
    try:
        float(str)
        return True
    except ValueError:
        return False


def is_int(str):
    if str is None:
        return False
    try:
        int(str)
        return True
    except ValueError:
        return False


def is_photo(path, extensions={".jpeg", ".tif", ".png", ".jfif"}):
    return any(path.endswith(ext) for ext in extensions)
    """
    {file: any(file.endswith(ext) for ext in extensions) for file in files}
    files = {"a_movie.mkv", "an_image.png",
             "a_movie_without_extension", "an_image_without_extension"}
    extensions = {".jpg", ".png", ".gif"} etc {'a_movie_without_extension': False, 'an_image.png': True 'an_image_without_extension': False, 'a_movie.mkv': False}
    """


def get_file_ext(file):
    fileExtentionRegex = re.compile(r'^(.+)(\..+)$')
    extention = fileExtentionRegex.search(file)
    return extention.group(2)


def get_file_name(file):
    fileExtentionRegex = re.compile(r'^(.+)(\..+)$')
    extention = fileExtentionRegex.search(file)
    return extention.group(1)
