import sys
from pathlib import Path


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
    "JPEG": images, "PNG": images, "JPG": images, "GIF": images,
    "TXT": documents, "PDF": documents, "DOC": documents, "DOCX": documents, "XLSX": documents,
    "ZIP": archives, "GZ": archives, "TAR": archives
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
        new_name = folder/item.name
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