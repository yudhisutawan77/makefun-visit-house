#!/usr/bin/env python3
"""Copy the pre-rendered invitation image to the harness output.

Stdlib only. The entry image (entry.png, 1024x1024) sits next to this
file; this program does not re-render it, it only places a byte-identical
copy where the harness expects it: /output/entry.png.

Output resolution, in order:
  1. ENTRY_OUT       - a file path, or a directory (entry.png inside it)
  2. ENTRY_OUT_DIR   - a directory (entry.png inside it)
  3. /output/entry.png
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ENTRY_FILE = "entry.png"


def pick_output_path():
    """Decide where the image goes from the environment, with fallback."""
    explicit = os.environ.get("ENTRY_OUT")
    if explicit:
        return explicit
    out_dir = os.environ.get("ENTRY_OUT_DIR")
    if out_dir:
        return os.path.join(out_dir, ENTRY_FILE)
    return os.path.join("/output", ENTRY_FILE)


def place_entry_image(source_path, destination):
    """Copy the image, treating a directory destination as entry.png inside it.

    A destination that exists as a directory, or that has no file
    extension at all (e.g. /output), is a directory; anything with an
    extension (e.g. /output/entry.png) is a file path.
    """
    if os.path.isdir(destination) or "." not in os.path.basename(destination):
        destination = os.path.join(destination, ENTRY_FILE)
    folder = os.path.dirname(os.path.abspath(destination))
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(source_path, destination)
    return destination


def main():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(work_dir, ENTRY_FILE)
    written = place_entry_image(source, pick_output_path())
    print("wrote", written)


if __name__ == "__main__":
    main()
