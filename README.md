# YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

<details open>
<summary>Русский</summary>

Вырезка отрезков с YouTube в MP4. Качается **только нужный кусок**, не весь ролик.

**Лицензия:** [GNU GPL v3](LICENSE) — copyleft, форки только под GPL.

Desktop app + опциональное **Chromium-расширение** (Chrome, Opera, Edge) — Load unpacked, без магазинов.

</details>

<details>
<summary>English</summary>

Cut segments from YouTube as MP4. Downloads **only the selected clip**, not the full video.

**License:** [GNU GPL v3](LICENSE) — copyleft; forks must stay under GPL.

Desktop app + optional **Chromium extension** (Chrome, Opera, Edge) — Load unpacked, no stores.

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

חיתוך קטעים מ-YouTube ל-MP4. מוריד **רק את הקטע הנבחר**, לא את כל הסרטון.

**רישיון:** [GNU GPL v3](LICENSE) — copyleft; forks חייבים להישאר תחת GPL.

אפליקציית Desktop + **הרחבת Chromium** אופציונלית (Chrome, Opera, Edge) — Load unpacked, בלי חנויות.

</div>

</details>

<details>
<summary>हिन्दी</summary>

YouTube से MP4 में क्लिप कट। **सिर्फ चुना हुआ टुकड़ा** डाउनलोड होता है, पूरा वीडियो नहीं।

**लाइसेंस:** [GNU GPL v3](LICENSE) — copyleft; forks सिर्फ GPL के तहत।

Desktop app + वैकल्पिक **Chromium एक्सटेंशन** (Chrome, Opera, Edge) — Load unpacked, स्टोर नहीं।

</details>

<details>
<summary>Oʻzbekcha</summary>

YouTube dan MP4 qirqim. **Faqat kerakli qism** yuklanadi, butun video emas.

**Litsenziya:** [GNU GPL v3](LICENSE) — copyleft; forklar faqat GPL ostida.

Desktop app + ixtiyoriy **Chromium kengaytmasi** (Chrome, Opera, Edge) — Load unpacked, doʻkonlarsiz.

</details>

---

## Структура репозитория

<details open>
<summary>Русский</summary>

```
├── src/              # общий Python-код (Windows + Linux)
├── extension/        # Chromium extension (Load unpacked)
├── windows/          # exe, Inno Setup installer
├── linux/            # binary, install.sh (все дистри)
├── docs/             # инструкции (5 языков)
└── LICENSE
```

Бинарники — в [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

</details>

<details>
<summary>English</summary>

```
├── src/              # shared Python code (Windows + Linux)
├── extension/        # Chromium extension (Load unpacked)
├── windows/          # exe, Inno Setup installer
├── linux/            # binary, install.sh (all distros)
├── docs/             # docs (5 languages)
└── LICENSE
```

Binaries are in [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

```
├── src/              # קוד Python משותף (Windows + Linux)
├── extension/        # הרחבת Chromium (Load unpacked)
├── windows/          # exe, מתקין Inno Setup
├── linux/            # binary, install.sh (כל ההפצות)
├── docs/             # הוראות (5 שפות)
└── LICENSE
```

בינאריים — ב-[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases).

</div>

</details>

<details>
<summary>हिन्दी</summary>

```
├── src/              # साझा Python कोड (Windows + Linux)
├── extension/        # Chromium एक्सटेंशन (Load unpacked)
├── windows/          # exe, Inno Setup इंस्टॉलर
├── linux/            # binary, install.sh (सभी distro)
├── docs/             # निर्देश (5 भाषाएँ)
└── LICENSE
```

बाइनरी — [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) में।

</details>

<details>
<summary>Oʻzbekcha</summary>

```
├── src/              # umumiy Python kodi (Windows + Linux)
├── extension/        # Chromium kengaytmasi (Load unpacked)
├── windows/          # exe, Inno Setup o‘rnatuvchi
├── linux/            # binary, install.sh (barcha distrolar)
├── docs/             # ko‘rsatmalar (5 til)
└── LICENSE
```

Binariylar — [Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) da.

</details>

---

## Что скачать

<details open>
<summary>Русский</summary>

| Нужно | Windows | Linux |
|-------|---------|-------|
| **Только app** | portable `.exe` | portable binary |
| **App + расширение** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |
| **Только расширение** | `YVPClipper-extension.zip` | `YVPClipper-extension.tar.gz` |

После **установщика**: запусти app один раз — покажет путь к папке `extension` для Load unpacked (на языке интерфейса).

Расширение **не ставится автоматически** — Chrome/Opera не дают. Только вручную: режим разработчика → Load unpacked → папка из подсказки.

### Где лежит приложение (для расширения)

Расширение стучится в desktop app по `http://127.0.0.1:8766` — **путь к exe не важен**, главное чтобы app была запущена (или поднялась через `yvp://`).

Если ставил **установщик**, layout такой:

| ОС | Каталог приложения | Папка для Load unpacked |
|----|--------------------|-------------------------|
| **Windows** | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| **Linux** | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

На Linux при заданном `XDG_DATA_HOME` вместо `~/.local/share` будет `$XDG_DATA_HOME/yvp-clipper/`.

**Без установщика (portable + архив расширения):** положи app и распакованное расширение куда угодно → запусти app → Load unpacked на папку с `manifest.json`. Протокол `yvp://` не зарегистрирован — первый раз app нужно запустить самому (или держать открытой).

</details>

<details>
<summary>English</summary>

| Need | Windows | Linux |
|------|---------|-------|
| **App only** | portable `.exe` | portable binary |
| **App + extension** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |
| **Extension only** | `YVPClipper-extension.zip` | `YVPClipper-extension.tar.gz` |

After the **installer**: launch the app once — it shows the path to the `extension` folder for Load unpacked (in the UI language).

The extension is **not installed automatically** — Chrome/Opera don’t allow that. Manual only: Developer mode → Load unpacked → folder from the tip.

### Where the app lives (for the extension)

The extension talks to the desktop app at `http://127.0.0.1:8766` — **exe path doesn’t matter**; the app must be running (or started via `yvp://`).

If you used the **installer**, layout is:

| OS | App directory | Load unpacked folder |
|----|---------------|----------------------|
| **Windows** | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| **Linux** | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

On Linux, if `XDG_DATA_HOME` is set, use `$XDG_DATA_HOME/yvp-clipper/` instead of `~/.local/share`.

**Without installer (portable + extension archive):** put the app and unpacked extension anywhere → start the app → Load unpacked on the folder with `manifest.json`. `yvp://` is not registered — start the app yourself the first time (or keep it open).

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

| צורך | Windows | Linux |
|------|---------|-------|
| **רק אפליקציה** | portable `.exe` | portable binary |
| **אפליקציה + הרחבה** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |
| **רק הרחבה** | `YVPClipper-extension.zip` | `YVPClipper-extension.tar.gz` |

אחרי **המתקין**: הפעל את האפליקציה פעם אחת — תוצג נתיב לתיקיית `extension` ל-Load unpacked (בשפת הממשק).

ההרחבה **לא מותקנת אוטומטית** — Chrome/Opera לא מאפשרים. רק ידנית: מצב מפתח → Load unpacked → התיקייה מהטיפ.

### איפה האפליקציה (להרחבה)

ההרחבה מדברת עם האפליקציה ב-`http://127.0.0.1:8766` — **נתיב ל-exe לא משנה**; חשוב שהאפליקציה רצה (או עלתה דרך `yvp://`).

אם התקנת עם **מתקין**:

| מערכת | תיקיית אפליקציה | תיקייה ל-Load unpacked |
|-------|-----------------|------------------------|
| **Windows** | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| **Linux** | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

ב-Linux עם `XDG_DATA_HOME` — `$XDG_DATA_HOME/yvp-clipper/` במקום `~/.local/share`.

**בלי מתקין (portable + ארכיון הרחבה):** שים את האפליקציה וההרחבה המפורקת בכל מקום → הפעל אפליקציה → Load unpacked על תיקייה עם `manifest.json`. `yvp://` לא רשום — בפעם הראשונה צריך להפעיל את האפליקציה ידנית (או להשאיר פתוחה).

</div>

</details>

<details>
<summary>हिन्दी</summary>

| ज़रूरत | Windows | Linux |
|--------|---------|-------|
| **सिर्फ app** | portable `.exe` | portable binary |
| **App + एक्सटेंशन** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |
| **सिर्फ एक्सटेंशन** | `YVPClipper-extension.zip` | `YVPClipper-extension.tar.gz` |

**इंस्टॉलर** के बाद: app एक बार चलाओ — Load unpacked के लिए `extension` फोल्डर का पाथ दिखाएगा (UI भाषा में)।

एक्सटेंशन **अपने आप नहीं लगता** — Chrome/Opera अनुमति नहीं देते। सिर्फ मैन्युअल: Developer mode → Load unpacked → टिप वाला फोल्डर।

### ऐप कहाँ है (एक्सटेंशन के लिए)

एक्सटेंशन desktop app से `http://127.0.0.1:8766` पर बात करता है — **exe का पाथ मायने नहीं रखता**; app चलना चाहिए (या `yvp://` से उठे)।

अगर **इंस्टॉलर** लगाया:

| OS | ऐप डायरेक्टरी | Load unpacked फोल्डर |
|----|---------------|----------------------|
| **Windows** | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| **Linux** | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

Linux पर `XDG_DATA_HOME` सेट हो तो `~/.local/share` की जगह `$XDG_DATA_HOME/yvp-clipper/`।

**बिना इंस्टॉलर (portable + एक्सटेंशन आर्काइव):** app और अनपैक्ड एक्सटेंशन कहीं भी रखो → app चलाओ → `manifest.json` वाले फोल्डर पर Load unpacked। `yvp://` रजिस्टर नहीं — पहली बार app खुद चालू करो (या खुला रखो)।

</details>

<details>
<summary>Oʻzbekcha</summary>

| Kerak | Windows | Linux |
|-------|---------|-------|
| **Faqat app** | portable `.exe` | portable binary |
| **App + kengaytma** | `YVPClipper-Setup.exe` | `YVPClipper-linux-installer.tar.gz` |
| **Faqat kengaytma** | `YVPClipper-extension.zip` | `YVPClipper-extension.tar.gz` |

**O‘rnatuvchidan** keyin: appni bir marta ishga tushiring — Load unpacked uchun `extension` papkasi yo‘lini ko‘rsatadi (interfeys tilida).

Kengaytma **avtomatik o‘rnatilmaydi** — Chrome/Opera ruxsat bermaydi. Faqat qo‘lda: Developer mode → Load unpacked → maslahatdagi papka.

### Ilova qayerda (kengaytma uchun)

Kengaytma desktop app bilan `http://127.0.0.1:8766` orqali gaplashadi — **exe yo‘li muhim emas**; app ishlashi kerak (yoki `yvp://` orqali ko‘tariladi).

Agar **o‘rnatuvchi** ishlatgan bo‘lsangiz:

| OS | Ilova katalogi | Load unpacked papkasi |
|----|----------------|------------------------|
| **Windows** | `%LOCALAPPDATA%\YVPClipper\` | `%LOCALAPPDATA%\YVPClipper\extension\` |
| **Linux** | `~/.local/share/yvp-clipper/` | `~/.local/share/yvp-clipper/extension/` |

Linuxda `XDG_DATA_HOME` berilgan bo‘lsa — `~/.local/share` o‘rniga `$XDG_DATA_HOME/yvp-clipper/`.

**O‘rnatuvchisiz (portable + kengaytma arxivi):** app va ochilgan kengaytmani istalgan joyga qo‘ying → appni ishga tushiring → `manifest.json` bo‘lgan papkaga Load unpacked. `yvp://` ro‘yxatdan o‘tmagan — birinchi marta appni o‘zingiz oching (yoki ochiq tuting).

</details>

---

## Ручная установка (без Setup / install.sh)

<details open>
<summary>Русский</summary>

1. Скачай **portable app** + **`YVPClipper-extension.zip`** (Windows) или **`.tar.gz`** (Linux).
2. Распакуй архив расширения — внутри папка `YVPClipper-extension/` с `manifest.json`.
3. Запусти portable app (двойной клик / `./YOUTUBE\ VIDEOS\ ...`).
4. `chrome://extensions` → режим разработчика → **Load unpacked** → выбери распакованную папку.

</details>

<details>
<summary>English</summary>

1. Download **portable app** + **`YVPClipper-extension.zip`** (Windows) or **`.tar.gz`** (Linux).
2. Unpack the extension archive — inside is `YVPClipper-extension/` with `manifest.json`.
3. Start the portable app (double-click / `./YOUTUBE\ VIDEOS\ ...`).
4. `chrome://extensions` → Developer mode → **Load unpacked** → pick the unpacked folder.

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

1. הורד **portable app** + **`YVPClipper-extension.zip`** (Windows) או **`.tar.gz`** (Linux).
2. פרק את ארכיון ההרחבה — בפנים `YVPClipper-extension/` עם `manifest.json`.
3. הפעל את ה-portable app (לחיצה כפולה / `./YOUTUBE\ VIDEOS\ ...`).
4. `chrome://extensions` → מצב מפתח → **Load unpacked** → בחר את התיקייה המפורקת.

</div>

</details>

<details>
<summary>हिन्दी</summary>

1. **portable app** + **`YVPClipper-extension.zip`** (Windows) या **`.tar.gz`** (Linux) डाउनलोड करो।
2. एक्सटेंशन आर्काइव अनपैक करो — अंदर `YVPClipper-extension/` और `manifest.json`।
3. portable app चलाओ (डबल क्लिक / `./YOUTUBE\ VIDEOS\ ...`)।
4. `chrome://extensions` → Developer mode → **Load unpacked** → अनपैक्ड फोल्डर चुनो।

</details>

<details>
<summary>Oʻzbekcha</summary>

1. **portable app** + **`YVPClipper-extension.zip`** (Windows) yoki **`.tar.gz`** (Linux) yuklab oling.
2. Kengaytma arxivini oching — ichida `YVPClipper-extension/` va `manifest.json`.
3. Portable appni ishga tushiring (ikki marta bosish / `./YOUTUBE\ VIDEOS\ ...`).
4. `chrome://extensions` → Developer mode → **Load unpacked** → ochilgan papkani tanlang.

</details>

---

## Windows

<details open>
<summary>Русский</summary>

### Только app (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → скачай `.exe` (длинное имя, без Setup) → двойной клик.

### App + расширение

1. `YVPClipper-Setup.exe` → установка (`yvp://`, папка extension)
2. Запусти app → прочитай подсказку про расширение
3. `chrome://extensions` или `opera://extensions` → Load unpacked → папка из подсказки

### Из исходников

```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### Сборка exe + Setup

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

</details>

<details>
<summary>English</summary>

### App only (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → download the `.exe` (long name, not Setup) → double-click.

### App + extension

1. `YVPClipper-Setup.exe` → install (`yvp://`, extension folder)
2. Launch the app → read the extension tip
3. `chrome://extensions` or `opera://extensions` → Load unpacked → folder from the tip

### From source

```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### Build exe + Setup

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

### רק אפליקציה (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → הורד `.exe` (שם ארוך, בלי Setup) → לחיצה כפולה.

### אפליקציה + הרחבה

1. `YVPClipper-Setup.exe` → התקנה (`yvp://`, תיקיית extension)
2. הפעל אפליקציה → קרא את הטיפ על ההרחבה
3. `chrome://extensions` או `opera://extensions` → Load unpacked → התיקייה מהטיפ

### מקוד מקור

```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### בניית exe + Setup

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

</div>

</details>

<details>
<summary>हिन्दी</summary>

### सिर्फ app (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → `.exe` डाउनलोड (लंबा नाम, Setup नहीं) → डबल क्लिक।

### App + एक्सटेंशन

1. `YVPClipper-Setup.exe` → इंस्टॉल (`yvp://`, extension फोल्डर)
2. app चलाओ → एक्सटेंशन की टिप पढ़ो
3. `chrome://extensions` या `opera://extensions` → Load unpacked → टिप वाला फोल्डर

### सोर्स से

```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### exe + Setup बिल्ड

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

</details>

<details>
<summary>Oʻzbekcha</summary>

### Faqat app (portable)

[Releases](https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases) → `.exe` yuklab oling (uzun nom, Setup emas) → ikki marta bosing.

### App + kengaytma

1. `YVPClipper-Setup.exe` → o‘rnatish (`yvp://`, extension papkasi)
2. Appni ishga tushiring → kengaytma maslahatini o‘qing
3. `chrome://extensions` yoki `opera://extensions` → Load unpacked → maslahatdagi papka

### Manbadan

```bat
py -m pip install -r src/requirements.txt -r windows/requirements.txt
py src\main.py
```

### exe + Setup yig‘ish

```bat
py scripts\sync_extension_manifest.py
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
iscc windows\installer.iss
```

</details>

---

## Linux

<details open>
<summary>Русский</summary>

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

</details>

<details>
<summary>English</summary>

**Dependency:** `ffmpeg` on PATH.

### App only (portable)

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### App + extension

```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
yvp-clipper   # or yvp://start
```

Then Load unpacked, same as Windows.

### From source

```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

**תלות:** `ffmpeg` ב-PATH.

### רק אפליקציה (portable)

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### אפליקציה + הרחבה

```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
yvp-clipper   # או yvp://start
```

אחר כך Load unpacked כמו ב-Windows.

### מקוד מקור

```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

</div>

</details>

<details>
<summary>हिन्दी</summary>

**डिпенडेंसी:** PATH में `ffmpeg`।

### सिर्फ app (portable)

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### App + एक्सटेंशन

```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
yvp-clipper   # या yvp://start
```

फिर Load unpacked — Windows जैसा।

### सोर्स से

```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

</details>

<details>
<summary>Oʻzbekcha</summary>

**Bog‘liqlik:** PATH da `ffmpeg`.

### Faqat app (portable)

```bash
gh release download --repo NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV --pattern "*" --dir .
chmod +x YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

### App + kengaytma

```bash
tar xzf YVPClipper-linux-installer.tar.gz
./install.sh
yvp-clipper   # yoki yvp://start
```

Keyin Load unpacked — Windows dagi kabi.

### Manbadan

```bash
chmod +x linux/run.sh linux/build-installer.sh
./linux/build-installer.sh
```

</details>

---

## Возможности

<details open>
<summary>Русский</summary>

- Desktop GUI или расширение на YouTube (через bridge `127.0.0.1:8766`)
- `yvp://` — авто-запуск app из расширения, трей, закрытие после клипа
- **Языки:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- Иконка — флаг Узбекистана 🇺🇿

</details>

<details>
<summary>English</summary>

- Desktop GUI or YouTube extension (via bridge `127.0.0.1:8766`)
- `yvp://` — auto-start app from the extension, tray, close after clip
- **Languages:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- Icon — Uzbekistan flag 🇺🇿

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

- Desktop GUI או הרחבה ב-YouTube (דרך bridge `127.0.0.1:8766`)
- `yvp://` — הפעלה אוטומטית מההרחבה, מגש, סגירה אחרי קליפ
- **שפות:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- אייקון — דגל אוזבקיסטן 🇺🇿

</div>

</details>

<details>
<summary>हिन्दी</summary>

- Desktop GUI या YouTube एक्सटेंशन (bridge `127.0.0.1:8766`)
- `yvp://` — एक्सटेंशन से auto-start, tray, क्लिप के बाद बंद
- **भाषाएँ:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- आइकन — उज़्बेकिस्तान का झंडा 🇺🇿

</details>

<details>
<summary>Oʻzbekcha</summary>

- Desktop GUI yoki YouTube kengaytmasi (bridge `127.0.0.1:8766`)
- `yvp://` — kengaytmadan auto-start, tray, klipdan keyin yopilish
- **Tillar:** Русский, English, עברית, हिन्दी, Oʻzbekcha
- Ikona — Oʻzbekiston bayrogʻi 🇺🇿

</details>

---

## Документация

<details open>
<summary>Русский</summary>

- Подробная инструкция: [docs/INSTRUCTIONS.md](docs/INSTRUCTIONS.md)
- Расширение: [extension/README.md](extension/README.md)

</details>

<details>
<summary>English</summary>

- Full guide: [docs/INSTRUCTIONS.en.md](docs/INSTRUCTIONS.en.md)
- Extension: [extension/README.md](extension/README.md)

</details>

<details>
<summary>עברית</summary>

<div dir="rtl">

- מדריך מלא: [docs/INSTRUCTIONS.he.md](docs/INSTRUCTIONS.he.md)
- הרחבה: [extension/README.md](extension/README.md)

</div>

</details>

<details>
<summary>हिन्दी</summary>

- पूरी गाइड: [docs/INSTRUCTIONS.hi.md](docs/INSTRUCTIONS.hi.md)
- एक्सटेंशन: [extension/README.md](extension/README.md)

</details>

<details>
<summary>Oʻzbekcha</summary>

- Toʻliq qoʻllanma: [docs/INSTRUCTIONS.uz.md](docs/INSTRUCTIONS.uz.md)
- Kengaytma: [extension/README.md](extension/README.md)

</details>

---

## Стек

<details open>
<summary>Русский</summary>

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3

</details>

<details>
<summary>English</summary>

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3

</details>

<details>
<summary>עברית</summary>

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3

</details>

<details>
<summary>हिन्दी</summary>

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3

</details>

<details>
<summary>Oʻzbekcha</summary>

Python · CustomTkinter · yt-dlp · ffmpeg · Chromium MV3

</details>
