"""Файловое логирование."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = _app_dir()
LOG_DIR = APP_DIR / "logs"
LOG_FILE = LOG_DIR / "clipper.log"

_LOGGER: logging.Logger | None = None


def get_log_dir() -> Path:
    return LOG_DIR


def get_log_file() -> Path:
    return LOG_FILE


def setup_logging() -> logging.Logger:
    global _LOGGER
    if _LOGGER is not None:
        return _LOGGER

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("yvp_vashnie_peregovori")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _LOGGER = logger
    logger.info("=" * 60)
    logger.info("Сессия запущена")
    logger.info("Python: %s", sys.version.replace("\n", " "))
    logger.info("Лог-файл: %s", LOG_FILE)
    return logger


def logger() -> logging.Logger:
    if _LOGGER is None:
        return setup_logging()
    return _LOGGER
