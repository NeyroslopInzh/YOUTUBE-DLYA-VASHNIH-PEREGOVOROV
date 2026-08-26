#!/usr/bin/env python3
"""Generate multi-size .ico from Uzbek flag PNG for Windows exe/installer."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("pip install Pillow") from exc

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "extension" / "icons" / "icon128.png"
OUT = ROOT / "assets" / "app.ico"


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing {SRC}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(SRC).convert("RGBA")
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    image.save(OUT, format="ICO", sizes=sizes)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
