# הוראות מלאות (עברית)

## מבנה הפרויקט

| תיקייה | תפקיד |
|--------|--------|
| `src/` | קוד משותף |
| `windows/` | `run.bat`, `build.bat`, PyInstaller |
| `linux/` | `run.sh`, `build.sh`, PKGBUILD |
| `docs/` | תיעוד |

---

## Windows

### EXE מוכן
[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → לחיצה כפולה.

### מקוד מקור
```bat
windows\run.bat
```

### בניית EXE
```bat
windows\build.bat
```
→ `dist\windows\`

---

## Linux

### דרישות
- Python 3.10+
- `ffmpeg` ב-PATH
- `python3-tk`

### מקוד מקור
```bash
chmod +x linux/run.sh
./linux/run.sh
```

### בניית בינארי
```bash
chmod +x linux/build.sh
./linux/build.sh
```
→ `dist/linux/`

### Arch PKGBUILD
```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
```

---

## שדות בממשק

| שדה | פורמט |
|-----|--------|
| שפה | Русский, English, עברית, हिन्दी, Oʻzbekcha |
| קישור | URL של YouTube |
| התחלה / סיום | `MM:SS`, `HH:MM:SS`, או שניות |
| שם | שם mp4 ללא סיומת |
| תיקייה | נוצרת אוטומטית |

---

## לוגים והגדרות

- `settings.json` — שמירה אוטומטית (כולל שפה)
- `logs/clipper.log` — לוג מלא
- דוגמה: `src/settings.json.example`

---

## בעיות נפוצות

### WinError 10054
YouTube ניתק → נסה שוב / VPN.

### ffmpeg code -11 (Linux)
```bash
sudo pacman -S ffmpeg
sudo apt install ffmpeg
```

### Ctrl+C (Windows, פריסה רוסית)
עדכן ל-v2.0.0+.

### תיקיית «Videos» / «Видео»
האפליקציה בוחרת אוטומטית.

---

## רישיון

[GNU GPL v3](../LICENSE)
