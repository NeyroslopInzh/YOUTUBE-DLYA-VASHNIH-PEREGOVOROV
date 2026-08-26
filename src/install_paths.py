"""Paths for installed app layout (installer vs portable)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

INSTALL_MARKER = ".yvp_installed"
WIN_DIR_NAME = "YVPClipper"
LINUX_DIR_NAME = "yvp-clipper"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _frozen_exe_dir() -> Path:
    return Path(sys.executable).resolve().parent


def _windows_install_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    if not local:
        return Path()
    return Path(local) / WIN_DIR_NAME


def _linux_install_dir() -> Path:
    data_home = os.environ.get("XDG_DATA_HOME", "")
    if data_home:
        return Path(data_home) / LINUX_DIR_NAME
    return Path.home() / ".local" / "share" / LINUX_DIR_NAME


def install_root() -> Path | None:
    """Return install root if app was installed via setup script, else None."""
    if sys.platform == "win32":
        candidate = _windows_install_dir()
    else:
        candidate = _linux_install_dir()

    if (candidate / INSTALL_MARKER).is_file():
        return candidate
    return None


def extension_dir() -> Path:
    """Directory to load as unpacked Chromium extension."""
    installed = install_root()
    if installed is not None:
        ext = installed / "extension"
        if (ext / "manifest.json").is_file():
            return ext

    frozen = getattr(sys, "frozen", False)
    if frozen:
        bundled = _frozen_exe_dir() / "extension"
        if (bundled / "manifest.json").is_file():
            return bundled

    dev = _repo_root() / "extension"
    if (dev / "manifest.json").is_file():
        return dev

    return _repo_root() / "extension"


def was_installed_via_setup() -> bool:
    return install_root() is not None
