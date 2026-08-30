// YVP Clipper — proxy localhost fetches from extension origin (not youtube.com).
// Avoids Chromium Local Network Access blocking content-script → 127.0.0.1.
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type !== "YVP_HTTP") {
    return undefined;
  }
  const url = message.url;
  const init = message.init || {};
  fetch(url, init)
    .then(async (res) => {
      const data = await res.json().catch(() => ({}));
      sendResponse({ httpOk: res.ok, status: res.status, data });
    })
    .catch((err) => {
      sendResponse({ networkError: String(err && err.message ? err.message : err) });
    });
  return true;
});
