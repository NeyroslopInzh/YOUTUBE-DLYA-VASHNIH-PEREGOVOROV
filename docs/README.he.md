# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

הורדת **רק הקטע הנבחר** מ-YouTube כ-MP4 — לא את כל הסרטון.

**רישיון:** [GNU GPL v3](../LICENSE) — copyleft; forks חייבים להישאר תחת GPL.

## מבנה המאגר

```
├── src/              # קוד Python משותף (Windows + Linux)
├── windows/          # הרצה ובנייה ב-Windows
├── linux/            # הרצה, בנייה, PKGBUILD ל-Arch
├── docs/             # תיעוד (שפות מרובות)
└── LICENSE
```

קבצים בינאריים **לא ב-git** — ב-[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

---

## התקנה מהירה — Windows

### אפשרות A: EXE מוכן (מומלץ)

```powershell
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*.exe" --dir .
```

ללא `gh`: [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → הורד `.exe` → לחיצה כפולה.

### אפשרות B: מקוד מקור

```bat
windows\run.bat
```

### אפשרות C: בניית EXE

```bat
windows\build.bat
```

→ `dist\windows\`

---

## התקנה מהירה — Linux

**חובה:** `ffmpeg` בכל ההפצות.

```bash
sudo pacman -S ffmpeg    # Arch
sudo apt install ffmpeg python3-tk   # Debian/Ubuntu
sudo dnf install ffmpeg python3-tkinter   # Fedora
```

### אפשרות A: בינארי מ-Releases

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### אפשרות B: מקוד מקור

```bash
chmod +x linux/run.sh
./linux/run.sh
```

### אפשרות C: בניית בינארי

```bash
chmod +x linux/build.sh
./linux/build.sh
```

→ `dist/linux/`

### אפשרות D: Arch — PKGBUILD

```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
yvp-vashnie-peregovori
```

---

## יכולות

- קישור YouTube + זמן התחלה/סיום + שם קובץ + תיקייה
- **שפות ממשק:** Русский, English, עברית, हिन्दी, Oʻzbekcha — בחירה ב-«שפה», נשמר ב-`settings.json`
- שמירה אוטומטית של שדות
- לוגים: `logs/clipper.log`
- מקלדת רוסית: Ctrl+C/V/A ב-Windows
- תיקייה ברירת מחדל: `~/Videos/YouTubeClips` או `~/Видео/YouTubeClips`

## תיעוד נוסף

| שפה | README | הוראות |
|-----|--------|--------|
| Русский | [../README.md](../README.md) | [INSTRUCTIONS.md](INSTRUCTIONS.md) |
| English | [README.en.md](README.en.md) | [INSTRUCTIONS.en.md](INSTRUCTIONS.en.md) |
| עברית | קובץ זה | [INSTRUCTIONS.he.md](INSTRUCTIONS.he.md) |
| हिन्दी | [README.hi.md](README.hi.md) | [INSTRUCTIONS.hi.md](INSTRUCTIONS.hi.md) |
| Oʻzbekcha | [README.uz.md](README.uz.md) | [INSTRUCTIONS.uz.md](INSTRUCTIONS.uz.md) |

## מחסנית

Python · CustomTkinter · yt-dlp · ffmpeg
