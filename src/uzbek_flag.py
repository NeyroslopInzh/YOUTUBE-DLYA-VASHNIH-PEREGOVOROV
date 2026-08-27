"""Единый рисунок флага Узбекистана (Pillow) — app / installer / extension / UI."""

from __future__ import annotations

from PIL import Image, ImageDraw

BLUE = "#0099B5"
GREEN = "#1EB53A"
WHITE = "#FFFFFF"
RED = "#CE1126"


def draw_uzbekistan_flag(width: int, height: int) -> Image.Image:
    """Прямоугольный флаг (обычно 3:2). Для квадратных иконок — вписать в квадрат с полями."""
    img = Image.new("RGB", (width, height), BLUE)
    draw = ImageDraw.Draw(img)

    third = height / 3.0
    draw.rectangle((0, 0, width, third), fill=BLUE)
    draw.rectangle((0, third, width, 2 * third), fill=WHITE)
    draw.rectangle((0, 2 * third, width, height), fill=GREEN)

    line = max(1, height // 48)
    y1 = int(round(third))
    y2 = int(round(2 * third))
    draw.rectangle((0, y1 - line, width, y1 + line), fill=RED)
    draw.rectangle((0, y2 - line, width, y2 + line), fill=RED)

    # Полумесяц + 12 звёзд на синей полосе
    if height >= 12:
        cx = width * 0.18
        cy = third / 2
        r = third * 0.36
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
        # смещённый вырез → полумесяц
        draw.ellipse(
            (cx - r * 0.15, cy - r * 0.95, cx + r * 1.25, cy + r * 0.95),
            fill=BLUE,
        )

        # 12 звёзд: ряды 3 / 4 / 5 справа от полумесяца
        star_r = max(1.0, height * 0.035)
        rows = (3, 4, 5)
        base_x = cx + r * 1.15
        for row_i, count in enumerate(rows):
            for col in range(count):
                sx = base_x + col * (star_r * 2.6)
                sy = cy - (len(rows) - 1) * star_r * 1.35 + row_i * star_r * 2.7
                _star(draw, sx, sy, star_r, WHITE)

    return img


def draw_uzbekistan_icon(size: int) -> Image.Image:
    """Квадратная иконка — флаг на весь квадрат (удобно для .ico / extension)."""
    return draw_uzbekistan_flag(size, size).convert("RGBA")


def _star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, color: str) -> None:
    import math

    pts: list[tuple[float, float]] = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color)
