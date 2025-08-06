import os
import shutil

from copy_directory import copy_directory
from generate_page import generate_page


def main():
    source = "./static"
    dest = "./public"

    print(f"Removing '{dest}' directory")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    copy_directory(source, dest)

    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
