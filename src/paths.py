"""Пути по умолчанию с учётом локали и XDG."""

from __future__ import annotations

import os
from pathlib import Path


def _expand_user_dirs_value(value: str) -> Path:
    home = str(Path.home())
    expanded = value.strip().strip('"')
    expanded = expanded.replace("$HOME", home).replace("${HOME}", home)
    return Path(expanded)


def _xdg_videos_dir() -> Path | None:
    env = os.environ.get("XDG_VIDEOS_DIR")
    if env:
        return _expand_user_dirs_value(env)

    config = Path.home() / ".config" / "user-dirs.dirs"
    if not config.exists():
        return None

    try:
        for line in config.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("XDG_VIDEOS_DIR="):
                return _expand_user_dirs_value(line.split("=", 1)[1])
    except OSError:
        return None
    return None


def _detect_videos_dir() -> Path:
    xdg = _xdg_videos_dir()
    if xdg and xdg.is_dir():
        return xdg

    home = Path.home()
    for name in ("Videos", "Видео", "videos", "видео", "Video", "Música"):
        candidate = home / name
        if candidate.is_dir():
            return candidate

    return home


def default_output_dir() -> Path:
    """Папка сохранения по умолчанию: ~/Видео/YouTubeClips или ~/Videos/YouTubeClips."""
    return _detect_videos_dir() / "YouTubeClips"


def ensure_output_dir(path: str | Path, fallback: Path | None = None) -> Path:
    """Создаёт папку сохранения или возвращает fallback."""
    fallback = fallback or default_output_dir()
    raw = str(path).strip() if path else str(fallback)

    if not raw:
        target = fallback
    else:
        target = Path(raw).expanduser()

    try:
        target.mkdir(parents=True, exist_ok=True)
        return target.resolve()
    except OSError:
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback.resolve()


def normalize_saved_output_dir(saved: str, default: Path | None = None) -> str:
    default_path = default or default_output_dir()
    if not saved or not str(saved).strip():
        return str(ensure_output_dir(default_path, default_path))

    saved_path = Path(saved).expanduser()
    if saved_path.is_dir():
        return str(saved_path.resolve())

    try:
        return str(ensure_output_dir(saved_path, default_path))
    except OSError:
        return str(ensure_output_dir(default_path, default_path))
