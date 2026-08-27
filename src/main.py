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
from i18n import LANGUAGE_FLAGS, get_i18n, set_language
from flag_icons import flag_ctk_image
from keyboard import bind_layout_safe_shortcuts, is_layout_safe_ctrl
from paths import default_output_dir, ensure_output_dir
from protocol import bridge_already_running, is_protocol_launch
from install_paths import extension_dir, was_installed_via_setup
from settings import FormSettings, load_settings, save_settings
from tray import TrayIcon
from pricol_gif import AnimatedGifLabel, pricol_gif_path

# Цвета кнопок флагов
_FLAG_ACTIVE = ("#1f6aa5", "#144870")  # fg, hover
_FLAG_IDLE = ("#2b2b2b", "#3a3a3a")


class ClipperApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry("920x480")
        self.minsize(820, 440)
        self._apply_window_icon()

        self._log_queue: queue.Queue[str | tuple[str, str]] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._ui_labels: dict[str, ctk.CTkLabel] = {}
        self._entries: dict[str, ctk.CTkEntry] = {}
        self._flag_buttons: dict[str, ctk.CTkButton] = {}
        self._pricol: AnimatedGifLabel | None = None
        self._lang_code = "ru"
        self._logs_expanded = False
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

    def _apply_window_icon(self) -> None:
        """Иконка окна/таскбара — тот же узбекский флаг."""
        candidates: list[Path] = []
        if getattr(sys, "frozen", False):
            meipass = getattr(sys, "_MEIPASS", None)
            if meipass:
                candidates.append(Path(meipass) / "assets" / "app.ico")
            candidates.append(Path(sys.executable).resolve().parent / "assets" / "app.ico")
        root = Path(__file__).resolve().parent.parent
        candidates.append(root / "assets" / "app.ico")
        for path in candidates:
            if path.is_file():
                try:
                    self.iconbitmap(default=str(path))
                    self.iconbitmap(str(path))
                except tk.TclError:
                    continue
                return

    def _build_ui(self, saved: FormSettings) -> None:
        self.header = ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=860,
            justify="center",
        )
        self.header.pack(pady=(16, 4))

        self.hint_label = ctk.CTkLabel(self, text=self._t("ui.hint"), text_color="gray70")
        self.hint_label.pack(pady=(0, 12))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=16, pady=(0, 8))

        form_body = ctk.CTkFrame(form, fg_color="transparent")
        form_body.pack(fill="x", padx=4, pady=4)

        fields = ctk.CTkFrame(form_body, fg_color="transparent")
        fields.pack(side="left", fill="both", expand=True)

        lang_row = ctk.CTkFrame(fields, fg_color="transparent")
        lang_row.pack(fill="x", padx=12, pady=(10, 0))
        self._ui_labels["ui.label_language"] = ctk.CTkLabel(
            lang_row, text=self._t("ui.label_language"), width=140, anchor="w"
        )
        self._ui_labels["ui.label_language"].pack(side="left")

        flags = ctk.CTkFrame(lang_row, fg_color="transparent")
        flags.pack(side="left", padx=(8, 0))
        self._flag_images: dict[str, object] = {}
        for code, _emoji in LANGUAGE_FLAGS:
            img = flag_ctk_image(code)
            self._flag_images[code] = img  # keep ref so GC не сожрёт
            btn = ctk.CTkButton(
                flags,
                text="",
                image=img,
                width=56,
                height=36,
                corner_radius=4,
                command=lambda c=code: self._set_language(c),
            )
            btn.pack(side="left", padx=(0, 6))
            self._flag_buttons[code] = btn
        self._refresh_flag_buttons()

        self.url_var = tk.StringVar(value=saved.url)
        self.start_var = tk.StringVar(value=saved.start)
        self.end_var = tk.StringVar(value=saved.end)
        self.title_var = tk.StringVar(value=saved.title)
        self.dir_var = tk.StringVar(value=saved.output_dir or str(default_output_dir()))

        self._row(fields, "ui.label_url", self.url_var, "ui.ph_url")
        self._row(fields, "ui.label_start", self.start_var, "ui.ph_start")
        self._row(fields, "ui.label_end", self.end_var, "ui.ph_end")
        self._row(fields, "ui.label_title", self.title_var, "ui.ph_title")

        dir_row = ctk.CTkFrame(fields, fg_color="transparent")
        dir_row.pack(fill="x", padx=12, pady=(10, 10))
        self._ui_labels["ui.label_output_dir"] = ctk.CTkLabel(
            dir_row, text=self._t("ui.label_output_dir"), width=140, anchor="w"
        )
        self._ui_labels["ui.label_output_dir"].pack(side="left")
        self._entries["dir"] = ctk.CTkEntry(dir_row, textvariable=self.dir_var)
        self._entries["dir"].pack(side="left", fill="x", expand=True, padx=(8, 8))
        self.browse_btn = ctk.CTkButton(dir_row, text=self._t("ui.btn_browse"), width=80, command=self._pick_dir)
        self.browse_btn.pack(side="right")

        gif_path = pricol_gif_path()
        if gif_path is not None:
            pricol_wrap = ctk.CTkFrame(form_body, fg_color="transparent")
            pricol_wrap.pack(side="right", padx=(8, 12), pady=10)
            try:
                self._pricol = AnimatedGifLabel(pricol_wrap, gif_path, max_width=220)
                self._pricol.pack(anchor="center")
                self._pricol.start()
            except Exception as exc:  # noqa: BLE001
                logger().warning("Pricol GIF failed: %s", exc)
                self._pricol = None

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

        self.status_label = ctk.CTkLabel(btn_row, text=self._t("ui.status_ready"), text_color="gray70")
        self.status_label.pack(side="left", padx=16)

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill="x", padx=16, pady=(0, 16))

        log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=8, pady=(6, 6))

        self.log_toggle_btn = ctk.CTkButton(
            log_header,
            text=self._t("ui.log_expand"),
            width=120,
            height=28,
            fg_color="transparent",
            hover_color=("#3a3a3a", "#3a3a3a"),
            text_color=("gray90", "gray90"),
            anchor="w",
            command=self._toggle_logs,
        )
        self.log_toggle_btn.pack(side="left")

        self.log_body = ctk.CTkFrame(self.log_frame, fg_color="transparent")

        log_tools = ctk.CTkFrame(self.log_body, fg_color="transparent")
        log_tools.pack(fill="x", padx=8, pady=(0, 6))

        self.copy_log_btn = ctk.CTkButton(
            log_tools, text=self._t("ui.btn_copy_log"), width=110, command=self._copy_log
        )
        self.copy_log_btn.pack(side="left")

        self.logs_btn = ctk.CTkButton(
            log_tools, text=self._t("ui.btn_logs"), width=70, command=self._open_logs
        )
        self.logs_btn.pack(side="left", padx=(8, 0))

        self.log_box = ctk.CTkTextbox(self.log_body, font=ctk.CTkFont(family="Consolas", size=12), height=180)
        self.log_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._setup_log_interactions()
        bind_layout_safe_shortcuts(
            self,
            log_widget=self.log_box._textbox,
            on_copy_log=self._copy_log,
            on_select_all_log=lambda: self._select_all_log(None),
        )

    def _refresh_flag_buttons(self) -> None:
        for code, btn in self._flag_buttons.items():
            if code == self._lang_code:
                btn.configure(fg_color=_FLAG_ACTIVE[0], hover_color=_FLAG_ACTIVE[1])
            else:
                btn.configure(fg_color=_FLAG_IDLE[0], hover_color=_FLAG_IDLE[1])

    def _set_language(self, code: str) -> None:
        if code == self._lang_code:
            return
        self._lang_code = code
        set_language(code)
        self._refresh_flag_buttons()
        self._apply_language()

    def _toggle_logs(self) -> None:
        self._logs_expanded = not self._logs_expanded
        if self._logs_expanded:
            self.log_body.pack(fill="both", expand=True)
            self.log_frame.pack_configure(fill="both", expand=True)
            self.log_toggle_btn.configure(text=self._t("ui.log_collapse"))
            self.geometry("920x640")
            self.minsize(820, 540)
        else:
            self.log_body.pack_forget()
            self.log_frame.pack_configure(fill="x", expand=False)
            self.log_toggle_btn.configure(text=self._t("ui.log_expand"))
            self.geometry("920x480")
            self.minsize(820, 440)

    def _apply_language(self) -> None:
        self.hint_label.configure(text=self._t("ui.hint"))
        for key, widget in self._ui_labels.items():
            widget.configure(text=self._t(key))
        self.browse_btn.configure(text=self._t("ui.btn_browse"))
        self.download_btn.configure(text=self._t("ui.btn_download"))
        self.copy_log_btn.configure(text=self._t("ui.btn_copy_log"))
        self.logs_btn.configure(text=self._t("ui.btn_logs"))
        self.log_toggle_btn.configure(
            text=self._t("ui.log_collapse" if self._logs_expanded else "ui.log_expand")
        )
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
        if self._pricol is not None:
            self._pricol.stop()
            self._pricol = None
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
