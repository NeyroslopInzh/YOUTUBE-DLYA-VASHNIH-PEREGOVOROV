"""System tray (Windows) for extension background mode."""

from __future__ import annotations

import sys
import threading
from pathlib import Path
from typing import Callable


def tray_icon_path() -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidate = Path(meipass) / "assets" / "icon48.png"
            if candidate.is_file():
                return candidate
    root = Path(__file__).resolve().parent.parent
    return root / "extension" / "icons" / "icon48.png"


class TrayIcon:
    def __init__(
        self,
        title: str,
        on_show: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        self._title = title
        self._on_show = on_show
        self._on_quit = on_quit
        self._icon = None
        self._thread: threading.Thread | None = None
        self._started = threading.Event()

    def start(self) -> bool:
        if sys.platform != "win32":
            return False
        if self._thread and self._thread.is_alive():
            return True

        try:
            import pystray
            from PIL import Image
        except ImportError:
            return False

        icon_file = tray_icon_path()
        if icon_file.is_file():
            image = Image.open(icon_file)
        else:
            image = Image.new("RGB", (48, 48), color="#0099B5")

        menu = pystray.Menu(
            pystray.MenuItem("Открыть", self._menu_show, default=True),
            pystray.MenuItem("Выход", self._menu_quit),
        )
        self._icon = pystray.Icon("yvp_clipper", image, self._title, menu)
        self._thread = threading.Thread(target=self._run_icon, daemon=True)
        self._thread.start()
        return self._started.wait(timeout=5)

    def _run_icon(self) -> None:
        assert self._icon is not None
        self._started.set()
        self._icon.run()

    def _menu_show(self, _icon: object, _item: object) -> None:
        self._on_show()

    def _menu_quit(self, _icon: object, _item: object) -> None:
        self._on_quit()

    def stop(self) -> None:
        if self._icon is not None:
            try:
                self._icon.stop()
            except Exception:
                pass
        self._icon = None
