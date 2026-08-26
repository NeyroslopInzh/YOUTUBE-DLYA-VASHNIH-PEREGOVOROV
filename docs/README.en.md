# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

Download **only the selected segment** from YouTube as MP4 — not the full video.

**License:** [GNU GPL v3](../LICENSE) — copyleft; forks must stay under GPL.

## Repository layout

```
├── src/              # shared Python code (Windows + Linux)
├── windows/          # run and build on Windows
├── linux/            # run, build, Arch PKGBUILD
├── docs/             # documentation (multiple languages)
└── LICENSE
```

Binaries are **not in git** — get them from [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

---

## Quick install — Windows

### Option A: pre-built EXE (recommended)

**PowerShell:**

```powershell
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*.exe" --dir .
```

Without `gh`: open [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases), download the `.exe`, double-click.

### Option B: from source

```bat
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
git checkout standalone-app
windows\run.bat
```

### Option C: build EXE yourself

```bat
windows\build.bat
```

Output: `dist\windows\`

---

## Quick install — Linux

**Required:** `ffmpeg` on all distros.

```bash
# Arch
sudo pacman -S ffmpeg

# Debian / Ubuntu
sudo apt install ffmpeg python3-tk

# Fedora
sudo dnf install ffmpeg python3-tkinter
```

### Option A: binary from Releases

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### Option B: from source

```bash
chmod +x linux/run.sh
./linux/run.sh
```

### Option C: build binary

```bash
chmod +x linux/build.sh
./linux/build.sh
```

Output: `dist/linux/`

### Option D: Arch — PKGBUILD

```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
yvp-vashnie-peregovori
```

---

## Features

- YouTube URL + start/end time + filename + output folder
- **UI languages:** Русский, English, עברית, हिन्दी, Oʻzbekcha — pick from the **Language** dropdown; saved in `settings.json`
- Auto-save fields (`settings.json` next to exe/binary)
- Logs: `logs/clipper.log`
- Russian keyboard layout: Ctrl+C/V/A on Windows
- Default folder: `~/Videos/YouTubeClips` or `~/Видео/YouTubeClips`

## More docs

| Language | README | Instructions |
|----------|--------|--------------|
| Русский | [../README.md](../README.md) | [INSTRUCTIONS.md](INSTRUCTIONS.md) |
| English | this file | [INSTRUCTIONS.en.md](INSTRUCTIONS.en.md) |
| עברית | [README.he.md](README.he.md) | [INSTRUCTIONS.he.md](INSTRUCTIONS.he.md) |
| हिन्दी | [README.hi.md](README.hi.md) | [INSTRUCTIONS.hi.md](INSTRUCTIONS.hi.md) |
| Oʻzbekcha | [README.uz.md](README.uz.md) | [INSTRUCTIONS.uz.md](INSTRUCTIONS.uz.md) |

## Stack

Python · CustomTkinter · yt-dlp · ffmpeg
