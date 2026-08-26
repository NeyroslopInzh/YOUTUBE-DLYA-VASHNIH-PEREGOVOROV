# Инструкция — YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

Программа вырезает нужный отрезок с YouTube и сохраняет его в MP4.

---

## Способ 1. Готовый EXE (Windows, без консоли)

**Для кого:** просто скачал и пользуешься.

1. Открой папку `release/windows/`
2. Дважды кликни **`YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe`**
3. Заполни поля (или они подтянутся из прошлой сессии)
4. Нажми **Скачать отрезок**

Консоль не нужна. Python ставить не нужно.

> При первом запуске рядом с exe появятся `logs/` и `settings.json`.

---

## Способ 2. Запуск через CMD (BAT)

**Для кого:** есть Python, хочешь запускать из исходников.

1. Установи **Python 3.10+** с [python.org](https://www.python.org/downloads/)  
   При установке отметь **Add Python to PATH**.
2. Скачай/клонируй проект.
3. Дважды кликни **`run.bat`**  
   Или из CMD:
   ```bat
   cd "путь\к\проекту"
   run.bat
   ```
4. BAT сам поставит зависимости и откроет окно программы.

---

## Способ 3. Сборка EXE из исходников (Windows)

**Для кого:** менял код и хочешь пересобрать exe.

1. Python 3.10+ в PATH.
2. Запусти **`build_windows.bat`**  
   Или вручную:
   ```bat
   py -m pip install -r requirements.txt -r requirements-build.txt
   py -m PyInstaller app.spec --noconfirm
   copy "dist\YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe" "release\windows\"
   ```
3. Готовый файл: `release/windows/YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe`

---

## Способ 4. Сборка под Linux

**Для кого:** Linux без Python или хочешь один бинарник.

> Linux-бинарник собирается **на Linux-машине** (кросс-компиляция с Windows не поддерживается).

1. Установи Python 3.10+ и pip.
2. В терминале:
   ```bash
   cd /path/to/project
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
3. Запуск:
   ```bash
   ./release/linux/YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
   ```

Если нужен только исходный запуск без сборки:
```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

---

## Поля в интерфейсе

| Поле | Пример | Формат |
|------|--------|--------|
| Ссылка YouTube | `https://youtu.be/...` | URL |
| Начало отрезка | `6:01` или `366` | MM:SS, HH:MM:SS или секунды |
| Конец отрезка | `6:07` | то же |
| Название файла | `мой_клип` | без `.mp4` |
| Папка сохранения | `D:\clips` | любой путь |

---

## Автосохранение

При закрытии программы все поля сохраняются в **`settings.json`** рядом с exe/скриптом.  
При следующем запуске подставятся автоматически.

Пример: `settings.json.example`

---

## Логи

Файл: **`logs/clipper.log`**

Пишется:
- URL, отрезок, путь сохранения
- команда yt-dlp и её вывод
- ошибки и повторы

В GUI кнопка **Логи** открывает файл в проводнике.

---

## Требования

- Windows 10+ или Linux с GUI (X11/Wayland)
- Интернет
- ~100 МБ места под программу

Зависимости (ставятся автоматически при bat/сборке):
- `yt-dlp` — скачивание
- `customtkinter` — интерфейс
- `imageio-ffmpeg` — ffmpeg в комплекте

---

## Частые проблемы

### WinError 10054 / Unable to download API page
YouTube оборвал соединение. Попробуй:
- повтор через минуту
- VPN / другую сеть

### Файл уже существует
Переименуй клип или удали старый MP4 в папке сохранения.

### ffmpeg exited with code -11 (Linux)
Bundled ffmpeg в exe на Linux может падать. Поставь системный:

```bash
sudo pacman -S ffmpeg
```

После этого перезапусти приложение — будет использован `/usr/bin/ffmpeg`.

Нужен Tk:
```bash
# Ubuntu/Debian
sudo apt install python3-tk
```

---

## Структура проекта

```
├── main.py                  # GUI
├── app_name.py              # название приложения
├── clipper.py               # логика yt-dlp
├── app_log.py               # файловые логи
├── settings.py              # автосохранение полей
├── run.bat                  # запуск через CMD (Windows)
├── build_windows.bat        # сборка exe (Windows)
├── build_linux.sh           # сборка бинарника (Linux)
├── app.spec                 # конфиг PyInstaller
├── requirements.txt
├── requirements-build.txt
├── release/
│   ├── windows/
│   │   └── YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL.exe
│   └── linux/
│       └── YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL
├── INSTRUCTIONS.md          # эта инструкция
└── README.md
```
