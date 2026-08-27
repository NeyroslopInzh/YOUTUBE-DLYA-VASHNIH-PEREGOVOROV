# पूर्ण निर्देश (हिन्दी)

## प्रोजेक्ट संरचना

| फ़ोल्डर | उद्देश्य |
|---------|----------|
| `src/` | साझा ऐप कोड |
| `windows/` | PyInstaller spec, Inno Setup (`installer.iss`) |
| `linux/` | `run.sh`, `build.sh`, PKGBUILD |
| `docs/` | दस्तावेज़ |

---

## Windows

### तैयार EXE
[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → डबल क्लिक।

### सोर्स से
```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### EXE बिल्ड
```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```
→ `dist\windows\`

---

## Linux

### आवश्यकताएँ
- Python 3.10+
- PATH में `ffmpeg`
- `python3-tk`

### सोर्स से
```bash
chmod +x linux/run.sh
./linux/run.sh
```

### बाइनरी बिल्ड
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

## UI फ़ील्ड

| फ़ील्ड | प्रारूप |
|--------|---------|
| भाषा | Русский, English, עברית, हिन्दी, Oʻzbekcha |
| लिंक | YouTube URL |
| शुरुआत / अंत | `MM:SS`, `HH:MM:SS`, या सेकंड |
| नाम | mp4 नाम, बिना extension |
| फ़ोल्डर | कोई भी पथ, अपने आप बनता है |

---

## लॉग और सेटिंग

- `settings.json` — ऑटो-सेव (भाषा सहित)
- `logs/clipper.log` — पूरा yt-dlp लॉग
- उदाहरण: `src/settings.json.example`

---

## सामान्य समस्याएँ

### WinError 10054
YouTube ने कनेक्शन तोड़ा → दोबारा / VPN।

### ffmpeg code -11 (Linux)
```bash
sudo pacman -S ffmpeg
sudo apt install ffmpeg
```

### Ctrl+C (Windows, रूसी लेआउट)
v2.0.0+ अपडेट करें।

### «Videos» / «Видео» फ़ोल्डर
ऐप स्वचालित चुनता है।

---

## लाइसेंस

[GNU GPL v3](../LICENSE)
