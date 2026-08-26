#!/usr/bin/env python3
# Generate Uzbekistan flag icons for the Chromium extension.
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as exc:
    raise SystemExit("Install Pillow: pip install pillow") from exc

OUT = Path(__file__).resolve().parent
BLUE = "#0099B5"
GREEN = "#1EB53A"
WHITE = "#FFFFFF"
RED = "#CE1126"


def draw_flag(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BLUE)
    draw = ImageDraw.Draw(img)
    third = size / 3
    draw.rectangle((0, 0, size, third), fill=BLUE)
    draw.rectangle((0, third, size, 2 * third), fill=WHITE)
    draw.rectangle((0, 2 * third, size, size), fill=GREEN)
    line = max(1, size // 32)
    draw.rectangle((0, int(third) - line, size, int(third) + line), fill=RED)
    draw.rectangle((0, int(2 * third) - line, size, int(2 * third) + line), fill=RED)

    if size >= 24:
        cx = size * 0.22
        cy = third / 2
        r = third * 0.38
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
        draw.ellipse((cx - r * 0.35, cy - r, cx + r * 1.15, cy + r), fill=BLUE)
        if size >= 48:
            for i in range(5):
                sx = cx + r * 1.35 + (i % 3) * r * 0.28
                sy = cy - r * 0.45 + (i // 3) * r * 0.45
                sr = max(2, size // 24)
                draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=WHITE)

    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for size, name in ((16, "icon16.png"), (48, "icon48.png"), (128, "icon128.png")):
        draw_flag(size).save(OUT / name, format="PNG")
    print(f"Wrote icons to {OUT}")


if __name__ == "__main__":
    main()
