"""Папка загрузок Chrome/Edge из Preferences (Windows)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _read_prefs_download_dir(prefs_path: Path) -> Path | None:
    try:
        data = json.loads(prefs_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    savefile = data.get("savefile") if isinstance(data.get("savefile"), dict) else {}
    raw = savefile.get("default_directory")
    if not raw or not str(raw).strip():
        return None

    path = Path(str(raw))
    if path.is_dir():
        return path.resolve()
    return None


def get_browser_download_dir() -> Path | None:
    """Папка загрузок из chrome://settings/downloads (Chrome / Edge / Chromium)."""
    if sys.platform == "win32":
        return _windows_browser_download_dir()
    return _linux_browser_download_dir()


def _windows_browser_download_dir() -> Path | None:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return None

    candidates: list[Path] = []
    for browser in ("Google/Chrome", "Microsoft/Edge", "Chromium"):
        base = Path(local) / browser / "User Data"
        if not base.is_dir():
            continue
        for profile in ("Default", "Profile 1", "Profile 2"):
            prefs = base / profile / "Preferences"
            if prefs.is_file():
                candidates.append(prefs)

    for prefs in candidates:
        found = _read_prefs_download_dir(prefs)
        if found is not None:
            return found
    return None


def _linux_browser_download_dir() -> Path | None:
    config = os.environ.get("XDG_CONFIG_HOME")
    config_root = Path(config) if config else Path.home() / ".config"

    candidates: list[Path] = []
    for browser in (
        "google-chrome",
        "chromium",
        "BraveSoftware/Brave-Browser",
        "microsoft-edge",
        "opera",
    ):
        base = config_root / browser
        if not base.is_dir():
            continue
        for profile in ("Default", "Profile 1", "Profile 2"):
            prefs = base / profile / "Preferences"
            if prefs.is_file():
                candidates.append(prefs)

    for prefs in candidates:
        found = _read_prefs_download_dir(prefs)
        if found is not None:
            return found
    return None
