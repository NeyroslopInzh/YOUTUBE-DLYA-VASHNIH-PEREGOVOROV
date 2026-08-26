# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

Вырезка отрезков с YouTube в MP4. Качается **только нужный кусок**, не весь ролик.

**Лицензия:** [GNU GPL v3](LICENSE) — copyleft, форки только под GPL.

Desktop app + опциональное **Chromium-расширение** (Chrome, Opera, Edge) — Load unpacked, без магазинов.

## Структура репозитория

```
├── src/              # общий Python-код (Windows + Linux)
├── extension/        # Chromium extension (Load unpacked)
├── windows/          # exe, Inno Setup installer
├── linux/            # binary, install.sh (все дистри)
├── docs/             # инструкции (5 языков)
└── LICENSE
```

Бинарники — в [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

---

## Что скачать

| Нужно | Windows | Linux |
|-------|---------|-------|
| **Только app** | portable `.exe` | portable binary |
| **App + расширение** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |

После **установщика**: запусти app один раз — покажет путь к папке `extension` для Load unpacked (на языке интерфейса).

Расширение **не ставится автоматически** — Chrome/Opera не дают. Только вручную: режим разработчика → Load unpacked → папка из подсказки.

---

## Windows

### Только app (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → скачай `.exe` (длинное имя, без Setup) → двойной клик.

### App + расширение

1. `YVPClipper-Setup.exe` → установка (`yvp://`, папка extension)
2. Запусти app → прочитай подсказку про расширение
3. `chrome://extensions` или `opera://extensions` → Load unpacked → папка из подсказки

### Из исходников

```bat
windows\run.bat
windows\build-installer.bat   REM exe + Setup (нужен Inno Setup)
```

---

## Linux

**Зависимость:** `ffmpeg` в PATH.

### Только app (portable)

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### App + расширение

```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
yvp-clipper   # или yvp://start
```

Дальше — Load unpacked, как на Windows.

### Из исходников

```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

---

## Возможности

- Desktop GUI или расширение на YouTube (через bridge `127.0.0.1:8766`)
- `yvp://` — авто-запуск app из расширения, трей, закрытие после клипа
- **Языки:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- Иконка — флаг Узбекистана 🇺🇿

## Документация

| Язык | README | Инструкция |
|------|--------|------------|
| Русский | этот файл | [docs/INSTRUCTIONS.md](docs/INSTRUCTIONS.md) |
| English | [docs/README.en.md](docs/README.en.md) | [docs/INSTRUCTIONS.en.md](docs/INSTRUCTIONS.en.md) |
| עברית | [docs/README.he.md](docs/README.he.md) | [docs/INSTRUCTIONS.he.md](docs/INSTRUCTIONS.he.md) |
| हिन्दी | [docs/README.hi.md](docs/README.hi.md) | [docs/INSTRUCTIONS.hi.md](docs/INSTRUCTIONS.hi.md) |
| Oʻzbekcha | [docs/README.uz.md](docs/README.uz.md) | [docs/INSTRUCTIONS.uz.md](docs/INSTRUCTIONS.uz.md) |

Расширение: [extension/README.md](extension/README.md)

## Стек

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3
