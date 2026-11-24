#!/usr/bin/env python3
"""Entry point for the news-image-20261124 make.fun bounty.

Copies the committed poster.png (1024x1024, one image summing up
24 November 2026's world news) to /output/entry.png.
Standard library only; resolves the poster from this script's own
directory so it works from any working directory.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER = os.path.join(HERE, "poster.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1024 * 1024  # gate: at most 1 MiB
MAX_DIM = 1024           # gate: at most 1024x1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def validate(path):
    """Self-check the poster against the bounty gate before copying.

    Returns a list of problems (empty when the file is acceptable):
    PNG signature, 1 MiB size cap, and IHDR dimensions within
    1024x1024.
    """
    problems = []
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        problems.append(f"file too large: {size} > {MAX_BYTES} bytes")
    with open(path, "rb") as fh:
        head = fh.read(33)
    if not head.startswith(PNG_SIG):
        problems.append("missing PNG signature")
    elif len(head) >= 33 and head[12:16] == b"IHDR":
        width, height = struct.unpack(">II", head[16:24])
        if width > MAX_DIM or height > MAX_DIM:
            problems.append(
                f"dimensions {width}x{height} exceed {MAX_DIM}x{MAX_DIM}")
    else:
        problems.append("missing IHDR chunk")
    return problems


def main():
    if not os.path.isfile(POSTER):
        print(f"poster not found: {POSTER}", file=sys.stderr)
        return 1
    problems = validate(POSTER)
    if problems:
        for problem in problems:
            print(f"invalid poster: {problem}", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(POSTER, OUT)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
