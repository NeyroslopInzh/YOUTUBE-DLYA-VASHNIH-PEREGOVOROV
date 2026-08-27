"""Переводы интерфейса и сообщений об ошибках."""

from __future__ import annotations

from typing import Any

# Порядок: ru, en, he, hi, uz
LANGUAGES: list[tuple[str, str]] = [
    ("ru", "Русский"),
    ("en", "English"),
    ("he", "עברית"),
    ("hi", "हिन्दी"),
    ("uz", "Oʻzbekcha"),
]

# Флаги для кнопок языка (emoji)
LANGUAGE_FLAGS: list[tuple[str, str]] = [
    ("ru", "🇷🇺"),
    ("en", "🇺🇸"),
    ("he", "🇮🇱"),
    ("hi", "🇮🇳"),
    ("uz", "🇺🇿"),
]

DEFAULT_LANG = "ru"

STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "ui.hint": "Время: MM:SS.mmm, HH:MM:SS.mmm или секунды (дробь ок). Качается только нужный кусок.",
        "ui.label_url": "Ссылка YouTube",
        "ui.label_start": "Начало отрезка",
        "ui.label_end": "Конец отрезка",
        "ui.label_title": "Название файла",
        "ui.label_output_dir": "Папка сохранения",
        "ui.label_language": "Язык",
        "ui.ph_url": "https://www.youtube.com/watch?v=...",
        "ui.ph_start": "1:30.250 или 90.5",
        "ui.ph_end": "3:45.750 или 225.5",
        "ui.ph_title": "мой_клип",
        "ui.btn_browse": "Обзор…",
        "ui.btn_download": "Скачать отрезок",
        "ui.btn_copy_log": "Копировать лог",
        "ui.btn_logs": "Логи",
        "ui.status_ready": "Готов",
        "ui.status_downloading": "Загрузка…",
        "ui.status_done": "Готово",
        "ui.status_error": "Ошибка",
        "ui.log_title": "Лог",
        "ui.log_expand": "▶ Лог",
        "ui.log_collapse": "▼ Лог",
        "ui.menu_copy": "Копировать",
        "ui.menu_select_all": "Выделить всё",
        "ui.msg_saved": "Сохранено:\n{path}",
        "ui.msg_unexpected": "Неожиданная ошибка:\n{error}",
        "ui.msg_output_dir_fail": "Не удалось создать папку сохранения:\n{error}",
        "err.empty_url": "Ссылка на YouTube не указана",
        "err.not_youtube": "Нужна ссылка на YouTube",
        "err.time_empty": "Время не указано",
        "err.time_invalid": "Неверный формат времени: {value!r} (MM:SS.mmm, HH:MM:SS.mmm или секунды)",
        "err.end_before_start": "Время окончания должно быть позже времени начала",
        "err.title_empty": "Название файла пустое",
        "err.file_exists": "Файл уже существует: {path}",
        "err.file_not_found": "Файл не найден после загрузки",
        "err.output_dir": "Не удалось создать папку сохранения: {path}\n{error}",
        "err.ffmpeg_missing_linux": "ffmpeg не найден в PATH. Установи: sudo pacman -S ffmpeg (Arch) или apt install ffmpeg",
        "err.ffmpeg_missing_win": "ffmpeg не найден. Переустанови приложение или добавь ffmpeg в PATH.",
        "err.ffmpeg_segfault": "ffmpeg упал (segfault, код -11). На Linux: sudo pacman -S ffmpeg и перезапуск.",
        "err.openssl_mismatch": "Конфликт OpenSSL (libcrypto). Обнови приложение до последней версии — в ней yt-dlp встроен в бинарник.",
        "err.winerror_10054": "YouTube оборвал соединение (WinError 10054). Повтор через минуту, VPN или другая сеть.",
        "err.api_page": "Не удалось получить данные видео с YouTube. Проверь интернет/VPN.",
        "err.bot_check": "YouTube просит проверку. Попробуй VPN или другую сеть.",
        "err.ytdlp_code": "yt-dlp завершился с кодом {code}.\n{tail}",
        "clip.downloading": "Скачиваю отрезок {start} — {end}",
        "clip.saving": "Сохраняю в: {path}",
        "clip.retry": "Повтор {attempt}/{total} через {wait} сек...",
        "clip.done": "Готово!",
        "welcome.title": "Установка завершена",
        "welcome.body": "Приложение готово к работе.",
        "welcome.extension_hint": "Если хотите качать отрезки через расширение браузера — установите его вручную (Load unpacked / загрузить распакованное).",
        "welcome.extension_path": "Папка расширения:\n{path}",
        "welcome.extension_steps": "Chrome / Opera / Edge: Режим разработчика → Загрузить распакованное → выберите эту папку.",
        "welcome.ok": "Понятно",
    },
    "en": {
        "ui.hint": "Time: MM:SS.mmm, HH:MM:SS.mmm or seconds (fractional OK). Only the selected segment is downloaded.",
        "ui.label_url": "YouTube link",
        "ui.label_start": "Start time",
        "ui.label_end": "End time",
        "ui.label_title": "File name",
        "ui.label_output_dir": "Save folder",
        "ui.label_language": "Language",
        "ui.ph_url": "https://www.youtube.com/watch?v=...",
        "ui.ph_start": "1:30.250 or 90.5",
        "ui.ph_end": "3:45.750 or 225.5",
        "ui.ph_title": "my_clip",
        "ui.btn_browse": "Browse…",
        "ui.btn_download": "Download clip",
        "ui.btn_copy_log": "Copy log",
        "ui.btn_logs": "Logs",
        "ui.status_ready": "Ready",
        "ui.status_downloading": "Downloading…",
        "ui.status_done": "Done",
        "ui.status_error": "Error",
        "ui.log_title": "Log",
        "ui.log_expand": "▶ Log",
        "ui.log_collapse": "▼ Log",
        "ui.menu_copy": "Copy",
        "ui.menu_select_all": "Select all",
        "ui.msg_saved": "Saved:\n{path}",
        "ui.msg_unexpected": "Unexpected error:\n{error}",
        "ui.msg_output_dir_fail": "Could not create output folder:\n{error}",
        "err.empty_url": "YouTube URL is required",
        "err.not_youtube": "A valid YouTube URL is required",
        "err.time_empty": "Time is required",
        "err.time_invalid": "Invalid time format: {value!r} (MM:SS.mmm, HH:MM:SS.mmm or seconds)",
        "err.end_before_start": "End time must be after start time",
        "err.title_empty": "File name is empty",
        "err.file_exists": "File already exists: {path}",
        "err.file_not_found": "Output file not found after download",
        "err.output_dir": "Could not create folder: {path}\n{error}",
        "err.ffmpeg_missing_linux": "ffmpeg not found in PATH. Install: sudo pacman -S ffmpeg or apt install ffmpeg",
        "err.ffmpeg_missing_win": "ffmpeg not found. Reinstall the app or add ffmpeg to PATH.",
        "err.ffmpeg_segfault": "ffmpeg crashed (segfault, code -11). On Linux install system ffmpeg and restart.",
        "err.openssl_mismatch": "OpenSSL conflict (libcrypto). Update to the latest app build — yt-dlp is bundled inside.",
        "err.winerror_10054": "YouTube closed the connection (WinError 10054). Retry, VPN or another network.",
        "err.api_page": "Could not fetch video data from YouTube. Check internet/VPN.",
        "err.bot_check": "YouTube wants verification. Try VPN or another network.",
        "err.ytdlp_code": "yt-dlp exited with code {code}.\n{tail}",
        "clip.downloading": "Downloading {start} — {end}",
        "clip.saving": "Saving to: {path}",
        "clip.retry": "Retry {attempt}/{total} in {wait} sec...",
        "clip.done": "Done!",
        "welcome.title": "Setup complete",
        "welcome.body": "The app is ready to use.",
        "welcome.extension_hint": "To download clips from the browser extension, install it manually (Load unpacked).",
        "welcome.extension_path": "Extension folder:\n{path}",
        "welcome.extension_steps": "Chrome / Opera / Edge: Developer mode → Load unpacked → select this folder.",
        "welcome.ok": "OK",
    },
    "he": {
        "ui.hint": "זמן: MM:SS.mmm, HH:MM:SS.mmm או שניות (שבר OK). מוריד רק את הקטע שנבחר.",
        "ui.label_url": "קישור YouTube",
        "ui.label_start": "תחילת קטע",
        "ui.label_end": "סוף קטע",
        "ui.label_title": "שם קובץ",
        "ui.label_output_dir": "תיקיית שמירה",
        "ui.label_language": "שפה",
        "ui.ph_url": "https://www.youtube.com/watch?v=...",
        "ui.ph_start": "1:30.250 או 90.5",
        "ui.ph_end": "3:45.750 או 225.5",
        "ui.ph_title": "הקליפ_שלי",
        "ui.btn_browse": "עיון…",
        "ui.btn_download": "הורד קטע",
        "ui.btn_copy_log": "העתק לוג",
        "ui.btn_logs": "לוגים",
        "ui.status_ready": "מוכן",
        "ui.status_downloading": "מוריד…",
        "ui.status_done": "הושלם",
        "ui.status_error": "שגיאה",
        "ui.log_title": "לוג",
        "ui.log_expand": "▶ לוג",
        "ui.log_collapse": "▼ לוג",
        "ui.menu_copy": "העתק",
        "ui.menu_select_all": "בחר הכל",
        "ui.msg_saved": "נשמר:\n{path}",
        "ui.msg_unexpected": "שגיאה בלתי צפויה:\n{error}",
        "ui.msg_output_dir_fail": "לא ניתן ליצור תיקייה:\n{error}",
        "err.empty_url": "נדרש קישור YouTube",
        "err.not_youtube": "נדרש קישור YouTube תקין",
        "err.time_empty": "לא צוין זמן",
        "err.time_invalid": "פורמט זמן לא תקין: {value!r} (MM:SS.mmm, HH:MM:SS.mmm או שניות)",
        "err.end_before_start": "זמן הסיום חייב להיות אחרי זמן ההתחלה",
        "err.title_empty": "שם הקובץ ריק",
        "err.file_exists": "הקובץ כבר קיים: {path}",
        "err.file_not_found": "הקובץ לא נמצא אחרי ההורדה",
        "err.output_dir": "לא ניתן ליצור תיקייה: {path}\n{error}",
        "err.ffmpeg_missing_linux": "ffmpeg לא נמצא. התקן: sudo pacman -S ffmpeg או apt install ffmpeg",
        "err.ffmpeg_missing_win": "ffmpeg לא נמצא. התקן מחדש או הוסף ffmpeg ל-PATH.",
        "err.ffmpeg_segfault": "ffmpeg קרס (segfault). התקן ffmpeg מערכת והפעל מחדש.",
        "err.openssl_mismatch": "התנגשות OpenSSL (libcrypto). עדכן לגרסה האחרונה — yt-dlp מובנה בבינארי.",
        "err.winerror_10054": "YouTube ניתק את החיבור. נסה שוב, VPN או רשת אחרת.",
        "err.api_page": "לא ניתן לקבל נתוני וידאו מ-YouTube. בדוק אינטרנט/VPN.",
        "err.bot_check": "YouTube דורש אימות. נסה VPN או רשת אחרת.",
        "err.ytdlp_code": "yt-dlp הסתיים עם קוד {code}.\n{tail}",
        "clip.downloading": "מוריד {start} — {end}",
        "clip.saving": "שומר ב: {path}",
        "clip.retry": "ניסיון {attempt}/{total} בעוד {wait} שניות...",
        "clip.done": "הושלם!",
        "welcome.title": "ההתקנה הושלמה",
        "welcome.body": "היישום מוכן לשימוש.",
        "welcome.extension_hint": "להורדה דרך תוסף הדפדפן — התקן ידנית (Load unpacked).",
        "welcome.extension_path": "תיקיית התוסף:\n{path}",
        "welcome.extension_steps": "Chrome / Opera / Edge: מצב מפתח → Load unpacked → בחר תיקייה זו.",
        "welcome.ok": "הבנתי",
    },
    "hi": {
        "ui.hint": "समय: MM:SS.mmm, HH:MM:SS.mmm या सेकंड (दशमलव OK)। केवल चुना हुआ हिस्सा डाउनलोड होता है।",
        "ui.label_url": "YouTube लिंक",
        "ui.label_start": "शुरुआत",
        "ui.label_end": "अंत",
        "ui.label_title": "फ़ाइल नाम",
        "ui.label_output_dir": "सेव फ़ोल्डर",
        "ui.label_language": "भाषा",
        "ui.ph_url": "https://www.youtube.com/watch?v=...",
        "ui.ph_start": "1:30.250 या 90.5",
        "ui.ph_end": "3:45.750 या 225.5",
        "ui.ph_title": "mera_clip",
        "ui.btn_browse": "ब्राउज़…",
        "ui.btn_download": "क्लिप डाउनलोड",
        "ui.btn_copy_log": "लॉग कॉपी",
        "ui.btn_logs": "लॉग",
        "ui.status_ready": "तैयार",
        "ui.status_downloading": "डाउनलोड…",
        "ui.status_done": "हो गया",
        "ui.status_error": "त्रुटि",
        "ui.log_title": "लॉग",
        "ui.log_expand": "▶ लॉग",
        "ui.log_collapse": "▼ लॉग",
        "ui.menu_copy": "कॉपी",
        "ui.menu_select_all": "सब चुनें",
        "ui.msg_saved": "सेव:\n{path}",
        "ui.msg_unexpected": "अप्रत्याशित त्रुटि:\n{error}",
        "ui.msg_output_dir_fail": "फ़ोल्डर नहीं बना:\n{error}",
        "err.empty_url": "YouTube लिंक आवश्यक है",
        "err.not_youtube": "मान्य YouTube लिंक आवश्यक है",
        "err.time_empty": "समय नहीं दिया",
        "err.time_invalid": "गलत समय प्रारूप: {value!r} (MM:SS.mmm, HH:MM:SS.mmm या सेकंड)",
        "err.end_before_start": "अंत, शुरुआत के बाद होना चाहिए",
        "err.title_empty": "फ़ाइल नाम खाली है",
        "err.file_exists": "फ़ाइल पहले से है: {path}",
        "err.file_not_found": "डाउनलोड के बाद फ़ाइल नहीं मिली",
        "err.output_dir": "फ़ोल्डर नहीं बना: {path}\n{error}",
        "err.ffmpeg_missing_linux": "ffmpeg नहीं मिला। sudo pacman -S ffmpeg या apt install ffmpeg",
        "err.ffmpeg_missing_win": "ffmpeg नहीं मिला। ऐप दोबारा इंस्टॉल करें।",
        "err.ffmpeg_segfault": "ffmpeg crash (segfault)। Linux पर system ffmpeg इंस्टॉल करें।",
        "err.openssl_mismatch": "OpenSSL conflict (libcrypto)। नवीनतम build अपडेट करें — yt-dlp बंडल में है।",
        "err.winerror_10054": "YouTube ने कनेक्शन तोड़ दिया। दोबारा, VPN या दूसरा नेटवर्क।",
        "err.api_page": "YouTube से डेटा नहीं मिला। इंटरनेट/VPN जाँचें।",
        "err.bot_check": "YouTube सत्यापन माँगता है। VPN आज़माएँ।",
        "err.ytdlp_code": "yt-dlp कोड {code} पर बंद।\n{tail}",
        "clip.downloading": "डाउनलोड {start} — {end}",
        "clip.saving": "सेव: {path}",
        "clip.retry": "पुनः {attempt}/{total}, {wait} सेकंड...",
        "clip.done": "हो गया!",
        "welcome.title": "इंस्टॉल पूरा",
        "welcome.body": "ऐप उपयोग के लिए तैयार है।",
        "welcome.extension_hint": "ब्राउज़र एक्सटेंशन से क्लिप डाउनलोड करने के लिए — मैन्युअल इंस्टॉल करें (Load unpacked)।",
        "welcome.extension_path": "एक्सटेंशन फ़ोल्डर:\n{path}",
        "welcome.extension_steps": "Chrome / Opera / Edge: Developer mode → Load unpacked → यह फ़ोल्डर चुनें।",
        "welcome.ok": "ठीक है",
    },
    "uz": {
        "ui.hint": "Vaqt: MM:SS.mmm, HH:MM:SS.mmm yoki soniyalar (kasr OK). Faqat tanlangan qism yuklanadi.",
        "ui.label_url": "YouTube havolasi",
        "ui.label_start": "Boshlanish",
        "ui.label_end": "Tugash",
        "ui.label_title": "Fayl nomi",
        "ui.label_output_dir": "Saqlash papkasi",
        "ui.label_language": "Til",
        "ui.ph_url": "https://www.youtube.com/watch?v=...",
        "ui.ph_start": "1:30.250 yoki 90.5",
        "ui.ph_end": "3:45.750 yoki 225.5",
        "ui.ph_title": "mening_klip",
        "ui.btn_browse": "Tanlash…",
        "ui.btn_download": "Qismni yuklash",
        "ui.btn_copy_log": "Logni nusxalash",
        "ui.btn_logs": "Loglar",
        "ui.status_ready": "Tayyor",
        "ui.status_downloading": "Yuklanmoqda…",
        "ui.status_done": "Tayyor",
        "ui.status_error": "Xato",
        "ui.log_title": "Log",
        "ui.log_expand": "▶ Log",
        "ui.log_collapse": "▼ Log",
        "ui.menu_copy": "Nusxalash",
        "ui.menu_select_all": "Hammasini tanlash",
        "ui.msg_saved": "Saqlandi:\n{path}",
        "ui.msg_unexpected": "Kutilmagan xato:\n{error}",
        "ui.msg_output_dir_fail": "Papka yaratilmadi:\n{error}",
        "err.empty_url": "YouTube havolasi kerak",
        "err.not_youtube": "Toʻgʻri YouTube havolasi kerak",
        "err.time_empty": "Vaqt kiritilmagan",
        "err.time_invalid": "Notoʻgʻri vaqt: {value!r} (MM:SS.mmm, HH:MM:SS.mmm yoki soniyalar)",
        "err.end_before_start": "Tugash vaqti boshlanishdan keyin boʻlishi kerak",
        "err.title_empty": "Fayl nomi boʻsh",
        "err.file_exists": "Fayl allaqachon bor: {path}",
        "err.file_not_found": "Yuklashdan keyin fayl topilmadi",
        "err.output_dir": "Papka yaratilmadi: {path}\n{error}",
        "err.ffmpeg_missing_linux": "ffmpeg topilmadi. Oʻrnating: sudo pacman -S ffmpeg yoki apt install ffmpeg",
        "err.ffmpeg_missing_win": "ffmpeg topilmadi. Ilovani qayta oʻrnating.",
        "err.ffmpeg_segfault": "ffmpeg ishdan chiqdi (segfault). Linuxda tizim ffmpeg oʻrnating.",
        "err.openssl_mismatch": "OpenSSL ziddiyati (libcrypto). Soʻnggi build ga yangilang — yt-dlp ichkarida.",
        "err.winerror_10054": "YouTube ulanishni uzdi. Qayta urining, VPN yoki boshqa tarmoq.",
        "err.api_page": "YouTube dan maʼlumot olinmadi. Internet/VPN ni tekshiring.",
        "err.bot_check": "YouTube tekshiruv soʻrayapti. VPN sinab koʻring.",
        "err.ytdlp_code": "yt-dlp {code} kod bilan tugadi.\n{tail}",
        "clip.downloading": "Yuklanmoqda {start} — {end}",
        "clip.saving": "Saqlash: {path}",
        "clip.retry": "Qayta {attempt}/{total}, {wait} soniya...",
        "clip.done": "Tayyor!",
        "welcome.title": "O'rnatish tugadi",
        "welcome.body": "Ilova ishlatishga tayyor.",
        "welcome.extension_hint": "Brauzer kengaytmasi orqali yuklash uchun — qo'lda o'rnating (Load unpacked).",
        "welcome.extension_path": "Kengaytma papkasi:\n{path}",
        "welcome.extension_steps": "Chrome / Opera / Edge: Dasturchi rejimi → Load unpacked → shu papkani tanlang.",
        "welcome.ok": "Tushunarli",
    },
}

# Fix Hebrew typo קrashed -> crashed in translation
STRINGS["he"]["err.ffmpeg_segfault"] = "ffmpeg קרס (segfault). התקן ffmpeg מערכת והפעל מחדש."


class I18n:
    def __init__(self, lang: str = DEFAULT_LANG) -> None:
        self.lang = lang if lang in STRINGS else DEFAULT_LANG

    def t(self, key: str, **kwargs: Any) -> str:
        text = STRINGS.get(self.lang, STRINGS[DEFAULT_LANG]).get(key)
        if text is None:
            text = STRINGS[DEFAULT_LANG].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def language_label(self) -> str:
        for code, label in LANGUAGES:
            if code == self.lang:
                return label
        return LANGUAGES[0][1]


_i18n = I18n()


def get_i18n() -> I18n:
    return _i18n


def set_language(lang: str) -> I18n:
    global _i18n
    _i18n = I18n(lang)
    return _i18n


def code_from_label(label: str) -> str:
    for code, name in LANGUAGES:
        if name == label:
            return code
    return DEFAULT_LANG


def label_from_code(code: str) -> str:
    for c, name in LANGUAGES:
        if c == code:
            return name
    return LANGUAGES[0][1]
