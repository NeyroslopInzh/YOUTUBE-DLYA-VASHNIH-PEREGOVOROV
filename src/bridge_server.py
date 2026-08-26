"""HTTP-мост: Chromium extension → desktop app (тот же clipper.py)."""

from __future__ import annotations

import json
import threading
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from chrome_downloads import get_browser_download_dir
from clipper import ClipRequest, ClipperError, download_clip, sanitize_filename
from paths import default_output_dir, ensure_output_dir

BRIDGE_VERSION = "1.0.0"
DEFAULT_PORT = 8766

_jobs: dict[str, dict[str, Any]] = {}
_jobs_lock = threading.Lock()
_server: ThreadingHTTPServer | None = None
_server_thread: threading.Thread | None = None


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


def _unique_title(output_dir: Path, title: str) -> str:
    """Если файл уже есть — добавить _2, _3… (для extension без диалогов)."""
    filename = sanitize_filename(title)
    if not filename.lower().endswith(".mp4"):
        filename += ".mp4"
    if not (output_dir / filename).exists():
        return title

    stem = Path(filename).stem
    for index in range(2, 100):
        candidate_name = f"{stem}_{index}.mp4"
        if not (output_dir / candidate_name).exists():
            return f"{stem}_{index}"
    return f"{stem}_{uuid.uuid4().hex[:6]}"


def _resolve_output_dir(data: dict[str, Any], app_output_dir: Path) -> Path:
    explicit = str(data.get("output_dir", "")).strip()
    if explicit:
        return ensure_output_dir(explicit, app_output_dir)

    if data.get("use_browser_downloads"):
        browser_dir = get_browser_download_dir()
        if browser_dir is not None:
            return ensure_output_dir(browser_dir, app_output_dir)

    return ensure_output_dir(app_output_dir, default_output_dir())


def _run_job(
    job_id: str,
    request: ClipRequest,
    on_job_finished: Callable[[str, bool], None] | None = None,
) -> None:
    def on_log(msg: str) -> None:
        _append_log(job_id, msg)

    success = False
    try:
        result = download_clip(request, on_log=on_log)
        success = True
        with _jobs_lock:
            _jobs[job_id]["status"] = "done"
            _jobs[job_id]["path"] = str(result.output_path)
            _jobs[job_id]["filename"] = result.output_path.name
            _jobs[job_id]["output_path"] = str(result.output_path)
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
    finally:
        if on_job_finished is not None:
            try:
                on_job_finished(job_id, success)
            except Exception:
                pass


def _make_handler(
    get_app_output_dir: Callable[[], Path],
    on_job_started: Callable[[], None] | None = None,
    on_job_finished: Callable[[str, bool], None] | None = None,
):
    class BridgeHandler(BaseHTTPRequestHandler):
        server_version = f"YVPBridge/{BRIDGE_VERSION}"

        def log_message(self, fmt: str, *args: object) -> None:
            return

        def do_OPTIONS(self) -> None:
            self.send_response(204)
            _cors_headers(self)
            self.end_headers()

        def do_GET(self) -> None:
            path = urlparse(self.path).path.rstrip("/") or "/"
            app_dir = get_app_output_dir()

            if path == "/health":
                browser_dir = get_browser_download_dir()
                ffmpeg_path: str | None = None
                ffmpeg_ok = False
                try:
                    from clipper import _resolve_ffmpeg
                    from yt_dlp.downloader.external import FFmpegFD
                    from yt_dlp.postprocessor.ffmpeg import FFmpegPostProcessor

                    ffmpeg_path = _resolve_ffmpeg()
                    FFmpegPostProcessor._ffmpeg_location.set(ffmpeg_path)
                    ffmpeg_ok = FFmpegFD.available()
                except Exception:
                    pass
                _json_response(
                    self,
                    200,
                    {
                        "ok": True,
                        "service": "yvp-app-bridge",
                        "version": BRIDGE_VERSION,
                        "app_output_dir": str(app_dir),
                        "browser_download_dir": str(browser_dir) if browser_dir else None,
                        "ffmpeg_path": ffmpeg_path,
                        "ffmpeg_ok": ffmpeg_ok,
                    },
                )
                return

            if path.startswith("/jobs/"):
                parts = path.split("/")
                if len(parts) >= 3:
                    job_id = parts[2]
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
                            "output_path": job.get("output_path"),
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

                app_dir = get_app_output_dir()
                output_dir = _resolve_output_dir(data, app_dir)
                title = _unique_title(output_dir, title)
                job_id = uuid.uuid4().hex
                request = ClipRequest(
                    url=url,
                    start=start,
                    end=end,
                    title=title,
                    output_dir=output_dir,
                )

                with _jobs_lock:
                    _jobs[job_id] = {
                        "status": "running",
                        "log": [f"Папка сохранения: {output_dir}"],
                    }

                if on_job_started is not None:
                    try:
                        on_job_started()
                    except Exception:
                        pass

                thread = threading.Thread(
                    target=_run_job,
                    args=(job_id, request, on_job_finished),
                    daemon=True,
                )
                thread.start()
                _json_response(
                    self,
                    202,
                    {"job_id": job_id, "status": "running", "output_dir": str(output_dir)},
                )
            except (ClipperError, ValueError, json.JSONDecodeError) as exc:
                _json_response(self, 400, {"error": str(exc)})
            except Exception as exc:  # noqa: BLE001
                _json_response(self, 500, {"error": str(exc)})

    return BridgeHandler


def start_bridge_server(
    get_app_output_dir: Callable[[], Path],
    port: int = DEFAULT_PORT,
    on_job_started: Callable[[], None] | None = None,
    on_job_finished: Callable[[str, bool], None] | None = None,
) -> int:
    global _server, _server_thread

    if _server is not None:
        return _server.server_address[1]

    handler = _make_handler(get_app_output_dir, on_job_started, on_job_finished)
    _server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _server_thread.start()
    return _server.server_address[1]


def stop_bridge_server() -> None:
    global _server, _server_thread
    if _server is not None:
        _server.shutdown()
        _server = None
    _server_thread = None
