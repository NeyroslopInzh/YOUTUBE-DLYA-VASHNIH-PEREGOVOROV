#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
echo "[Companion] Starting on http://127.0.0.1:8765"
exec python3 extension/companion/server.py
