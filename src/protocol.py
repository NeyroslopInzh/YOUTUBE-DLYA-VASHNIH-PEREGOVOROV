"""Custom URL protocol (yvp://) helpers for extension auto-launch."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request

BRIDGE_HEALTH_URL = "http://127.0.0.1:8766/health"
PROTOCOL_SCHEME = "yvp://"


def is_protocol_launch(argv: list[str] | None = None) -> bool:
    args = argv if argv is not None else sys.argv
    return any(arg.lower().startswith(PROTOCOL_SCHEME) for arg in args[1:])


def bridge_already_running(timeout: float = 1.0) -> bool:
    try:
        with urllib.request.urlopen(BRIDGE_HEALTH_URL, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return False
