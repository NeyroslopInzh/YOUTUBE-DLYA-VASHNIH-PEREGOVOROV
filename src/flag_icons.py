"""PNG-флаги для кнопок языка (Pillow). Без emoji — Windows их часто убивает."""

from __future__ import annotations

import math
from functools import lru_cache

from PIL import Image, ImageDraw

try:
    from customtkinter import CTkImage
except ImportError:  # pragma: no cover
    CTkImage = None  # type: ignore[misc, assignment]

W, H = 48, 32


def _stripe_h(img: Image.Image, colors: list[str]) -> None:
    draw = ImageDraw.Draw(img)
    n = len(colors)
    for i, color in enumerate(colors):
        y0 = int(H * i / n)
        y1 = int(H * (i + 1) / n)
        draw.rectangle((0, y0, W, y1), fill=color)


def draw_ru() -> Image.Image:
    img = Image.new("RGB", (W, H))
    _stripe_h(img, ["#FFFFFF", "#0039A6", "#D52B1E"])
    return img


def draw_en() -> Image.Image:
    """Упрощённый US: полосы + синий кантон с точками-звёздами."""
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    for i in range(13):
        y0 = int(H * i / 13)
        y1 = int(H * (i + 1) / 13)
        draw.rectangle((0, y0, W, y1), fill="#B22234" if i % 2 == 0 else "#FFFFFF")
    canton_w = int(W * 0.4)
    canton_h = int(H * 7 / 13)
    draw.rectangle((0, 0, canton_w, canton_h), fill="#3C3B6E")
    # Точки вместо полигонов — на 48px звёзды выглядят как каша
    for row in range(4):
        cols = 5 if row % 2 == 0 else 4
        for col in range(cols):
            ox = 0 if row % 2 == 0 else (canton_w / (cols + 1)) * 0.5
            sx = ox + (col + 1) * canton_w / (cols + 1)
            sy = (row + 0.7) * canton_h / 5
            r = 1.2
            draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill="#FFFFFF")
    return img


def draw_he() -> Image.Image:
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    blue = "#0038B8"
    band = max(2, H // 8)
    draw.rectangle((0, band, W, band * 2), fill=blue)
    draw.rectangle((0, H - band * 2, W, H - band), fill=blue)
    cx, cy, r = W / 2, H / 2, H * 0.22
    up = [(cx, cy - r), (cx - r * 0.9, cy + r * 0.55), (cx + r * 0.9, cy + r * 0.55)]
    down = [(cx, cy + r), (cx - r * 0.9, cy - r * 0.55), (cx + r * 0.9, cy - r * 0.55)]
    draw.line(up + [up[0]], fill=blue, width=2)
    draw.line(down + [down[0]], fill=blue, width=2)
    return img


def draw_hi() -> Image.Image:
    img = Image.new("RGB", (W, H))
    _stripe_h(img, ["#FF9933", "#FFFFFF", "#138808"])
    draw = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H / 2, H * 0.18
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline="#000080", width=2)
    for i in range(12):
        ang = i * math.pi / 6
        draw.line(
            (cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang)),
            fill="#000080",
            width=1,
        )
    return img


def draw_uz() -> Image.Image:
    from uzbek_flag import draw_uzbekistan_flag

    return draw_uzbekistan_flag(W, H)


_DRAWERS = {
    "ru": draw_ru,
    "en": draw_en,
    "he": draw_he,
    "hi": draw_hi,
    "uz": draw_uz,
}


def flag_image(code: str) -> Image.Image:
    drawer = _DRAWERS.get(code)
    if drawer is None:
        img = Image.new("RGB", (W, H), "#666666")
        return img
    return drawer()


@lru_cache(maxsize=16)
def flag_ctk_image(code: str) -> "CTkImage":
    if CTkImage is None:
        raise RuntimeError("customtkinter is required for flag_ctk_image")
    pil = flag_image(code)
    return CTkImage(light_image=pil, dark_image=pil, size=(W, H))
