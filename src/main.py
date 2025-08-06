import os
import shutil

from copy_directory import copy_directory


def main():
    source = "./static"
    dest = "./public"

    print(f"Removing '{dest}' directory")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    copy_directory(source, dest)


if __name__ == "__main__":
    main()
