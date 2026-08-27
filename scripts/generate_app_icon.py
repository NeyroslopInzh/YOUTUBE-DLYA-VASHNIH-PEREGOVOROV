#!/usr/bin/env python3
"""Generate multi-size .ico from Uzbek flag for Windows exe/installer."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("pip install Pillow") from exc

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from uzbek_flag import draw_uzbekistan_icon  # noqa: E402

OUT = ROOT / "assets" / "app.ico"
OUT_PNG = ROOT / "assets" / "app_icon.png"
SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    master = draw_uzbekistan_icon(256).convert("RGBA")
    master.save(OUT_PNG, format="PNG")

    # Pillow сам даунскейлит master под каждый size в ICO
    master.save(OUT, format="ICO", sizes=SIZES)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
