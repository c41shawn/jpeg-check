#!/usr/bin/env python3
"""
jpeg_check.py  -  READ-ONLY JPEG checker. Never changes any file.

Needs Python 3 plus two free libraries:  pip install pillow numpy

Run:   python3 jpeg_check.py /path/to/folder
Extras (all optional):
   --subfolders   also check JPEGs inside folders within the folder
   --no-light     hide the LIGHT% column
   --no-hex       hide the hex (#rrggbb) values

Every number is measured at full size (no shrinking), on brightness
(a grey scale of 0-255). Hex values are that same brightness written as
a grey color: brightness 63 = #3f3f3f. They are NOT the photo's colors.

Files are listed in sets (a blank line between sets). A set is every file
whose name starts the same, up to the first - _ space or dot:
   03-siste.jpg, 03-siste-final.jpg  ->  one set
Change SET_SPLIT below if your naming works differently.

JPEG only. There is no pass/fail. Compare photos to each other.
Tip: the table is wide. Widen your Terminal window before running.
"""

import os
import re
import sys
import io
from PIL import Image, ImageCms
import numpy as np

Image.MAX_IMAGE_PIXELS = None

DARK_MAX = 63      # shadows    = brightness 0-63    (#000000-#3f3f3f)
LIGHT_MIN = 192    # highlights = brightness 192-255 (#c0c0c0-#ffffff)
FILE_W = 28        # width of the FILE column
PROF_W = 18        # width of the PROFILE column
COL_W = 12         # width of every number column (all the same)
SET_SPLIT = r"[-_ .]"  # a 'set' = files whose names start the same, up to the
                       # first - _ space or . (e.g. 03-a.jpg, 03-a-final.jpg)


def hexgrey(v):
    return "#" + f"{int(v):02x}" * 3


def profile_name(img):
    data = img.info.get("icc_profile")
    if not data:
        return "none"
    try:
        prof = ImageCms.ImageCmsProfile(io.BytesIO(data))
        return ImageCms.getProfileDescription(prof).strip()
    except Exception:
        return "unreadable"


def check(path):
    with Image.open(path) as img:
        prof = profile_name(img)
        gray = np.array(img.convert("L"))
    total = gray.size
    black = np.sum(gray == 0) / total * 100
    white = np.sum(gray == 255) / total * 100
    dark = np.sum(gray <= DARK_MAX) / total * 100
    light = np.sum(gray >= LIGHT_MIN) / total * 100
    median = int(np.median(gray))

    shadows = np.unique(gray[gray <= DARK_MAX])
    gaps = int((shadows.max() - shadows.min() + 1) - len(shadows)) if len(shadows) > 1 else 0
    return prof, black, white, gaps, median, dark, light


def find_files(folder, subfolders):
    out = []
    if subfolders:
        for root, _, names in os.walk(folder):
            for n in names:
                if n.lower().endswith((".jpg", ".jpeg")):
                    out.append(os.path.join(root, n))
    else:
        for n in os.listdir(folder):
            if n.lower().endswith((".jpg", ".jpeg")):
                out.append(os.path.join(folder, n))
    return sorted(out)


def main():
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("--")}
    paths = [a for a in args if not a.startswith("--")]
    known = {"--subfolders", "--no-light", "--no-hex"}

    if len(paths) != 1 or not os.path.isdir(paths[0]) or not flags <= known:
        print(__doc__)
        sys.exit(1)

    hx = "--no-hex" not in flags
    show_light = "--no-light" not in flags
    sub = "--subfolders" in flags
    files = find_files(paths[0], sub)
    if not files:
        print("No JPEGs found in that folder.")
        return

    # Stacked headers: one list of short lines per column. Order = importance.
    cols = [
        ["BLACK%", "pure black", "(level 0)"],
        ["WHITE%", "pure white", "(level 255)"],
        ["GAPS", "missing", "shadow steps", "0 = smooth"],
        ["MEDIAN", "middle level", "0-255" + (" + hex" if hx else "")],
        ["DARK%", "levels", "0-63"] + (["#000000-", "#3f3f3f"] if hx else []),
    ]
    if show_light:
        cols.append(["LIGHT%", "levels", "192-255"] + (["#c0c0c0-", "#ffffff"] if hx else []))

    height = max(len(c) for c in cols)
    left = [["FILE"], ["PROFILE", "(none = untagged)"]]
    # bottom-align: every column's last line sits right above the === line
    def pad(c):
        return [""] * (height - len(c)) + c
    left = [pad(c) for c in left]
    cols = [pad(c) for c in cols]
    head_lines = []
    for i in range(height):
        line = f"{left[0][i]:<{FILE_W}} {left[1][i]:<{PROF_W}}"
        for c in cols:
            line += f" {c[i]:^{COL_W}}"
        head_lines.append(line.rstrip())
    width = max(len(l) for l in head_lines)

    print()
    for l in head_lines:
        print(l)
    print("=" * width)

    prev_key = None
    for p in files:
        stem = re.split(SET_SPLIT, os.path.basename(p), maxsplit=1)[0].lower()
        key = (os.path.dirname(p), stem)
        if prev_key is not None and key != prev_key:
            print()
        prev_key = key
        name = os.path.relpath(p, paths[0]) if sub else os.path.basename(p)
        try:
            prof, b, w, g, m, d, l = check(p)
            row = f"{name[:FILE_W]:<{FILE_W}} {prof[:PROF_W]:<{PROF_W}}"
            vals = [f"{b:.2f}", f"{w:.2f}", f"{g}",
                    f"{m} {hexgrey(m)}" if hx else f"{m}", f"{d:.1f}"]
            if show_light:
                vals.append(f"{l:.1f}")
            for v in vals:
                row += f" {v:^{COL_W}}"
            print(row)
        except Exception as e:
            print(f"{name[:FILE_W]:<{FILE_W}} ERROR: {e}")
    print()


if __name__ == "__main__":
    main()


