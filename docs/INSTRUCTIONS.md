# Полная инструкция

## Структура проекта

| Папка | Назначение |
|-------|------------|
| `src/` | Общий код приложения |
| `extension/` | Chromium-расширение (Load unpacked) |
| `windows/` | portable exe, Inno Setup (`YVPClipper-Setup.exe`) |
| `linux/` | portable binary, `install.sh` (все дистри) |
| `docs/` | Документация |

---

## Windows

### Только app
Portable `.exe` из [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) (файл без «Setup» в имени).

### App + расширение
1. `YVPClipper-Setup.exe`
2. Запусти app — диалог с путём к папке extension
3. Браузер → режим разработчика → Load unpacked

### Исходники / сборка
```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

---

## Linux

### Требования
- `ffmpeg` в PATH

### Только app
Portable binary из Releases.

### App + расширение
```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
```

### Исходники / сборка
```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

---

## Расширение

[extension/README.md](../extension/README.md) — Load unpacked, без Chrome Web Store.

---

## Поля интерфейса

| Поле | Формат |
|------|--------|
| Язык | Русский, English, עברית, हिन्दी, Oʻzbekcha |
| Ссылка | URL YouTube |
| Начало / конец | `MM:SS`, `HH:MM:SS`, секунды |
| Название | имя mp4 без расширения |
| Папка | любой путь, создаётся автоматически |

---

## Логи и настройки

- `settings.json` — автосохранение полей
- `logs/clipper.log` — полный лог yt-dlp
- Пример настроек: `src/settings.json.example`

---

## Частые проблемы

### WinError 10054
YouTube оборвал соединение → повтор / VPN.

### ffmpeg code -11 (Linux)
```bash
sudo pacman -S ffmpeg   # Arch
sudo apt install ffmpeg # Debian
```

### OpenSSL / libcrypto.so.3 (Linux, бинарник из Releases)
Если в логе `OPENSSL_3.3.0 not found` — обновись до **v2.1.1+**.

### Приложение «клонируется» / Fontconfig warning (Linux, v2.1.1)
Обновись до **v2.1.2+**: yt-dlp вызывается внутри процесса.

### Скачивается всё видео, а не отрезок (Linux, v2.1.2)
Обновись до **v2.1.3+**: исправлен API-параметр `download_ranges` (in-process режим игнорировал `--download-sections`).

### Ctrl+C не работает (Windows, русская раскладка)
Обновись до v2.0.0+ — исправлено через keycode.

### Папка «Видео» vs «Videos»
Приложение само ищет XDG / `~/Видео` / `~/Videos`.

---

## Сборка релиза (maintainers)

```bash
git tag v2.0.0
git push origin v2.0.0
```

GitHub Actions соберёт Windows + Linux арtefacts автоматически (workflow `release-builds.yml`).

---

## Лицензия

[GNU GPL v3](../LICENSE) — copyleft.
