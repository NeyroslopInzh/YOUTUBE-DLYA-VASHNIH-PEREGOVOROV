"""Ctrl+шорткаты независимо от раскладки (Windows: keycode вместо keysym)."""

from __future__ import annotations

import sys
import tkinter as tk
from collections.abc import Callable

# Физические keycode на Windows (QWERTY-позиции клавиш)
VK_A = 65
VK_C = 67
VK_V = 86
VK_X = 88
VK_Z = 90

_CTRL_KEYS = {VK_A, VK_C, VK_V, VK_X, VK_Z}


def is_ctrl_pressed(event: tk.Event) -> bool:
    return bool(event.state & 0x4)


def is_layout_safe_ctrl(event: tk.Event) -> bool:
    return is_ctrl_pressed(event) and event.keycode in _CTRL_KEYS


def bind_layout_safe_shortcuts(
    root: tk.Misc,
    *,
    log_widget: tk.Text | None = None,
    on_copy_log: Callable[[], None] | None = None,
    on_select_all_log: Callable[[], None] | None = None,
) -> None:
    if sys.platform != "win32":
        return

    def handler(event: tk.Event) -> str | None:
        if not is_layout_safe_ctrl(event):
            return None

        widget = event.widget
        code = event.keycode

        if log_widget is not None and widget is log_widget:
            if code == VK_C and on_copy_log:
                on_copy_log()
                return "break"
            if code == VK_A and on_select_all_log:
                on_select_all_log()
                return "break"
            return "break"

        if code == VK_C:
            _emit(widget, "<<Copy>>")
            return "break"
        if code == VK_V:
            _emit(widget, "<<Paste>>")
            return "break"
        if code == VK_X:
            _emit(widget, "<<Cut>>")
            return "break"
        if code == VK_A:
            _select_all(widget)
            return "break"
        if code == VK_Z:
            _emit(widget, "<<Undo>>")
            return "break"
        return None

    root.bind_all("<Control-KeyPress>", handler, add="+")
    root.bind_all("<Control-Key>", handler, add="+")


def _emit(widget: tk.Misc, sequence: str) -> None:
    try:
        widget.event_generate(sequence)
    except tk.TclError:
        pass


def _select_all(widget: tk.Misc) -> None:
    if isinstance(widget, tk.Entry):
        widget.select_range(0, tk.END)
        widget.icursor(tk.END)
        return
    if isinstance(widget, tk.Text):
        widget.tag_add("sel", "1.0", "end-1c")
        widget.mark_set("insert", "end-1c")
        widget.see("insert")
