# Полная инструкция

## Структура проекта

| Папка | Назначение |
|-------|------------|
| `src/` | Общий код приложения |
| `windows/` | `run.bat`, `build.bat`, PyInstaller spec |
| `linux/` | `run.sh`, `build.sh`, PyInstaller spec, PKGBUILD |
| `docs/` | Документация |

---

## Windows

### Готовый EXE
Скачай из [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → двойной клик.

### Исходники
```bat
windows\run.bat
```

### Сборка EXE
```bat
windows\build.bat
```
→ `dist\windows\`

---

## Linux

### Требования
- Python 3.10+
- `ffmpeg` в PATH
- `python3-tk` / `tk`

### Исходники
```bash
chmod +x linux/run.sh
./linux/run.sh
```

### Сборка бинарника
```bash
chmod +x linux/build.sh
./linux/build.sh
```
→ `dist/linux/`

Бинарник собран под glibc (Ubuntu CI) — работает на Arch, Debian, Fedora и др.

### Arch PKGBUILD
```bash
cd linux/packaging/arch
makepkg -sf
sudo pacman -U yvp-vashnie-peregovori-*.pkg.tar.zst
```

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
Если в логе `OPENSSL_3.3.0 not found` — это конфликт системного `yt-dlp` с библиотеками PyInstaller. Обновись до **v2.1.1+**: бинарник вызывает встроенный `yt-dlp`, системный не нужен.

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
