#!/usr/bin/env python3
"""Sync extension/manifest.json name + version from src/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from app_name import APP_NAME  # noqa: E402
from app_version import APP_VERSION  # noqa: E402

MANIFEST = ROOT / "extension" / "manifest.json"
ISS = ROOT / "windows" / "installer.iss"


def _sync_iss_version() -> None:
    if not ISS.is_file():
        return
    text = ISS.read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("#define MyAppVersion"):
            lines.append(f'#define MyAppVersion "{APP_VERSION}"\n')
        else:
            lines.append(line)
    ISS.write_text("".join(lines), encoding="utf-8")
    print(f"Updated {ISS} -> {APP_VERSION}")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["name"] = APP_NAME
    data["short_name"] = APP_NAME
    data["action"]["default_title"] = APP_NAME
    data["version"] = APP_VERSION
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {MANIFEST} -> {APP_VERSION}")
    _sync_iss_version()


if __name__ == "__main__":
    main()
