#!/usr/bin/env python3
"""Render the front page to entry.png and verify it.

Uses the headless Chromium shell bundled with Playwright to screenshot
page.html at 1024x1024, then checks the result is a PNG of exactly
1024x1024 pixels and under the 1 MiB cap. Also writes 300 px and 512 px
downscales to /tmp for legibility checks.

The entry program (main.ts) only copies entry.png to /output; this
script runs at build time on the author's machine, never in the
harness, so the submitted image is byte-stable.
"""

import glob
import hashlib
import os
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ROOT, "page.html")
IMAGE = os.path.join(ROOT, "entry.png")


def locate_shell():
    pattern = os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")
    for candidate in sorted(glob.glob(pattern)):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise FileNotFoundError("no headless Chromium shell under ~/.cache/ms-playwright")


def screenshot(shell):
    command = [
        shell, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--window-size=1024,1024",
        f"--screenshot={IMAGE}", f"file://{PAGE}",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def verify():
    with Image.open(IMAGE) as picture:
        assert picture.size == (1024, 1024), f"unexpected size {picture.size}"
        assert picture.format == "PNG", f"unexpected format {picture.format}"
        picture.resize((300, 300), Image.LANCZOS).save("/tmp/thumb300.png")
        picture.resize((512, 512), Image.LANCZOS).save("/tmp/half512.png")
    size = os.path.getsize(IMAGE)
    digest = hashlib.sha256(open(IMAGE, "rb").read()).hexdigest()
    print(f"wrote {IMAGE} 1024x1024 {size} bytes sha256 {digest}")
    assert size <= 1048576, "entry.png over the 1 MiB cap"


def main():
    screenshot(locate_shell())
    verify()


if __name__ == "__main__":
    sys.exit(main())
