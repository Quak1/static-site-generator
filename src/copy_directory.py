import os
import shutil


def copy_directory(source, dest):
    if not os.path.exists(source):
        raise Exception("Source directory doesn't exist")

    if not os.path.exists(dest):
        os.mkdir(dest)

    print(f"Copying directory '{source}' to '{dest}'")
    for entry in os.listdir(source):
        path = os.path.join(source, entry)
        if os.path.isfile(path):
            shutil.copy(path, dest)
        else:
            dest_path = os.path.join(dest, entry)
            copy_directory(path, dest_path)
