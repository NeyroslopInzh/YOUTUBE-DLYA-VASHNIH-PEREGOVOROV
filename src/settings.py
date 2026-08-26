"""Сохранение и загрузка последних значений формы."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app_log import APP_DIR
from paths import default_output_dir, ensure_output_dir, normalize_saved_output_dir


SETTINGS_FILE = APP_DIR / "settings.json"


@dataclass
class FormSettings:
    url: str = ""
    start: str = "0:00"
    end: str = "1:00"
    title: str = ""
    output_dir: str = ""


def load_settings(default_output_dir_str: str | None = None) -> FormSettings:
    default_path = Path(default_output_dir_str) if default_output_dir_str else default_output_dir()
    default_str = str(ensure_output_dir(default_path, default_path))

    if not SETTINGS_FILE.exists():
        return FormSettings(output_dir=default_str)

    try:
        raw = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        saved_dir = str(raw.get("output_dir") or default_str)
        return FormSettings(
            url=str(raw.get("url", "")),
            start=str(raw.get("start", "0:00")),
            end=str(raw.get("end", "1:00")),
            title=str(raw.get("title", "")),
            output_dir=normalize_saved_output_dir(saved_dir, default_path),
        )
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return FormSettings(output_dir=default_str)


def save_settings(settings: FormSettings) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(
        json.dumps(asdict(settings), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
