"""PyInstaller runtime: bundled ffmpeg for one-file exe."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap_ffmpeg() -> None:
    if not getattr(sys, "frozen", False):
        return
    meipass = getattr(sys, "_MEIPASS", None)
    if not meipass:
        return
    for exe in Path(meipass).rglob("ffmpeg-win*.exe"):
        if exe.is_file():
            os.environ["IMAGEIO_FFMPEG_EXE"] = str(exe)
            break


_bootstrap_ffmpeg()
