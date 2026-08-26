# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

Вырезка отрезков с YouTube в MP4. Качается **только нужный кусок**, не весь ролик.

**Лицензия:** [GNU GPL v3](LICENSE) — copyleft, форки только под GPL.

## Структура репозитория

```
├── src/              # общий Python-код (Windows + Linux)
├── windows/          # запуск и сборка под Windows
├── linux/            # запуск, сборка, PKGBUILD для Arch
├── docs/             # подробная инструкция
└── LICENSE
```

Бинарники **не лежат в git** — только в [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

---

## Быстрая установка — Windows

### Вариант A: готовый EXE (рекомендуется)

**PowerShell** — скачать последний релиз:

```powershell
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*.exe" --dir .
```

Без `gh` — открой [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases), скачай `.exe`, двойной клик.

### Вариант B: из исходников

```bat
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
git checkout standalone-app
windows\run.bat
```

### Вариант C: собрать EXE самому

```bat
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
windows\build.bat
```

Результат: `dist\windows\`

---

## Быстрая установка — Linux

**Зависимость:** `ffmpeg` обязателен на всех дистрибутивах.

```bash
# Arch
sudo pacman -S ffmpeg

# Debian / Ubuntu
sudo apt install ffmpeg python3-tk

# Fedora
sudo dnf install ffmpeg python3-tkinter
```

### Вариант A: готовый бинарник из Releases

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### Вариант B: из исходников

```bash
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
git checkout standalone-app
chmod +x linux/run.sh
./linux/run.sh
```

### Вариант C: собрать бинарник самому

```bash
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
chmod +x linux/build.sh
./linux/build.sh
```

Результат: `dist/linux/`

### Вариант D: Arch — PKGBUILD

```bash
git clone https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV.git
cd YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
yvp-vashnie-peregovori
```

---

## Возможности

- Ссылка + время начала/конца + имя файла + папка
- Автосохранение полей (`settings.json` рядом с exe/бинарником)
- Логи: `logs/clipper.log`
- Русская раскладка: Ctrl+C/V/A работают на Windows
- Папка по умолчанию: `~/Видео/YouTubeClips` или `~/Videos/YouTubeClips`

## Подробнее

[docs/INSTRUCTIONS.md](docs/INSTRUCTIONS.md)

## Стек

Python · CustomTkinter · yt-dlp · ffmpeg
