"""YouTube Clipper — GUI for cutting YouTube video segments."""

from __future__ import annotations

import queue
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app_log import get_log_file, logger, setup_logging
from clipper import ClipRequest, ClipperError, download_clip
from settings import FormSettings, load_settings, save_settings

APP_TITLE = "YouTube Clipper"
DEFAULT_OUTPUT = Path.home() / "Videos" / "YouTubeClips"


class ClipperApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.geometry("720x560")
        self.minsize(640, 480)

        self._log_queue: queue.Queue[str | tuple[str, str]] = queue.Queue()
        self._worker: threading.Thread | None = None

        saved = load_settings(str(DEFAULT_OUTPUT))

        self._build_ui(saved)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_log)

    def _build_ui(self, saved: FormSettings) -> None:
        pad = {"padx": 16, "pady": (0, 10)}

        header = ctk.CTkLabel(
            self,
            text="Вырезка отрезков с YouTube",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.pack(pady=(16, 4))

        hint = ctk.CTkLabel(
            self,
            text="Время: MM:SS, HH:MM:SS или секунды. Качается только нужный кусок.",
            text_color="gray70",
        )
        hint.pack(pady=(0, 12))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=16, pady=(0, 8))

        self.url_var = tk.StringVar(value=saved.url)
        self.start_var = tk.StringVar(value=saved.start)
        self.end_var = tk.StringVar(value=saved.end)
        self.title_var = tk.StringVar(value=saved.title)
        self.dir_var = tk.StringVar(value=saved.output_dir or str(DEFAULT_OUTPUT))

        self._row(form, "Ссылка YouTube", self.url_var, placeholder="https://www.youtube.com/watch?v=...")
        self._row(form, "Начало отрезка", self.start_var, placeholder="1:30 или 90")
        self._row(form, "Конец отрезка", self.end_var, placeholder="3:45 или 225")
        self._row(form, "Название файла", self.title_var, placeholder="мой_клип")

        dir_row = ctk.CTkFrame(form, fg_color="transparent")
        dir_row.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkLabel(dir_row, text="Папка сохранения", width=140, anchor="w").pack(side="left")
        ctk.CTkEntry(dir_row, textvariable=self.dir_var).pack(side="left", fill="x", expand=True, padx=(8, 8))
        ctk.CTkButton(dir_row, text="Обзор…", width=80, command=self._pick_dir).pack(side="right")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 8))

        self.download_btn = ctk.CTkButton(
            btn_row,
            text="Скачать отрезок",
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_download,
        )
        self.download_btn.pack(side="left")

        ctk.CTkButton(
            btn_row,
            text="Логи",
            width=70,
            command=self._open_logs,
        ).pack(side="left", padx=(8, 0))

        self.status_label = ctk.CTkLabel(btn_row, text="Готов", text_color="gray70")
        self.status_label.pack(side="left", padx=16)

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ctk.CTkLabel(log_frame, text="Лог", anchor="w").pack(fill="x", padx=12, pady=(8, 4))

        self.log_box = ctk.CTkTextbox(log_frame, state="disabled", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _row(
        self,
        parent: ctk.CTkFrame,
        label: str,
        variable: tk.StringVar,
        placeholder: str = "",
    ) -> None:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(10, 0))
        ctk.CTkLabel(row, text=label, width=140, anchor="w").pack(side="left")
        ctk.CTkEntry(row, textvariable=variable, placeholder_text=placeholder).pack(
            side="left", fill="x", expand=True, padx=(8, 0)
        )

    def _pick_dir(self) -> None:
        path = filedialog.askdirectory(initialdir=self.dir_var.get() or str(Path.home()))
        if path:
            self.dir_var.set(path)

    def _open_logs(self) -> None:
        log_file = get_log_file()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        if not log_file.exists():
            log_file.touch()
        subprocess.Popen(["explorer", "/select,", str(log_file)])

    def _collect_settings(self) -> FormSettings:
        return FormSettings(
            url=self.url_var.get().strip(),
            start=self.start_var.get().strip(),
            end=self.end_var.get().strip(),
            title=self.title_var.get().strip(),
            output_dir=self.dir_var.get().strip(),
        )

    def _on_close(self) -> None:
        try:
            save_settings(self._collect_settings())
            logger().info("Настройки сохранены при выходе")
        except OSError as exc:
            logger().error("Не удалось сохранить настройки: %s", exc)
        self.destroy()

    def _append_log(self, text: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _poll_log(self) -> None:
        while True:
            try:
                item = self._log_queue.get_nowait()
            except queue.Empty:
                break

            if isinstance(item, tuple):
                kind, msg = item
                if kind == "status":
                    self.status_label.configure(text=msg)
                elif kind == "done":
                    self._set_busy(False)
                    if msg:
                        messagebox.showinfo(APP_TITLE, msg)
                elif kind == "error":
                    self._set_busy(False)
                    messagebox.showerror(APP_TITLE, msg)
            else:
                self._append_log(item)

        self.after(100, self._poll_log)

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.download_btn.configure(state=state)

    def _on_download(self) -> None:
        if self._worker and self._worker.is_alive():
            return

        self._set_busy(True)
        self._log_queue.put(("status", "Загрузка…"))

        request = ClipRequest(
            url=self.url_var.get(),
            start=self.start_var.get(),
            end=self.end_var.get(),
            title=self.title_var.get(),
            output_dir=Path(self.dir_var.get()),
        )

        def worker() -> None:
            log = setup_logging()
            try:
                def on_log(msg: str) -> None:
                    self._log_queue.put(msg)

                result = download_clip(request, on_log=on_log)
                self._log_queue.put(("done", f"Сохранено:\n{result.output_path}"))
                self._log_queue.put(("status", "Готово"))
            except ClipperError as exc:
                log.exception("ClipperError")
                self._log_queue.put(str(exc))
                self._log_queue.put(("error", str(exc)))
                self._log_queue.put(("status", "Ошибка"))
            except Exception as exc:  # noqa: BLE001
                log.exception("Неожиданная ошибка")
                self._log_queue.put(str(exc))
                self._log_queue.put(("error", f"Неожиданная ошибка:\n{exc}"))
                self._log_queue.put(("status", "Ошибка"))

        self._worker = threading.Thread(target=worker, daemon=True)
        self._worker.start()


def main() -> None:
    setup_logging()
    app = ClipperApp()
    app.mainloop()


if __name__ == "__main__":
    main()
