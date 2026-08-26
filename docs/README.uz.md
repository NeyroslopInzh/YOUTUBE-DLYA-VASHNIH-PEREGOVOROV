# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

YouTube dan **faqat tanlangan qism** MP4 sifatida — butun video emas.

**Litsenziya:** [GNU GPL v3](../LICENSE) — copyleft; fork lar GPL ostida qolishi kerak.

## Repozitoriy tuzilmasi

```
├── src/              # umumiy Python kodi (Windows + Linux)
├── windows/          # Windows da ishga tushirish va build
├── linux/            # Linux run, build, Arch PKGBUILD
├── docs/             # hujjatlar (bir nechta tillar)
└── LICENSE
```

Binariy fayllar **git da yo'q** — [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

---

## Tez o'rnatish — Windows

### A variant: tayyor EXE (tavsiya)

```powershell
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*.exe" --dir .
```

`gh` siz: [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → `.exe` yuklab oling → ikki marta bosing.

### B variant: manbadan

```bat
windows\run.bat
```

### C variant: EXE yig'ish

```bat
windows\build.bat
```

→ `dist\windows\`

---

## Tez o'rnatish — Linux

**Majburiy:** barcha distro larda `ffmpeg`.

```bash
sudo pacman -S ffmpeg    # Arch
sudo apt install ffmpeg python3-tk   # Debian/Ubuntu
sudo dnf install ffmpeg python3-tkinter   # Fedora
```

### A variant: Releases dan binariy

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### B variant: manbadan

```bash
chmod +x linux/run.sh
./linux/run.sh
```

### C variant: binariy yig'ish

```bash
chmod +x linux/build.sh
./linux/build.sh
```

→ `dist/linux/`

### D variant: Arch — PKGBUILD

```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
yvp-vashnie-peregovori
```

---

## Imkoniyatlar

- YouTube havolasi + boshlanish/tugash vaqti + fayl nomi + papka
- **UI tillari:** Русский, English, עברית, हिन्दी, Oʻzbekcha — «Til» ro'yxatidan; `settings.json` da saqlanadi
- Maydonlar avtomatik saqlanadi (`settings.json`)
- Loglar: `logs/clipper.log`
- Rus klaviaturasi: Windows da Ctrl+C/V/A
- Standart papka: `~/Videos/YouTubeClips` yoki `~/Видео/YouTubeClips`

## Boshqa tillardagi hujjatlar

| Til | README | Ko'rsatma |
|-----|--------|-----------|
| Русский | [../README.md](../README.md) | [INSTRUCTIONS.md](INSTRUCTIONS.md) |
| English | [README.en.md](README.en.md) | [INSTRUCTIONS.en.md](INSTRUCTIONS.en.md) |
| עברית | [README.he.md](README.he.md) | [INSTRUCTIONS.he.md](INSTRUCTIONS.he.md) |
| हिन्दी | [README.hi.md](README.hi.md) | [INSTRUCTIONS.hi.md](INSTRUCTIONS.hi.md) |
| Oʻzbekcha | bu fayl | [INSTRUCTIONS.uz.md](INSTRUCTIONS.uz.md) |

## Stack

Python · CustomTkinter · yt-dlp · ffmpeg
