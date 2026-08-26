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

import imageio_ffmpeg

from app_log import logger as app_logger


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


def _find_ytdlp() -> str:
    exe = shutil.which("yt-dlp")
    if exe:
        return exe
    # pip-installed module fallback
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
    """Normalize user time to HH:MM:SS for yt-dlp."""
    value = value.strip()
    if not value:
        raise ClipperError("Время не указано")

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

    raise ClipperError(f"Неверный формат времени: {value!r} (ожидается MM:SS, HH:MM:SS или секунды)")


def _time_to_seconds(value: str) -> int:
    normalized = parse_time(value)
    h, m, s = (int(x) for x in normalized.split(":"))
    return h * 3600 + m * 60 + s


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        raise ClipperError("Название файла пустое")
    return cleaned


def _friendly_error(output: str, code: int) -> str:
    text = output.lower()
    if "winerror 10054" in text or "forcibly closed" in text:
        return (
            "YouTube оборвал соединение (WinError 10054). "
            "Обычно помогает повтор через минуту, VPN или другой интернет."
        )
    if "unable to download api page" in text:
        return (
            "Не удалось получить данные видео с YouTube. "
            "Проверь интернет/VPN и попробуй ещё раз."
        )
    if "sign in to confirm" in text or "bot" in text:
        return "YouTube просит проверку (капча/логин). Попробуй другую сеть или VPN."
    tail = "\n".join(line for line in output.splitlines() if line.strip())[-800:]
    return f"yt-dlp завершился с кодом {code}.\n{tail}"


def _build_ytdlp_cmd(ffmpeg: str, section: str, output_path: Path, url: str) -> list[str]:
    return _ytdlp_base_args(ffmpeg) + [
        "--download-sections",
        section,
        "--force-keyframes-at-cuts",
        # android/tv клиенты стабильнее при обрывах API (WinError 10054)
        "--extractor-args",
        "youtube:player_client=android,tv,web",
        # JS-challenge без локального node/deno
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
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(title)
    if not filename.lower().endswith(".mp4"):
        filename += ".mp4"
    return output_dir / filename


def download_clip(
    request: ClipRequest,
    on_log: Callable[[str], None] | None = None,
) -> ClipResult:
    log = app_logger()

    def ui_log(msg: str) -> None:
        log.info(msg)
        if on_log:
            on_log(msg)

    url = request.url.strip()
    if not url:
        log.error("Валидация: пустая ссылка")
        raise ClipperError("Ссылка на YouTube не указана")
    if "youtube.com" not in url and "youtu.be" not in url:
        log.error("Валидация: не YouTube URL: %s", url)
        raise ClipperError("Нужна ссылка на YouTube")

    start = parse_time(request.start)
    end = parse_time(request.end)
    if _time_to_seconds(end) <= _time_to_seconds(start):
        log.error("Валидация: end <= start (%s — %s)", start, end)
        raise ClipperError("Время окончания должно быть позже времени начала")

    output_path = build_output_path(request.output_dir, request.title)
    if output_path.exists():
        log.error("Файл уже существует: %s", output_path)
        raise ClipperError(f"Файл уже существует: {output_path}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    section = f"*{start}-{end}"
    cmd = _build_ytdlp_cmd(ffmpeg, section, output_path, url)

    log.info("--- новая загрузка ---")
    log.info("URL: %s", url)
    log.info("Отрезок: %s — %s", start, end)
    log.info("Выход: %s", output_path)
    log.info("ffmpeg: %s", ffmpeg)
    log.info("Команда: %s", " ".join(f'"{part}"' if " " in part else part for part in cmd))

    ui_log(f"Скачиваю отрезок {start} — {end}")
    ui_log(f"Сохраняю в: {output_path}")

    max_attempts = 3
    last_output = ""
    code = 1
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            wait_s = attempt * 2
            log.warning("Повтор %s/%s через %s сек", attempt, max_attempts, wait_s)
            ui_log(f"Повтор {attempt}/{max_attempts} через {wait_s} сек...")
            time.sleep(wait_s)

        log.info("Попытка %s/%s", attempt, max_attempts)
        code, last_output = _run_ytdlp(cmd, ui_log)
        log.debug("yt-dlp stdout/stderr (%s символов):\n%s", len(last_output), last_output)

        if code == 0:
            log.info("yt-dlp успех на попытке %s", attempt)
            break

        log.error("yt-dlp код %s на попытке %s", code, attempt)

        if "winerror 10054" not in last_output.lower() and attempt < max_attempts:
            if "unable to download" not in last_output.lower():
                break

    if code != 0:
        err = _friendly_error(last_output, code)
        log.error("Загрузка провалена: %s", err)
        raise ClipperError(err)

    if not output_path.exists():
        candidates = list(request.output_dir.glob(f"{output_path.stem}*.mp4"))
        if len(candidates) == 1:
            if candidates[0] != output_path:
                log.info("Переименование %s -> %s", candidates[0], output_path)
                candidates[0].rename(output_path)
        else:
            log.error("Файл не найден после загрузки. Кандидаты: %s", candidates)
            raise ClipperError("Файл не найден после загрузки")

    log.info("Готово: %s", output_path)
    ui_log("Готово!")
    return ClipResult(output_path=output_path)
