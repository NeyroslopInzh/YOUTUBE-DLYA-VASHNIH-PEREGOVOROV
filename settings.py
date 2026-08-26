"""Сохранение и загрузка последних значений формы."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app_log import APP_DIR


SETTINGS_FILE = APP_DIR / "settings.json"


@dataclass
class FormSettings:
    url: str = ""
    start: str = "0:00"
    end: str = "1:00"
    title: str = ""
    output_dir: str = ""


def load_settings(default_output_dir: str) -> FormSettings:
    if not SETTINGS_FILE.exists():
        return FormSettings(output_dir=default_output_dir)

    try:
        raw = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        return FormSettings(
            url=str(raw.get("url", "")),
            start=str(raw.get("start", "0:00")),
            end=str(raw.get("end", "1:00")),
            title=str(raw.get("title", "")),
            output_dir=str(raw.get("output_dir") or default_output_dir),
        )
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return FormSettings(output_dir=default_output_dir)


def save_settings(settings: FormSettings) -> None:
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(
        json.dumps(asdict(settings), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
