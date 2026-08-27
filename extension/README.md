# Browser extension (Chromium)

**Лицензия:** [GNU GPL v3](../LICENSE)

Расширение для Chrome, Opera, Edge, Brave — **только Load unpacked**, без магазинов.

Имя расширения совпадает с desktop app:  
`YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL`

## Установка

### Вместе с приложением (рекомендуется)

Скачай **установщик** из [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases):

| ОС | Файл |
|----|------|
| Windows | `YVPClipper-Setup.exe` |
| Linux | `YVPClipper-linux-installer.tar.gz` → `./install.sh` |

После установки запусти desktop app **один раз** — покажет путь к папке расширения на твоём языке.

### Только расширение (из git)

Папка для Load unpacked: `extension/` (этот каталог).

### Только расширение (из Releases)

| ОС | Архив |
|----|-------|
| Windows | `YVPClipper-extension.zip` |
| Linux | `YVPClipper-extension.tar.gz` |

Распакуй → Load unpacked на папку с `manifest.json`. Desktop app — отдельно (portable exe/binary из Releases).

**Где лежит app после установщика:**

| ОС | App | Extension |
|----|-----|-----------|
| Windows | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| Linux | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

(`$XDG_DATA_HOME/yvp-clipper/` если `XDG_DATA_HOME` задан.)

## Load unpacked

1. Открой `chrome://extensions` или `opera://extensions` **сам**
2. Режим разработчика → **Load unpacked** / «Загрузить распакованное»
3. Выбери папку `extension` (из установки или из репозитория)

## Как работает

```
YouTube → бар «Скачать отрезок» под видео → маркеры на прогрессбаре → yvp:// / HTTP :8766 → clipper
```

Либо через popup расширения (иконка в панели Chrome).

**На странице watch:** под плеером бар YVP → «Скачать отрезок» → синий/зелёный маркеры на таймлайне (старт = текущая позиция, конец +10 с) → «Скачать».

Аппу держать открытой не нужно — расширение поднимет через `yvp://` (трей, авто-закрытие после клипа).

## Разработка

```bat
py scripts\sync_extension_manifest.py
```

Обновляет `manifest.json` (имя из `src/app_name.py`).

Reload в `chrome://extensions` после изменений.
