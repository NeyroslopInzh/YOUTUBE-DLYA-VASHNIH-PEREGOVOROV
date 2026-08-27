// YVP Clipper — Chromium extension
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later
// See ../../LICENSE

/** Time helpers — MM:SS[.mmm], HH:MM:SS[.mmm], or seconds (int/float). */

function secondsToTime(totalSeconds) {
  const msTotal = Math.max(0, Math.round((Number(totalSeconds) || 0) * 1000));
  const h = Math.floor(msTotal / 3600000);
  const m = Math.floor((msTotal % 3600000) / 60000);
  const s = Math.floor((msTotal % 60000) / 1000);
  const ms = msTotal % 1000;
  const frac = `.${String(ms).padStart(3, "0")}`;
  if (h > 0) {
    return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}${frac}`;
  }
  return `${m}:${String(s).padStart(2, "0")}${frac}`;
}

function parseTimeToSeconds(value) {
  const raw = String(value || "").trim();
  if (!raw) {
    throw new Error("Время не указано");
  }
  if (/^\d+(\.\d+)?$/.test(raw)) {
    return Number(raw);
  }
  const parts = raw.split(":");
  if (parts.some((p) => p === "" || Number.isNaN(Number(p)))) {
    throw new Error(`Неверный формат времени: ${raw}`);
  }
  if (parts.length === 2) {
    return Number(parts[0]) * 60 + Number(parts[1]);
  }
  if (parts.length === 3) {
    return Number(parts[0]) * 3600 + Number(parts[1]) * 60 + Number(parts[2]);
  }
  throw new Error(`Неверный формат времени: ${raw}`);
}
