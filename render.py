#!/usr/bin/env python3
"""Render page.html (the 43-story front page) to entry.png with the
headless Chromium shell bundled with Playwright, then verify the
result: exactly 1024x1024, a PNG, under the 1 MiB cap.

The entry program (main.ts) only copies entry.png to /output; this
script runs at build time on the author's machine, never in the
harness, so the submitted image is byte-stable.
"""

import glob
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def find_browser():
    candidates = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
    for path in sorted(candidates):
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    raise FileNotFoundError("no headless Chromium shell found under ~/.cache/ms-playwright")


def main():
    browser = find_browser()
    page = os.path.join(HERE, "page.html")
    out = os.path.join(HERE, "entry.png")
    cmd = [
        browser, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--window-size=1024,1024",
        f"--screenshot={out}", f"file://{page}",
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    with Image.open(out) as im:
        assert im.size == (1024, 1024), f"unexpected size {im.size}"
        assert im.format == "PNG", f"unexpected format {im.format}"
    size = os.path.getsize(out)
    print(f"wrote {out} 1024x1024 {size} bytes")
    assert size <= 1048576, "entry.png over the 1 MiB cap"


if __name__ == "__main__":
    sys.exit(main())
