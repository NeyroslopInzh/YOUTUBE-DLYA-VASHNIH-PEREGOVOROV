"""Animated GIF widget (Pillow frames → CTkLabel)."""

from __future__ import annotations

import sys
from pathlib import Path

import customtkinter as ctk
from PIL import Image


def pricol_gif_path() -> Path | None:
    candidates: list[Path] = []
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(Path(meipass) / "assets" / "pricol.gif")
        candidates.append(Path(sys.executable).resolve().parent / "assets" / "pricol.gif")
    root = Path(__file__).resolve().parent.parent
    candidates.append(root / "assets" / "pricol.gif")
    for path in candidates:
        if path.is_file():
            return path
    return None


class AnimatedGifLabel(ctk.CTkLabel):
    """Крутит GIF справа от формы — не перехватывает фокус у полей."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        gif_path: Path,
        max_width: int = 220,
        **kwargs: object,
    ) -> None:
        self._frames: list[ctk.CTkImage] = []
        self._delays: list[int] = []
        self._index = 0
        self._job: str | None = None
        self._alive = True

        pil = Image.open(gif_path)
        w, h = pil.size
        if w > max_width:
            ratio = max_width / w
            size = (max_width, max(1, int(h * ratio)))
        else:
            size = (w, h)

        n = getattr(pil, "n_frames", 1)
        for i in range(n):
            try:
                pil.seek(i)
            except EOFError:
                break
            frame = pil.convert("RGBA")
            self._frames.append(ctk.CTkImage(light_image=frame, dark_image=frame, size=size))
            delay = pil.info.get("duration", 80)
            self._delays.append(max(20, int(delay)))

        if not self._frames:
            blank = Image.new("RGBA", size, (0, 0, 0, 0))
            self._frames.append(ctk.CTkImage(light_image=blank, dark_image=blank, size=size))
            self._delays.append(100)

        kwargs.setdefault("text", "")
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, image=self._frames[0], **kwargs)
        # Не мешать кликам по полям слева — гифка не grab'ит ничего лишнего
        self.configure(cursor="")

    def start(self) -> None:
        self._alive = True
        self._tick()

    def stop(self) -> None:
        self._alive = False
        if self._job is not None:
            try:
                self.after_cancel(self._job)
            except Exception:
                pass
            self._job = None

    def _tick(self) -> None:
        if not self._alive or not self.winfo_exists():
            return
        self.configure(image=self._frames[self._index])
        delay = self._delays[self._index]
        self._index = (self._index + 1) % len(self._frames)
        self._job = self.after(delay, self._tick)

    def destroy(self) -> None:  # type: ignore[override]
        self.stop()
        super().destroy()
