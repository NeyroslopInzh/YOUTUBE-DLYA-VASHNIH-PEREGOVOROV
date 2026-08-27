"""YouTube segment downloader via yt-dlp --download-sections."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

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


def _find_ytdlp_exe() -> str | None:
    if _is_frozen():
        return None
    return shutil.which("yt-dlp")


def _use_inprocess_ytdlp() -> bool:
    # Frozen PyInstaller exe IS the GUI — sys.executable -m yt_dlp re-opens the app.
    if _is_frozen():
        return True
    # Dev/native host: same download_ranges API as frozen build (fast segment cut).
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        return False
    return True


def _format_hms(total_seconds: float) -> str:
    ms_total = max(0, int(round(float(total_seconds) * 1000)))
    h, rem = divmod(ms_total, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def parse_time(value: str) -> str:
    value = value.strip()
    if not value:
        raise ClipperError(_t("err.time_empty"))

    if re.fullmatch(r"\d+(?:\.\d+)?", value):
        return _format_hms(float(value))

    parts = value.split(":")
    try:
        if len(parts) == 2:
            m, s = parts
            total = int(m) * 60 + float(s)
            return _format_hms(total)
        if len(parts) == 3:
            h, m, s = parts
            total = int(h) * 3600 + int(m) * 60 + float(s)
            return _format_hms(total)
    except ValueError as exc:
        raise ClipperError(_t("err.time_invalid", value=value)) from exc

    raise ClipperError(_t("err.time_invalid", value=value))


def _time_to_seconds(value: str) -> float:
    normalized = parse_time(value)
    h, m, rest = normalized.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def _build_download_ranges(start: str, end: str):
    from yt_dlp.utils import download_range_func

    start_sec = _time_to_seconds(start)
    end_sec = _time_to_seconds(end)
    return download_range_func([], [(start_sec, end_sec)])

def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        raise ClipperError(_t("err.title_empty"))
    return cleaned


def _ffmpeg_exists(path: str | None) -> bool:
    return bool(path) and Path(path).is_file()


def _resolve_ffmpeg() -> str:
    system = shutil.which("ffmpeg")
    if sys.platform != "win32":
        if _ffmpeg_exists(system):
            return system  # type: ignore[arg-type]
        raise ClipperError(_t("err.ffmpeg_missing_linux"))

    candidates: list[Path] = []
    if _ffmpeg_exists(system):
        candidates.append(Path(system))  # type: ignore[arg-type]

    if _is_frozen():
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            root = Path(meipass)
            candidates.extend(root.rglob("ffmpeg-win*.exe"))
            candidates.extend(root.rglob("ffmpeg.exe"))

    try:
        import imageio_ffmpeg

        candidates.append(Path(imageio_ffmpeg.get_ffmpeg_exe()))
    except ImportError as exc:
        if not candidates:
            raise ClipperError(_t("err.ffmpeg_missing_win")) from exc

    for cand in candidates:
        if cand.is_file():
            return str(cand.resolve())

    raise ClipperError(_t("err.ffmpeg_missing_win"))


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


# Как desktop app (dist/windows): android + tv + web, webpage не скипаем.
_YOUTUBE_STRATEGIES: list[dict[str, list[str]]] = [
    {"player_client": ["android", "tv", "web"]},
]

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _build_cookie_header(cookies: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for cookie in cookies:
        name = str(cookie.get("name", "")).strip()
        if not name:
            continue
        value = str(cookie.get("value", ""))
        parts.append(f"{name}={value}")
    return "; ".join(parts)


def _write_netscape_cookies(cookies: list[dict[str, Any]], path: Path) -> None:
    lines = ["# Netscape HTTP Cookie File", "# Generated by YVP Clipper", ""]
    for cookie in cookies:
        name = str(cookie.get("name", "")).strip()
        if not name:
            continue
        domain = str(cookie.get("domain", "")).strip()
        if not domain:
            continue
        include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
        cookie_path = str(cookie.get("path") or "/")
        secure = "TRUE" if cookie.get("secure") else "FALSE"
        expires_raw = cookie.get("expirationDate", cookie.get("expires", 0))
        try:
            expires = int(float(expires_raw or 0))
        except (TypeError, ValueError):
            expires = 0
        value = str(cookie.get("value", ""))
        domain_col = domain
        if cookie.get("httpOnly"):
            domain_col = f"#HttpOnly_{domain}"
        lines.append(
            f"{domain_col}\t{include_subdomains}\t{cookie_path}\t{secure}\t{expires}\t{name}\t{value}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _youtube_extractor_args(strategy: dict[str, list[str]]) -> dict[str, Any]:
    return {"youtube": strategy}


def _youtube_extractor_args_cli(strategy: dict[str, list[str]]) -> str:
    parts: list[str] = []
    if clients := strategy.get("player_client"):
        parts.append(f"player_client={','.join(clients)}")
    if skip := strategy.get("player_skip"):
        parts.append(f"player_skip={','.join(skip)}")
    return f"youtube:{';'.join(parts)}"


def _ytdlp_options(
    ffmpeg: str,
    start: str,
    end: str,
    output_path: Path,
    youtube_strategy: dict[str, list[str]] | None = None,
    cookiefile: str | None = None,
    cookie_header: str | None = None,
    cookies_browser: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    strategy = youtube_strategy or _YOUTUBE_STRATEGIES[-1]
    opts: dict[str, Any] = {
        "download_ranges": _build_download_ranges(start, end),
        "force_keyframes_at_cuts": True,
        "extractor_args": _youtube_extractor_args(strategy),
        "remote_components": ["ejs:github"],
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 3,
        "socket_timeout": 30,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "no_warnings": True,
        "ffmpeg_location": ffmpeg,
        "outtmpl": str(output_path),
        "progress": True,
    }
    if cookie_header:
        opts["http_headers"] = {"Cookie": cookie_header}
    if cookiefile:
        opts["cookiefile"] = cookiefile
    if cookies_browser:
        opts["cookiesfrombrowser"] = cookies_browser
    return opts


class _YtdlpLogBridge:
    def __init__(self, on_log: Callable[[str], None]) -> None:
        self._on_log = on_log
        self.lines: list[str] = []

    def _emit(self, msg: str) -> None:
        if not msg:
            return
        msg = _strip_ansi(msg)
        if _should_skip_log_line(msg):
            return
        self.lines.append(msg)
        self._on_log(msg)

    def debug(self, msg: str) -> None:
        if msg.startswith("[debug] "):
            return
        self._emit(msg)

    def info(self, msg: str) -> None:
        self._emit(msg)

    def warning(self, msg: str) -> None:
        self._emit(msg)

    def error(self, msg: str) -> None:
        self._emit(msg)

    def text(self) -> str:
        return "\n".join(self.lines)


def _build_ytdlp_cmd(
    ffmpeg: str,
    section: str,
    output_path: Path,
    url: str,
    youtube_strategy: dict[str, list[str]] | None = None,
    cookiefile: str | None = None,
) -> list[str]:
    strategy = youtube_strategy or _YOUTUBE_STRATEGIES[-1]
    extractor = _youtube_extractor_args_cli(strategy)
    exe = _find_ytdlp_exe()
    prefix = [exe, "--ffmpeg-location", ffmpeg] if exe else [
        sys.executable,
        "-m",
        "yt_dlp",
        "--ffmpeg-location",
        ffmpeg,
    ]
    return prefix + _cli_args_tail(section, output_path, url, extractor, cookiefile)


def _cli_args_tail(
    section: str,
    output_path: Path,
    url: str,
    extractor_args: str,
    cookiefile: str | None = None,
) -> list[str]:
    args = [
        "--download-sections",
        section,
        "--force-keyframes-at-cuts",
        "--extractor-args",
        extractor_args,
        "--remote-components",
        "ejs:github",
        "--retries",
        "10",
        "--fragment-retries",
        "10",
        "--extractor-retries",
        "3",
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
    if cookiefile:
        args[0:0] = ["--cookies", cookiefile]
    return args


def _should_skip_log_line(line: str) -> bool:
    lowered = line.lower()
    return (
        line.startswith("Fontconfig warning:")
        or "deprecated feature:" in lowered
    )


def _run_ytdlp_subprocess(cmd: list[str], on_log: Callable[[str], None]) -> tuple[int, str]:
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
        if not line or _should_skip_log_line(line):
            continue
        lines.append(line)
        on_log(line)

    return proc.wait(), "\n".join(lines)


def _run_ytdlp_inprocess(
    ffmpeg: str,
    start: str,
    end: str,
    output_path: Path,
    url: str,
    on_log: Callable[[str], None],
    youtube_strategy: dict[str, list[str]] | None = None,
    cookiefile: str | None = None,
    cookie_header: str | None = None,
    cookies_browser: tuple[str, ...] | None = None,
) -> tuple[int, str]:
    import yt_dlp
    from yt_dlp.postprocessor.ffmpeg import FFmpegPostProcessor

    # CLI entry sets this; in-process YoutubeDL() does not (yt-dlp #2191).
    FFmpegPostProcessor._ffmpeg_location.set(ffmpeg)

    bridge = _YtdlpLogBridge(on_log)
    opts = _ytdlp_options(
        ffmpeg,
        start,
        end,
        output_path,
        youtube_strategy,
        cookiefile,
        cookie_header,
        cookies_browser,
    )
    opts["logger"] = bridge

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return 0, bridge.text()
    except yt_dlp.utils.DownloadError as exc:
        msg = str(exc)
        bridge.error(msg)
        return 1, bridge.text() or msg
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        bridge.error(msg)
        return 1, bridge.text() or msg


def _run_ytdlp(
    ffmpeg: str,
    start: str,
    end: str,
    section: str,
    output_path: Path,
    url: str,
    on_log: Callable[[str], None],
    youtube_strategy: dict[str, list[str]] | None = None,
    cookiefile: str | None = None,
    cookie_header: str | None = None,
    cookies_browser: tuple[str, ...] | None = None,
) -> tuple[int, str]:
    if _use_inprocess_ytdlp():
        return _run_ytdlp_inprocess(
            ffmpeg,
            start,
            end,
            output_path,
            url,
            on_log,
            youtube_strategy,
            cookiefile,
            cookie_header,
            cookies_browser,
        )
    cmd = _build_ytdlp_cmd(ffmpeg, section, output_path, url, youtube_strategy, cookiefile)
    return _run_ytdlp_subprocess(cmd, on_log)


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
    browser_cookies: list[dict[str, Any]] | None = None,
    cookies_browser: tuple[str, ...] | None = None,
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

    ui_log(_t("clip.downloading", start=start, end=end))
    ui_log(_t("clip.saving", path=output_path))

    cookie_path: Path | None = None
    if browser_cookies:
        cookie_path = request.output_dir / ".yvp-cookies.txt"
        _write_netscape_cookies(browser_cookies, cookie_path)

    max_attempts = 3
    last_output = ""
    code = 1
    try:
        for attempt in range(1, max_attempts + 1):
            strategy = _YOUTUBE_STRATEGIES[(attempt - 1) % len(_YOUTUBE_STRATEGIES)]
            if attempt > 1:
                wait_s = attempt * 2
                ui_log(_t("clip.retry", attempt=attempt, total=max_attempts, wait=wait_s))
                time.sleep(wait_s)

            cookiefile: str | None = None
            if cookie_path and attempt >= 2:
                cookiefile = str(cookie_path)
                if attempt == 2:
                    ui_log(f"Cookies YouTube (retry): {len(browser_cookies or [])}")

            code, last_output = _run_ytdlp(
                ffmpeg,
                start,
                end,
                section,
                output_path,
                url,
                ui_log,
                strategy,
                cookiefile,
                None,
                None,
            )
            if code == 0:
                break

            transient = (
                "winerror 10054" in last_output.lower()
                or "forcibly closed" in last_output.lower()
                or "unable to download" in last_output.lower()
                or "timed out" in last_output.lower()
                or "handshake" in last_output.lower()
            )
            if not transient or attempt >= max_attempts:
                break
    finally:
        if cookie_path is not None:
            cookie_path.unlink(missing_ok=True)

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
