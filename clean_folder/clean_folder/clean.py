import re
import shutil
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j",
    "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja"
)

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


images = list()
audio = list()
video = list()
documents = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": images, "PNG": images, "JPG": images, "GIF": images, "TXT": documents,
    "PDF": documents, "DOC": documents, "DOCX": documents, "XLSX": documents, "ZIP": archives, "GZ": archives,
    "TAR": archives
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("images", "audio", "video", "documents", "archives"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"Image: {images}\n")
    print(f"Audio: {audio}\n")
    print(f"Video: {video}\n")
    print(f"Document: {documents}\n")
    print(f"Archive: {archives}\n")
    print(f"Unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")


def handle_file(path, root_folder, dist):
    if path.exists():
        target_folder = root_folder / dist
        target_folder.mkdir(exist_ok=True)
        path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.stem)

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return

    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main():
    path = sys.argv[1]
    print(f"Start in {path}")
    folder_path = Path(path)

    scan(folder_path)

    for file in images:
        handle_file(file, folder_path, "images")

    for file in audio:
        handle_file(file, folder_path, "audio")

    for file in video:
        handle_file(file, folder_path, "video")

    for file in documents:
        handle_file(file, folder_path, "documents")

    for file in others:
        handle_file(file, folder_path, "others")

    for file in archives:
        handle_archive(file, folder_path, "archives")

    get_folder_objects(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')
    arg = Path(path)
    main()