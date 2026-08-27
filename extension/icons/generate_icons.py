#!/usr/bin/env python3
# Generate Uzbekistan flag icons for the Chromium extension.
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Install Pillow: pip install pillow") from exc

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from uzbek_flag import draw_uzbekistan_icon  # noqa: E402

OUT = Path(__file__).resolve().parent


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for size, name in ((16, "icon16.png"), (48, "icon48.png"), (128, "icon128.png")):
        draw_uzbekistan_icon(size).convert("RGBA").save(OUT / name, format="PNG")
    print(f"Wrote icons to {OUT}")


if __name__ == "__main__":
    main()
