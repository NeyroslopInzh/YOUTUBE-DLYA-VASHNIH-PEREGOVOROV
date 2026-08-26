"""GUI for cutting YouTube video segments."""

from __future__ import annotations

import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app_log import get_log_file, logger, setup_logging
from app_name import APP_NAME
from clipper import ClipRequest, ClipperError, download_clip
from keyboard import bind_layout_safe_shortcuts, is_layout_safe_ctrl
from paths import default_output_dir, ensure_output_dir
from settings import FormSettings, load_settings, save_settings


class ClipperApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry("720x560")
        self.minsize(640, 480)

        self._log_queue: queue.Queue[str | tuple[str, str]] = queue.Queue()
        self._worker: threading.Thread | None = None

        saved = load_settings()

        self._build_ui(saved)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_log)

    def _build_ui(self, saved: FormSettings) -> None:
        pad = {"padx": 16, "pady": (0, 10)}

        header = ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=680,
            justify="center",
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
        self.dir_var = tk.StringVar(value=saved.output_dir or str(default_output_dir()))

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
            text="Копировать лог",
            width=110,
            command=self._copy_log,
        ).pack(side="left", padx=(8, 0))

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

        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._setup_log_interactions()
        bind_layout_safe_shortcuts(
            self,
            log_widget=self.log_box._textbox,
            on_copy_log=self._copy_log,
            on_select_all_log=lambda: self._select_all_log(None),
        )

    def _setup_log_interactions(self) -> None:
        text = self.log_box._textbox
        text.configure(exportselection=True)

        self._log_menu = tk.Menu(self, tearoff=0)
        self._log_menu.add_command(label="Копировать", command=self._copy_log)
        self._log_menu.add_command(label="Выделить всё", command=lambda: self._select_all_log(None))

        text.bind("<Key>", self._on_log_key)
        text.bind("<Button-3>", self._show_log_menu)

    def _on_log_key(self, event: tk.Event) -> str | None:
        if is_layout_safe_ctrl(event):
            return None
        if event.keysym in {
            "Shift_L",
            "Shift_R",
            "Control_L",
            "Control_R",
            "Alt_L",
            "Alt_R",
            "Left",
            "Right",
            "Up",
            "Down",
            "Home",
            "End",
            "Prior",
            "Next",
            "Tab",
        }:
            return None
        return "break"

    def _show_log_menu(self, event: tk.Event) -> None:
        try:
            self._log_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._log_menu.grab_release()

    def _select_all_log(self, _event: tk.Event | None = None) -> None:
        text = self.log_box._textbox
        text.tag_add("sel", "1.0", "end-1c")
        text.mark_set("insert", "end-1c")
        text.see("insert")
        return "break"

    def _copy_log(self) -> None:
        text = self.log_box._textbox
        try:
            selection = text.get("sel.first", "sel.last")
        except tk.TclError:
            selection = text.get("1.0", "end-1c")
        if not selection.strip():
            return
        self.clipboard_clear()
        self.clipboard_append(selection)
        self.update()

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
        current = self.dir_var.get().strip()
        initial = current if current and Path(current).expanduser().is_dir() else str(default_output_dir().parent)
        path = filedialog.askdirectory(initialdir=initial)
        if path:
            self.dir_var.set(str(ensure_output_dir(path)))

    def _open_logs(self) -> None:
        log_file = get_log_file()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        if not log_file.exists():
            log_file.touch()
        if sys.platform == "win32":
            subprocess.Popen(["explorer", "/select,", str(log_file)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", str(log_file)])
        else:
            subprocess.Popen(["xdg-open", str(log_file.parent)])

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
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

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
                        messagebox.showinfo(APP_NAME, msg)
                elif kind == "error":
                    self._set_busy(False)
                    messagebox.showerror(APP_NAME, msg)
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

        try:
            output_dir = ensure_output_dir(self.dir_var.get())
            self.dir_var.set(str(output_dir))
        except OSError as exc:
            self._set_busy(False)
            messagebox.showerror(APP_NAME, f"Не удалось создать папку сохранения:\n{exc}")
            return

        request = ClipRequest(
            url=self.url_var.get(),
            start=self.start_var.get(),
            end=self.end_var.get(),
            title=self.title_var.get(),
            output_dir=output_dir,
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
