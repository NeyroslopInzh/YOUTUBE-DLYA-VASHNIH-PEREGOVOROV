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
from bridge_server import start_bridge_server, stop_bridge_server
from clipper import ClipRequest, ClipperError, download_clip
from i18n import LANGUAGES, code_from_label, get_i18n, label_from_code, set_language
from keyboard import bind_layout_safe_shortcuts, is_layout_safe_ctrl
from paths import default_output_dir, ensure_output_dir
from protocol import bridge_already_running, is_protocol_launch
from install_paths import extension_dir, was_installed_via_setup
from settings import FormSettings, load_settings, save_settings
from tray import TrayIcon


class ClipperApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry("720x600")
        self.minsize(640, 500)

        self._log_queue: queue.Queue[str | tuple[str, str]] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._ui_labels: dict[str, ctk.CTkLabel] = {}
        self._entries: dict[str, ctk.CTkEntry] = {}
        self._lang_code = "ru"
        self._extension_session = is_protocol_launch()
        self._force_quit = False
        self._quit_timer: str | None = None
        self._tray: TrayIcon | None = None
        self._bridge_jobs_pending = 0
        self._welcome_dismissed = False

        saved = load_settings()
        set_language(saved.language)
        self._lang_code = saved.language
        self._welcome_dismissed = saved.welcome_dismissed

        self._build_ui(saved)
        self._bridge_port = start_bridge_server(
            self._bridge_output_dir,
            on_job_started=lambda: self.after(0, self._track_bridge_job_started),
            on_job_finished=self._on_bridge_job_finished,
        )
        logger().info("Extension bridge http://127.0.0.1:%s", self._bridge_port)
        if self._extension_session:
            self._enter_extension_background_mode()
        elif was_installed_via_setup() and not self._welcome_dismissed:
            self.after(400, self._show_welcome_dialog)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_log)

    def _bridge_output_dir(self) -> Path:
        try:
            return ensure_output_dir(self.dir_var.get())
        except OSError:
            return ensure_output_dir(default_output_dir())

    def _t(self, key: str, **kwargs: object) -> str:
        return get_i18n().t(key, **kwargs)

    def _build_ui(self, saved: FormSettings) -> None:
        self.header = ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=680,
            justify="center",
        )
        self.header.pack(pady=(16, 4))

        self.hint_label = ctk.CTkLabel(self, text=self._t("ui.hint"), text_color="gray70")
        self.hint_label.pack(pady=(0, 12))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=16, pady=(0, 8))

        lang_row = ctk.CTkFrame(form, fg_color="transparent")
        lang_row.pack(fill="x", padx=12, pady=(10, 0))
        self._ui_labels["ui.label_language"] = ctk.CTkLabel(
            lang_row, text=self._t("ui.label_language"), width=140, anchor="w"
        )
        self._ui_labels["ui.label_language"].pack(side="left")
        self.lang_var = tk.StringVar(value=label_from_code(saved.language))
        self.lang_menu = ctk.CTkOptionMenu(
            lang_row,
            variable=self.lang_var,
            values=[name for _, name in LANGUAGES],
            command=self._on_language_change,
            width=180,
        )
        self.lang_menu.pack(side="left", padx=(8, 0))

        self.url_var = tk.StringVar(value=saved.url)
        self.start_var = tk.StringVar(value=saved.start)
        self.end_var = tk.StringVar(value=saved.end)
        self.title_var = tk.StringVar(value=saved.title)
        self.dir_var = tk.StringVar(value=saved.output_dir or str(default_output_dir()))

        self._row(form, "ui.label_url", self.url_var, "ui.ph_url")
        self._row(form, "ui.label_start", self.start_var, "ui.ph_start")
        self._row(form, "ui.label_end", self.end_var, "ui.ph_end")
        self._row(form, "ui.label_title", self.title_var, "ui.ph_title")

        dir_row = ctk.CTkFrame(form, fg_color="transparent")
        dir_row.pack(fill="x", padx=12, pady=(0, 10))
        self._ui_labels["ui.label_output_dir"] = ctk.CTkLabel(
            dir_row, text=self._t("ui.label_output_dir"), width=140, anchor="w"
        )
        self._ui_labels["ui.label_output_dir"].pack(side="left")
        self._entries["dir"] = ctk.CTkEntry(dir_row, textvariable=self.dir_var)
        self._entries["dir"].pack(side="left", fill="x", expand=True, padx=(8, 8))
        self.browse_btn = ctk.CTkButton(dir_row, text=self._t("ui.btn_browse"), width=80, command=self._pick_dir)
        self.browse_btn.pack(side="right")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 8))

        self.download_btn = ctk.CTkButton(
            btn_row,
            text=self._t("ui.btn_download"),
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_download,
        )
        self.download_btn.pack(side="left")

        self.copy_log_btn = ctk.CTkButton(
            btn_row, text=self._t("ui.btn_copy_log"), width=110, command=self._copy_log
        )
        self.copy_log_btn.pack(side="left", padx=(8, 0))

        self.logs_btn = ctk.CTkButton(
            btn_row, text=self._t("ui.btn_logs"), width=70, command=self._open_logs
        )
        self.logs_btn.pack(side="left", padx=(8, 0))

        self.status_label = ctk.CTkLabel(btn_row, text=self._t("ui.status_ready"), text_color="gray70")
        self.status_label.pack(side="left", padx=16)

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._ui_labels["ui.log_title"] = ctk.CTkLabel(log_frame, text=self._t("ui.log_title"), anchor="w")
        self._ui_labels["ui.log_title"].pack(fill="x", padx=12, pady=(8, 4))

        self.log_box = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._setup_log_interactions()
        bind_layout_safe_shortcuts(
            self,
            log_widget=self.log_box._textbox,
            on_copy_log=self._copy_log,
            on_select_all_log=lambda: self._select_all_log(None),
        )

    def _on_language_change(self, choice: str) -> None:
        self._lang_code = code_from_label(choice)
        set_language(self._lang_code)
        self._apply_language()

    def _apply_language(self) -> None:
        self.hint_label.configure(text=self._t("ui.hint"))
        for key, widget in self._ui_labels.items():
            widget.configure(text=self._t(key))
        self.browse_btn.configure(text=self._t("ui.btn_browse"))
        self.download_btn.configure(text=self._t("ui.btn_download"))
        self.copy_log_btn.configure(text=self._t("ui.btn_copy_log"))
        self.logs_btn.configure(text=self._t("ui.btn_logs"))
        if not (self._worker and self._worker.is_alive()):
            self.status_label.configure(text=self._t("ui.status_ready"))
        placeholders = {
            "ui.label_url": "ui.ph_url",
            "ui.label_start": "ui.ph_start",
            "ui.label_end": "ui.ph_end",
            "ui.label_title": "ui.ph_title",
        }
        for label_key, ph_key in placeholders.items():
            entry = self._entries.get(label_key)
            if entry:
                entry.configure(placeholder_text=self._t(ph_key))
        self._log_menu.entryconfigure(0, label=self._t("ui.menu_copy"))
        self._log_menu.entryconfigure(1, label=self._t("ui.menu_select_all"))

    def _row(
        self,
        parent: ctk.CTkFrame,
        label_key: str,
        variable: tk.StringVar,
        placeholder_key: str = "",
    ) -> None:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(10, 0))
        label = ctk.CTkLabel(row, text=self._t(label_key), width=140, anchor="w")
        label.pack(side="left")
        self._ui_labels[label_key] = label
        entry = ctk.CTkEntry(
            row,
            textvariable=variable,
            placeholder_text=self._t(placeholder_key) if placeholder_key else "",
        )
        entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self._entries[label_key] = entry

    def _setup_log_interactions(self) -> None:
        text = self.log_box._textbox
        text.configure(exportselection=True)

        self._log_menu = tk.Menu(self, tearoff=0)
        self._log_menu.add_command(label=self._t("ui.menu_copy"), command=self._copy_log)
        self._log_menu.add_command(
            label=self._t("ui.menu_select_all"), command=lambda: self._select_all_log(None)
        )

        text.bind("<Key>", self._on_log_key)
        text.bind("<Button-3>", self._show_log_menu)

    def _on_log_key(self, event: tk.Event) -> str | None:
        if is_layout_safe_ctrl(event):
            return None
        if event.keysym in {
            "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
            "Left", "Right", "Up", "Down", "Home", "End", "Prior", "Next", "Tab",
        }:
            return None
        return "break"

    def _show_log_menu(self, event: tk.Event) -> None:
        try:
            self._log_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._log_menu.grab_release()

    def _select_all_log(self, _event: tk.Event | None = None) -> str | None:
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
            language=self._lang_code,
            welcome_dismissed=self._welcome_dismissed,
        )

    def _show_welcome_dialog(self) -> None:
        if self._welcome_dismissed or self._extension_session:
            return
        ext_path = extension_dir()
        message = (
            f"{self._t('welcome.body')}\n\n"
            f"{self._t('welcome.extension_hint')}\n\n"
            f"{self._t('welcome.extension_path', path=ext_path)}\n\n"
            f"{self._t('welcome.extension_steps')}"
        )
        messagebox.showinfo(self._t("welcome.title"), message, parent=self)
        self._welcome_dismissed = True
        try:
            settings = self._collect_settings()
            settings.welcome_dismissed = True
            save_settings(settings)
        except OSError as exc:
            logger().error("Settings save failed: %s", exc)

    def _enter_extension_background_mode(self) -> None:
        self.withdraw()
        self._tray = TrayIcon(
            title=APP_NAME,
            on_show=lambda: self.after(0, self._show_window),
            on_quit=lambda: self.after(0, self._quit_app),
        )
        if not self._tray.start():
            logger().warning("Tray icon unavailable — running hidden without tray")
        logger().info("Extension session: background mode (tray)")

    def _show_window(self) -> None:
        self.deiconify()
        self.lift()
        self.focus_force()

    def _on_bridge_job_finished(self, job_id: str, success: bool) -> None:
        def handle() -> None:
            self._bridge_jobs_pending = max(0, self._bridge_jobs_pending - 1)
            logger().info("Bridge job %s finished success=%s pending=%s", job_id, success, self._bridge_jobs_pending)
            if (
                self._extension_session
                and success
                and self._bridge_jobs_pending == 0
                and not (self._worker and self._worker.is_alive())
            ):
                self._schedule_extension_quit()

        self.after(0, handle)

    def _track_bridge_job_started(self) -> None:
        self._bridge_jobs_pending += 1
        if self._quit_timer is not None:
            self.after_cancel(self._quit_timer)
            self._quit_timer = None

    def _schedule_extension_quit(self) -> None:
        if self._quit_timer is not None:
            self.after_cancel(self._quit_timer)
        self._quit_timer = self.after(2500, self._quit_app)

    def _quit_app(self) -> None:
        self._force_quit = True
        if self._quit_timer is not None:
            self.after_cancel(self._quit_timer)
            self._quit_timer = None
        if self._tray is not None:
            self._tray.stop()
            self._tray = None
        stop_bridge_server()
        try:
            save_settings(self._collect_settings())
        except OSError as exc:
            logger().error("Settings save failed: %s", exc)
        self.destroy()

    def _on_close(self) -> None:
        if self._extension_session and not self._force_quit:
            self.withdraw()
            return
        self._quit_app()

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
        self.download_btn.configure(state="disabled" if busy else "normal")

    def _on_download(self) -> None:
        if self._worker and self._worker.is_alive():
            return

        self._set_busy(True)
        self._log_queue.put(("status", self._t("ui.status_downloading")))

        try:
            output_dir = ensure_output_dir(self.dir_var.get())
            self.dir_var.set(str(output_dir))
        except OSError as exc:
            self._set_busy(False)
            messagebox.showerror(APP_NAME, self._t("ui.msg_output_dir_fail", error=exc))
            return

        lang = self._lang_code
        request = ClipRequest(
            url=self.url_var.get(),
            start=self.start_var.get(),
            end=self.end_var.get(),
            title=self.title_var.get(),
            output_dir=output_dir,
        )

        def worker() -> None:
            setup_logging()
            set_language(lang)
            try:
                def on_log(msg: str) -> None:
                    self._log_queue.put(msg)

                result = download_clip(request, on_log=on_log, language=lang)
                self._log_queue.put(("done", self._t("ui.msg_saved", path=result.output_path)))
                self._log_queue.put(("status", self._t("ui.status_done")))
            except ClipperError as exc:
                logger().exception("ClipperError")
                self._log_queue.put(str(exc))
                self._log_queue.put(("error", str(exc)))
                self._log_queue.put(("status", self._t("ui.status_error")))
            except Exception as exc:  # noqa: BLE001
                logger().exception("Unexpected error")
                self._log_queue.put(str(exc))
                self._log_queue.put(("error", self._t("ui.msg_unexpected", error=exc)))
                self._log_queue.put(("status", self._t("ui.status_error")))

        self._worker = threading.Thread(target=worker, daemon=True)
        self._worker.start()


def main() -> None:
    setup_logging()
    if is_protocol_launch() and bridge_already_running():
        logger().info("Protocol launch ignored — app already running")
        return
    app = ClipperApp()
    app.mainloop()


if __name__ == "__main__":
    main()
