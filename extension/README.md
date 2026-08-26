# Chromium extension — YVP Clipper

**Лицензия:** [GNU GPL v3](../LICENSE) — **copyleft**. MIT и прочая пермиссивная хуйня не применяется: форки, расширения и производные работы — **только под GPL v3+**, с открытым исходником.

Расширение для **Chromium** (Chrome, Edge, Brave, …): вырезка отрезка с **текущего** YouTube-видео.

Логика скачивания та же, что в desktop-приложении (`src/clipper.py`), но через **локальный companion** — в браузере yt-dlp/ffmpeg не запустить.

## Что умеет popup

| Поле | Поведение |
|------|-----------|
| Ссылка | **Нет поля** — берётся с открытой вкладки YouTube |
| Начало | Авто с `video.currentTime`, кнопка «↻ с плеера» |
| Конец | Вручную или кнопка «→ конец» от «+ секунд» |
| Название | По умолчанию — заголовок ролика |
| Куда сохранить | **Нет поля** — стандартное поведение Chrome (папка «Загрузки» или диалог «Сохранить как») |
| Настройки | **Не сохраняются** (каждый раз заново) |

## Быстрый старт

### 1. Companion (обязательно)

**Windows:**
```bat
extension\companion\run.bat
```

**Linux:**
```bash
chmod +x extension/companion/run.sh
./extension/companion/run.sh
```

Нужны: Python 3.10+, `ffmpeg`, `yt-dlp` (как для desktop `linux/run.sh`).

Companion слушает `http://127.0.0.1:8765`.

### 2. Установка расширения

1. Chrome → `chrome://extensions`
2. Включить **Режим разработчика**
3. **Загрузить распакованное** → папка `extension/chromium`

### 3. Использование

1. Открой YouTube `watch?v=...`, поставь на нужный момент (или смотри — начало подставится с плеера)
2. Клик по иконке расширения
3. Задай конец или «+ N сек» → «→ конец»
4. **Скачать отрезок** → файл уходит в **менеджер загрузок браузера**

Companion режет клип во временную папку, расширение забирает его через `chrome.downloads` — куда положить, решает Chrome (как в `chrome://settings/downloads`).

## Структура

```
extension/
├── chromium/          # MV3 расширение
│   ├── manifest.json
│   ├── popup.html/js/css
│   └── content.js     # читает URL, currentTime, title
└── companion/
    ├── server.py      # HTTP API → clipper.download_clip
    ├── run.bat
    └── run.sh
```

## API companion

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Проверка, что companion жив |
| POST | `/clip` | `{url, start, end, title}` → `{job_id}` |
| GET | `/jobs/{id}` | `{status, log[], filename?, download_url?}` |
| GET | `/jobs/{id}/file` | MP4 для `chrome.downloads` |

## Ветка

Разработка расширения — ветка **`browser-extension`**. Desktop-приложение — **`standalone-app`**.

## Лицензия

[GNU GPL v3](../LICENSE) — copyleft. Распространение бинарника расширения без исходников или под другой лицензией **запрещено**. Полный текст: `extension/LICENSE` (копия корневого LICENSE).

MIT **не используется** и не будет.
