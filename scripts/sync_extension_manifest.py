#!/usr/bin/env python3
"""Sync extension/manifest.json name from src/app_name.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from app_name import APP_NAME  # noqa: E402

MANIFEST = ROOT / "extension" / "manifest.json"


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["name"] = APP_NAME
    data["short_name"] = APP_NAME
    data["action"]["default_title"] = APP_NAME
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {MANIFEST}")


if __name__ == "__main__":
    main()
