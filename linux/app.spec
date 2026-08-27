# -*- mode: python ; coding: utf-8 -*-

import os
import sys

from PyInstaller.utils.hooks import collect_all

SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))
ROOT = os.path.abspath(os.path.join(SPEC_DIR, ".."))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

from app_name import APP_NAME  # noqa: E402

APP_NAME_STR = APP_NAME
ICON_SRC = os.path.join(ROOT, "extension", "icons", "icon48.png")
PRICOL_GIF = os.path.join(ROOT, "assets", "pricol.gif")

EXCLUDES = [
    "matplotlib",
    "numpy",
    "pandas",
    "scipy",
    "pytest",
    "setuptools",
    "distutils",
    "lib2to3",
    "unittest",
    "pydoc",
    "doctest",
    "tkinter.test",
    "imageio_ffmpeg",
]

datas = []
binaries = []
hiddenimports = []

for package in ("customtkinter", "yt_dlp", "pystray"):
    pkg_datas, pkg_binaries, pkg_hidden = collect_all(package)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hidden

if os.path.isfile(ICON_SRC):
    datas.append((ICON_SRC, "assets"))
if os.path.isfile(PRICOL_GIF):
    datas.append((PRICOL_GIF, "assets"))

a = Analysis(
    [os.path.join(SRC, "main.py")],
    pathex=[SRC],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports
    + [
        "clipper",
        "app_log",
        "settings",
        "app_name",
        "paths",
        "keyboard",
        "i18n",
        "bridge_server",
        "chrome_downloads",
        "protocol",
        "tray",
        "install_paths",
        "flag_icons",
        "uzbek_flag",
        "app_version",
        "pricol_gif",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME_STR,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
