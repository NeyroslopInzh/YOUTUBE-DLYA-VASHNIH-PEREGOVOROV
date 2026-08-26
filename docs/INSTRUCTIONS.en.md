# Full instructions (English)

## Project layout

| Folder | Purpose |
|--------|---------|
| `src/` | Shared application code |
| `windows/` | `run.bat`, `build.bat`, PyInstaller spec |
| `linux/` | `run.sh`, `build.sh`, PyInstaller spec, PKGBUILD |
| `docs/` | Documentation |

---

## Windows

### Pre-built EXE
Download from [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → double-click.

### From source
```bat
windows\run.bat
```

### Build EXE
```bat
windows\build.bat
```
→ `dist\windows\`

---

## Linux

### Requirements
- Python 3.10+
- `ffmpeg` in PATH
- `python3-tk` / `tk`

### From source
```bash
chmod +x linux/run.sh
./linux/run.sh
```

### Build binary
```bash
chmod +x linux/build.sh
./linux/build.sh
```
→ `dist/linux/`

Binary is built against glibc (Ubuntu CI) — works on Arch, Debian, Fedora, etc.

### Arch PKGBUILD
```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
```

---

## UI fields

| Field | Format |
|-------|--------|
| Language | Русский, English, עברית, हिन्दी, Oʻzbekcha |
| Link | YouTube URL |
| Start / end | `MM:SS`, `HH:MM:SS`, or seconds |
| Title | mp4 filename without extension |
| Folder | any path, created automatically |

---

## Logs and settings

- `settings.json` — auto-save (including selected language)
- `logs/clipper.log` — full yt-dlp log
- Example: `src/settings.json.example`

---

## Troubleshooting

### WinError 10054
YouTube closed the connection → retry / VPN.

### ffmpeg code -11 (Linux)
```bash
sudo pacman -S ffmpeg   # Arch
sudo apt install ffmpeg # Debian
```

### Ctrl+C broken (Windows, Russian layout)
Update to v2.0.0+ — fixed via keycodes.

### «Videos» vs «Видео» folder
App picks XDG / `~/Videos` / `~/Видео` automatically.

---

## Release build (maintainers)

```bash
git tag v2.0.0
git push origin v2.0.0
```

GitHub Actions builds Windows + Linux artifacts (`release-builds.yml`).

---

## License

[GNU GPL v3](../LICENSE) — copyleft.
