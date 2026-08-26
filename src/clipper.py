"""YouTube segment downloader via yt-dlp --download-sections."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from app_log import logger as app_logger
from i18n import get_i18n, set_language


class ClipperError(Exception):
    pass


@dataclass
class ClipRequest:
    url: str
    start: str
    end: str
    title: str
    output_dir: Path


@dataclass
class ClipResult:
    output_path: Path


def _t(key: str, **kwargs: object) -> str:
    return get_i18n().t(key, **kwargs)


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _find_ytdlp() -> str:
    # PyInstaller bundle ships yt_dlp; system yt-dlp inherits broken LD_LIBRARY_PATH
    # (bundled libcrypto vs system Python 3.14 / OpenSSL 3.3 → ImportError).
    if _is_frozen():
        return sys.executable
    exe = shutil.which("yt-dlp")
    if exe:
        return exe
    return sys.executable


def _ytdlp_base_args(ffmpeg_location: str) -> list[str]:
    exe = _find_ytdlp()
    if exe == sys.executable:
        return [
            sys.executable,
            "-m",
            "yt_dlp",
            "--ffmpeg-location",
            ffmpeg_location,
        ]
    return [exe, "--ffmpeg-location", ffmpeg_location]


def parse_time(value: str) -> str:
    value = value.strip()
    if not value:
        raise ClipperError(_t("err.time_empty"))

    if re.fullmatch(r"\d+", value):
        total = int(value)
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    parts = value.split(":")
    if len(parts) == 2:
        m, s = parts
        return f"00:{int(m):02d}:{int(s):02d}"
    if len(parts) == 3:
        h, m, s = parts
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

    raise ClipperError(_t("err.time_invalid", value=value))


def _time_to_seconds(value: str) -> int:
    normalized = parse_time(value)
    h, m, s = (int(x) for x in normalized.split(":"))
    return h * 3600 + m * 60 + s


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        raise ClipperError(_t("err.title_empty"))
    return cleaned


def _resolve_ffmpeg() -> str:
    system = shutil.which("ffmpeg")
    if sys.platform != "win32":
        if system:
            return system
        raise ClipperError(_t("err.ffmpeg_missing_linux"))
    if system:
        return system
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise ClipperError(_t("err.ffmpeg_missing_win")) from exc
    return imageio_ffmpeg.get_ffmpeg_exe()


def _friendly_error(output: str, code: int) -> str:
    text = output.lower()
    if "openssl_3.3.0" in text or "libcrypto.so.3" in text:
        return _t("err.openssl_mismatch")
    if "ffmpeg exited with code -11" in text or "code -11" in text:
        return _t("err.ffmpeg_segfault")
    if "winerror 10054" in text or "forcibly closed" in text:
        return _t("err.winerror_10054")
    if "unable to download api page" in text:
        return _t("err.api_page")
    if "sign in to confirm" in text or "bot" in text:
        return _t("err.bot_check")
    tail = "\n".join(line for line in output.splitlines() if line.strip())[-800:]
    return _t("err.ytdlp_code", code=code, tail=tail)


def _build_ytdlp_cmd(ffmpeg: str, section: str, output_path: Path, url: str) -> list[str]:
    return _ytdlp_base_args(ffmpeg) + [
        "--download-sections",
        section,
        "--force-keyframes-at-cuts",
        "--extractor-args",
        "youtube:player_client=android,tv,web",
        "--remote-components",
        "ejs:github",
        "--retries",
        "10",
        "--fragment-retries",
        "10",
        "--socket-timeout",
        "30",
        "-f",
        "bv*+ba/b",
        "--merge-output-format",
        "mp4",
        "--no-playlist",
        "--no-warnings",
        "--progress",
        "-o",
        str(output_path),
        url,
    ]


def _run_ytdlp(cmd: list[str], on_log: Callable[[str], None]) -> tuple[int, str]:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )

    lines: list[str] = []
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.rstrip()
        if line:
            lines.append(line)
            on_log(line)

    return proc.wait(), "\n".join(lines)


def build_output_path(output_dir: Path, title: str) -> Path:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ClipperError(_t("err.output_dir", path=output_dir, error=exc)) from exc
    filename = sanitize_filename(title)
    if not filename.lower().endswith(".mp4"):
        filename += ".mp4"
    return output_dir / filename


def download_clip(
    request: ClipRequest,
    on_log: Callable[[str], None] | None = None,
    language: str | None = None,
) -> ClipResult:
    if language:
        set_language(language)

    log = app_logger()

    def ui_log(msg: str) -> None:
        log.info(msg)
        if on_log:
            on_log(msg)

    url = request.url.strip()
    if not url:
        raise ClipperError(_t("err.empty_url"))
    if "youtube.com" not in url and "youtu.be" not in url:
        raise ClipperError(_t("err.not_youtube"))

    start = parse_time(request.start)
    end = parse_time(request.end)
    if _time_to_seconds(end) <= _time_to_seconds(start):
        raise ClipperError(_t("err.end_before_start"))

    output_path = build_output_path(request.output_dir, request.title)
    if output_path.exists():
        raise ClipperError(_t("err.file_exists", path=output_path))

    ffmpeg = _resolve_ffmpeg()
    section = f"*{start}-{end}"
    cmd = _build_ytdlp_cmd(ffmpeg, section, output_path, url)

    ui_log(_t("clip.downloading", start=start, end=end))
    ui_log(_t("clip.saving", path=output_path))

    max_attempts = 3
    last_output = ""
    code = 1
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            wait_s = attempt * 2
            ui_log(_t("clip.retry", attempt=attempt, total=max_attempts, wait=wait_s))
            time.sleep(wait_s)

        code, last_output = _run_ytdlp(cmd, ui_log)
        if code == 0:
            break

        if "winerror 10054" not in last_output.lower() and attempt < max_attempts:
            if "unable to download" not in last_output.lower():
                break

    if code != 0:
        raise ClipperError(_friendly_error(last_output, code))

    if not output_path.exists():
        candidates = list(request.output_dir.glob(f"{output_path.stem}*.mp4"))
        if len(candidates) == 1:
            if candidates[0] != output_path:
                candidates[0].rename(output_path)
        else:
            raise ClipperError(_t("err.file_not_found"))

    ui_log(_t("clip.done"))
    return ClipResult(output_path=output_path)
