import json
import os
import zlib


real_path = os.path.realpath(__file__)
PATH_DIR = os.path.dirname(real_path)
REPORTS_ALLOWED = os.path.join(PATH_DIR, "__allowed.txt")
REPORTS_PRIVATE = os.path.join(PATH_DIR, "__private.txt")

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def new_folder_path(root, name):
    new_folder = os.path.join(root, name)
    create_folder(new_folder)
    return new_folder

def create_new_folders(root, *names):
    for name in names:
        new_folder_path(root, name)

def fix_extention(ext: str):
    if ext[0] == '.':
        return ext
    return f".{ext}"

def add_extention(path: str, ext=None):
    if ext is not None:
        ext = fix_extention(ext)
        if not path.endswith(ext):
            path = path.split('.')[0]
            return f"{path}{ext}"
    return path

def save_backup(path):
    if os.path.isfile(path):
        old = f"{path}.old"
        if os.path.isfile(old):
            os.remove(old)
        os.rename(path, old)

def json_read(path: str):
    path = add_extention(path, '.json')
    try:
        with open(path) as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def json_read_no_exception(path: str):
    path = add_extention(path, '.json')
    with open(path) as file:
        return json.load(file)

def json_write(path: str, data, backup=False, indent=2, sep=None):
    path = add_extention(path, '.json')
    if backup:
        save_backup(path)
    with open(path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, default=sorted, indent=indent, separators=sep)


def bytes_read(path: str, ext=None):
    path = add_extention(path, ext)
    try:
        with open(path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return b''

def bytes_write(path: str, data: bytes, ext=None):
    path = add_extention(path, ext)
    with open(path, 'wb') as file:
        file.write(data)


def zlib_decompress(data: bytes):
    return zlib.decompress(data)

def zlib_text_read(path: str):
    path = add_extention(path, '.zlib')
    data_raw = bytes_read(path)
    data = zlib_decompress(data_raw)
    return data.decode()


def file_read(path: str, ext=None):
    path = add_extention(path, ext)
    # try:
    #     raw = bytes_read(path, ext)
    #     return raw.decode()
    # except Exception as e:
    #     print(f"[file_read] {e}")

    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def file_write(path: str, data: str, ext=None):
    path = add_extention(path, ext)
    with open(path, 'w') as f:
        f.write(data)


def get_folders(path) -> list[str]:
    return sorted(next(os.walk(path))[1])

def get_files(path) -> list[str]:
    return sorted(next(os.walk(path))[2])

def get_all_files(path=None, ext=None):
    if path is None:
        path = '.'
    files = get_files(path)
    if ext is None:
        return files
    ext = fix_extention(ext)
    return [file for file in files if file.endswith(ext)]

def get_logs_filter(filter_file: str):
    return file_read(filter_file).splitlines()

def get_folders_filter(folders: list[str], filter_str: str=None, private_only=True):
    if filter_str is not None:
        folders = [name for name in folders if filter_str in name]
    if private_only:
        filter_list = get_logs_filter(REPORTS_PRIVATE)
        folders = [name for name in folders if name not in filter_list]
    return folders