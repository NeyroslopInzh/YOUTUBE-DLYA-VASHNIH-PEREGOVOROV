// YVP Clipper — Chromium extension
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later
// See ../../LICENSE

/** Time helpers — same formats as desktop app (MM:SS, HH:MM:SS, seconds). */

function secondsToTime(totalSeconds) {
  const sec = Math.max(0, Math.floor(Number(totalSeconds) || 0));
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  if (h > 0) {
    return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  }
  return `${m}:${String(s).padStart(2, "0")}`;
}

function parseTimeToSeconds(value) {
  const raw = String(value || "").trim();
  if (!raw) {
    throw new Error("Время не указано");
  }
  if (/^\d+$/.test(raw)) {
    return parseInt(raw, 10);
  }
  const parts = raw.split(":").map((p) => parseInt(p, 10));
  if (parts.some((n) => Number.isNaN(n))) {
    throw new Error(`Неверный формат времени: ${raw}`);
  }
  if (parts.length === 2) {
    return parts[0] * 60 + parts[1];
  }
  if (parts.length === 3) {
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }
  throw new Error(`Неверный формат времени: ${raw}`);
}
