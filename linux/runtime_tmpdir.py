"""Prefer XDG cache over /tmp for tempfile/yt-dlp after the bootloader starts.

Onefile extraction itself still honours TMPDIR from the environment — the
wrapper in install.sh / PKGBUILD sets that before exec.
"""

from __future__ import annotations

import os
from pathlib import Path


def _cache_tmp() -> str:
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    path = base / "yvp-clipper" / "tmp"
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def _is_tmpfs_temp(path: str) -> bool:
    real = os.path.realpath(path) if path else ""
    return real in ("/tmp", "/var/tmp") or real.startswith("/tmp/") or real.startswith("/var/tmp/")


_current = os.environ.get("TMPDIR") or os.environ.get("TEMP") or os.environ.get("TMP") or ""
if not _current or _is_tmpfs_temp(_current):
    dest = _cache_tmp()
    os.environ["TMPDIR"] = dest
    os.environ["TEMP"] = dest
    os.environ["TMP"] = dest
