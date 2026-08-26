# Linux

- `run.sh` — запуск из исходников (нужен системный `ffmpeg`)
- `build.sh` — сборка бинарника в `dist/linux/`
- `app.spec` — PyInstaller без bundled ffmpeg (легче)
- `packaging/arch/` — PKGBUILD для Arch

```bash
sudo pacman -S ffmpeg python python-pip tk
chmod +x linux/run.sh && ./linux/run.sh
```
