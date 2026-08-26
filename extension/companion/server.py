#!/usr/bin/env python3
# YVP Clipper — local companion for Chromium extension
# Copyright (C) 2026 NeyroslopInzh contributors
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License v3 or later. See LICENSE.
"""Local HTTP companion for the Chromium extension — reuses src/clipper.py."""

from __future__ import annotations

import json
import mimetypes
import sys
import tempfile
import threading
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from clipper import ClipRequest, ClipperError, download_clip  # noqa: E402

HOST = "127.0.0.1"
PORT = 8765
TEMP_ROOT = Path(tempfile.gettempdir()) / "yvp-companion"

_jobs: dict[str, dict[str, Any]] = {}
_jobs_lock = threading.Lock()


def _job_temp_dir(job_id: str) -> Path:
    path = TEMP_ROOT / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _cors_headers(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")


def _json_response(handler: BaseHTTPRequestHandler, code: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(code)
    _cors_headers(handler)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw.decode("utf-8") or "{}")


def _append_log(job_id: str, line: str) -> None:
    with _jobs_lock:
        job = _jobs.get(job_id)
        if job is not None:
            job["log"].append(line)


def _run_job(job_id: str, request: ClipRequest) -> None:
    def on_log(msg: str) -> None:
        _append_log(job_id, msg)

    try:
        result = download_clip(request, on_log=on_log)
        filename = result.output_path.name
        with _jobs_lock:
            _jobs[job_id]["status"] = "done"
            _jobs[job_id]["path"] = str(result.output_path)
            _jobs[job_id]["filename"] = filename
    except ClipperError as exc:
        on_log(str(exc))
        with _jobs_lock:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"] = str(exc)
    except Exception as exc:  # noqa: BLE001
        on_log(str(exc))
        with _jobs_lock:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"] = str(exc)
            _jobs[job_id]["traceback"] = traceback.format_exc()


def _serve_job_file(handler: BaseHTTPRequestHandler, job_id: str) -> None:
    with _jobs_lock:
        job = _jobs.get(job_id)
    if not job or job.get("status") != "done":
        _json_response(handler, 404, {"error": "file not ready"})
        return

    file_path = Path(job["path"])
    if not file_path.is_file():
        _json_response(handler, 404, {"error": "file missing"})
        return

    filename = job.get("filename") or file_path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    data = file_path.read_bytes()

    handler.send_response(200)
    _cors_headers(handler)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header(
        "Content-Disposition",
        f'attachment; filename="{filename}"; filename*=UTF-8\'\'{quote(filename)}',
    )
    handler.end_headers()
    handler.wfile.write(data)


class CompanionHandler(BaseHTTPRequestHandler):
    server_version = "YVPCompanion/0.2"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[companion] {self.address_string()} {fmt % args}")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        _cors_headers(self)
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path.rstrip("/") or "/"

        if path == "/health":
            _json_response(self, 200, {"ok": True, "service": "yvp-companion"})
            return

        if path.startswith("/jobs/"):
            parts = path.split("/")
            # /jobs/{id} or /jobs/{id}/file
            if len(parts) >= 3:
                job_id = parts[2]
                if len(parts) >= 4 and parts[3] == "file":
                    _serve_job_file(self, job_id)
                    return

                with _jobs_lock:
                    job = _jobs.get(job_id)
                if not job:
                    _json_response(self, 404, {"error": "job not found"})
                    return
                _json_response(
                    self,
                    200,
                    {
                        "job_id": job_id,
                        "status": job["status"],
                        "log": job["log"],
                        "filename": job.get("filename"),
                        "download_url": f"/jobs/{job_id}/file",
                        "error": job.get("error"),
                    },
                )
                return

        _json_response(self, 404, {"error": "not found"})

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/clip":
            _json_response(self, 404, {"error": "not found"})
            return

        try:
            data = _read_json(self)
            url = str(data.get("url", "")).strip()
            start = str(data.get("start", "")).strip()
            end = str(data.get("end", "")).strip()
            title = str(data.get("title", "")).strip()

            if not url:
                raise ClipperError("URL is required")
            if not title:
                raise ClipperError("Title is required")

            job_id = uuid.uuid4().hex
            output_dir = _job_temp_dir(job_id)
            request = ClipRequest(
                url=url,
                start=start,
                end=end,
                title=title,
                output_dir=output_dir,
            )

            with _jobs_lock:
                _jobs[job_id] = {"status": "running", "log": []}

            thread = threading.Thread(target=_run_job, args=(job_id, request), daemon=True)
            thread.start()
            _json_response(self, 202, {"job_id": job_id, "status": "running"})
        except (ClipperError, ValueError, json.JSONDecodeError) as exc:
            _json_response(self, 400, {"error": str(exc)})
        except Exception as exc:  # noqa: BLE001
            _json_response(self, 500, {"error": str(exc)})


def main() -> None:
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), CompanionHandler)
    print(f"YVP companion listening on http://{HOST}:{PORT}")
    print(f"Temp clips: {TEMP_ROOT}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
