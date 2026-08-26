# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

Десктопная программа для вырезки отрезков с YouTube в MP4.

**Ветка:** `standalone-app` — автономное приложение с GUI.  
*(Git не поддерживает пробелы в имени ветки; задумывалась как `standalone app`.)*

## Быстрый старт

| Способ | Файл | Описание |
|--------|------|----------|
| **1. Готовый EXE** | `release/windows/YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe` | Двойной клик, без Python и консоли |
| **2. CMD / BAT** | `run.bat` | Запуск из исходников через Python |
| **3. Сборка Windows** | `build_windows.bat` | Компиляция exe из Python-кода |
| **4. Сборка Linux** | `build_linux.sh` | Бинарник для Linux (сборка на Linux) |

Полная инструкция: **[INSTRUCTIONS.md](INSTRUCTIONS.md)**

## Возможности

- Ссылка на YouTube + время начала/конца + имя файла + папка сохранения
- Качается **только нужный отрезок**, не весь ролик
- Автосохранение полей при выходе (`settings.json`)
- Логи в `logs/clipper.log`

## Стек

Python · CustomTkinter · yt-dlp · ffmpeg (imageio-ffmpeg)

## Скачать готовый EXE

```
release/windows/YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe
```

## Разработка

```bat
py -m pip install -r requirements.txt
py main.py
```

## Лицензия

**GNU GPL v3** — свободное использование с копилефтом.

- Можно использовать, изучать, менять и распространять
- Производные работы тоже только под **GPL** — переиздавать под проприетарной лицензией нельзя
- При распространении нужно сохранять исходники и ту же лицензию

Полный текст: [LICENSE](LICENSE)
