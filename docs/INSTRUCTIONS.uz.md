# To'liq ko'rsatma (Oʻzbekcha)

## Loyiha tuzilmasi

| Papka | Vazifa |
|-------|--------|
| `src/` | Umumiy ilova kodi |
| `windows/` | PyInstaller spec, Inno Setup (`installer.iss`) |
| `linux/` | `run.sh`, `build.sh`, PKGBUILD |
| `docs/` | Hujjatlar |

---

## Windows

### Tayyor EXE
[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → ikki marta bosing.

### Manbadan
```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```
→ `dist\windows\`

---

## Linux

### Talablar
- Python 3.10+
- PATH da `ffmpeg`
- `python3-tk`

### Manbadan
```bash
chmod +x linux/run.sh
./linux/run.sh
```

### Binariy yig'ish
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

## UI maydonlari

| Maydon | Format |
|--------|--------|
| Til | Русский, English, עברית, हिन्दी, Oʻzbekcha |
| Havola | YouTube URL |
| Boshlanish / tugash | `MM:SS`, `HH:MM:SS`, yoki soniyalar |
| Nom | mp4 nomi, kengaytmasiz |
| Papka | istalgan yo'l, avtomatik yaratiladi |

---

## Loglar va sozlamalar

- `settings.json` — avtomatik saqlash (til bilan)
- `logs/clipper.log` — to'liq yt-dlp logi
- Namuna: `src/settings.json.example`

---

## Tez-tez muammolar

### WinError 10054
YouTube ulanishni uzdi → qayta urining / VPN.

### ffmpeg code -11 (Linux)
```bash
sudo pacman -S ffmpeg
sudo apt install ffmpeg
```

### Ctrl+C (Windows, rus klaviaturasi)
v2.0.0+ ga yangilang.

### «Videos» / «Видео» papkasi
Ilova avtomatik tanlaydi.

---

## Litsenziya

[GNU GPL v3](../LICENSE)
