# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

YouTube से **सिर्फ चुना हुआ हिस्सा** MP4 में — पूरा वीडियो नहीं।

**लाइसेंस:** [GNU GPL v3](../LICENSE) — copyleft; forks GPL के तहत ही रहें।

## रिपॉज़िटरी संरचना

```
├── src/              # साझा Python कोड (Windows + Linux)
├── windows/          # Windows पर चलाना और बिल्ड
├── linux/            # Linux run, build, Arch PKGBUILD
├── docs/             # दस्तावेज़ (कई भाषाएँ)
└── LICENSE
```

बाइनरी **git में नहीं** — [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) से लें।

---

## त्वरित इंस्टॉल — Windows

### विकल्प A: तैयार EXE (अनुशंसित)

```powershell
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*.exe" --dir .
```

`gh` के बिना: [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → `.exe` डाउनलोड → डबल क्लिक।

### विकल्प B: सोर्स से

```bat
windows\run.bat
```

### विकल्प C: EXE बनाएँ

```bat
windows\build.bat
```

→ `dist\windows\`

---

## त्वरित इंस्टॉल — Linux

**ज़रूरी:** सभी distro पर `ffmpeg`।

```bash
sudo pacman -S ffmpeg    # Arch
sudo apt install ffmpeg python3-tk   # Debian/Ubuntu
sudo dnf install ffmpeg python3-tkinter   # Fedora
```

### विकल्प A: Releases से बाइनरी

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### विकल्प B: सोर्स से

```bash
chmod +x linux/run.sh
./linux/run.sh
```

### विकल्प C: बाइनरी बिल्ड

```bash
chmod +x linux/build.sh
./linux/build.sh
```

→ `dist/linux/`

### विकल्प D: Arch — PKGBUILD

```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
yvp-vashnie-peregovori
```

---

## सुविधाएँ

- YouTube लिंक + शुरुआत/अंत समय + फ़ाइल नाम + फ़ोल्डर
- **UI भाषाएँ:** Русский, English, עברית, हिन्दी, Oʻzbekcha — «भाषा» ड्रॉपडाउन; `settings.json` में सेव
- फ़ील्ड ऑटो-सेव (`settings.json`)
- लॉग: `logs/clipper.log`
- रूसी कीबोर्ड: Windows पर Ctrl+C/V/A
- डिफ़ॉल्ट फ़ोल्डर: `~/Videos/YouTubeClips` या `~/Видео/YouTubeClips`

## अन्य भाषाओं में दस्तावेज़

| भाषा | README | निर्देश |
|------|--------|---------|
| Русский | [../README.md](../README.md) | [INSTRUCTIONS.md](INSTRUCTIONS.md) |
| English | [README.en.md](README.en.md) | [INSTRUCTIONS.en.md](INSTRUCTIONS.en.md) |
| עברית | [README.he.md](README.he.md) | [INSTRUCTIONS.he.md](INSTRUCTIONS.he.md) |
| हिन्दी | यह फ़ाइल | [INSTRUCTIONS.hi.md](INSTRUCTIONS.hi.md) |
| Oʻzbekcha | [README.uz.md](README.uz.md) | [INSTRUCTIONS.uz.md](INSTRUCTIONS.uz.md) |

## स्टैक

Python · CustomTkinter · yt-dlp · ffmpeg
