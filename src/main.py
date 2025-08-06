import os
import shutil
import sys

from copy_directory import copy_directory
from generate_page import generate_page_recursive


def main():
    source = "./static"
    dest = "./docs"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print(f"Removing '{dest}' directory")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    copy_directory(source, dest)

    generate_page_recursive("./content", "./template.html", dest, basepath)


if __name__ == "__main__":
    main()
