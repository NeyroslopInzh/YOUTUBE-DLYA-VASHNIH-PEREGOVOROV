// YVP Clipper — Chromium extension content script
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later
// See ../../LICENSE

/** Read current YouTube watch page state for the popup + mount clip UI. */

function cleanWatchUrl() {
  const url = new URL(window.location.href);
  if (url.hostname === "youtu.be") {
    const id = url.pathname.replace(/^\//, "").split("/")[0];
    return id ? `https://www.youtube.com/watch?v=${id}` : window.location.href;
  }
  if (url.searchParams.has("v")) {
    return `https://www.youtube.com/watch?v=${url.searchParams.get("v")}`;
  }
  return window.location.href;
}

function readVideoTitle() {
  const h1 =
    document.querySelector("h1.ytd-watch-metadata yt-formatted-string") ||
    document.querySelector("#title h1 yt-formatted-string") ||
    document.querySelector("h1 yt-formatted-string");
  if (h1?.textContent?.trim()) {
    return h1.textContent.trim();
  }
  return document.title.replace(/\s*-\s*YouTube\s*$/i, "").trim();
}

function sanitizeFilename(name) {
  return name
    .replace(/[<>:"/\\|?*]/g, "_")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 120);
}

function getVideoInfo() {
  const video = document.querySelector("video");
  const title = readVideoTitle();
  return {
    ok: Boolean(video),
    url: window.location.href,
    cleanUrl: cleanWatchUrl(),
    startSeconds: video ? video.currentTime : 0,
    durationSeconds: video && Number.isFinite(video.duration) ? video.duration : null,
    title,
    suggestedFilename: sanitizeFilename(title || "clip"),
  };
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "GET_VIDEO_INFO") {
    sendResponse(getVideoInfo());
    return false;
  }
  return false;
});

(function mountYvpClipUi() {
  let lastUrl = location.href;
  let injectScheduled = false;

  function scheduleInject() {
    if (injectScheduled) return;
    injectScheduled = true;
    requestAnimationFrame(() => {
      injectScheduled = false;
      try {
        if (location.href !== lastUrl) {
          lastUrl = location.href;
          YvpClipUI.onNavigated();
          return;
        }
        YvpClipUI.inject();
      } catch (err) {
        console.warn("[YVP] scheduleInject", err);
      }
    });
  }

  document.addEventListener("yt-navigate-finish", () => {
    lastUrl = location.href;
    try {
      YvpClipUI.onNavigated();
    } catch (err) {
      console.warn("[YVP] navigate", err);
    }
  });

  // Не слушаем весь document — YouTube орёт мутациями и мы сами себе мешаем.
  // Цепляемся к primary / player, когда появятся.
  function observeMount() {
    const root =
      document.querySelector("ytd-watch-flexy") ||
      document.querySelector("#content") ||
      document.body;
    if (!root) return;
    const obs = new MutationObserver(() => scheduleInject());
    obs.observe(root, { childList: true, subtree: true });
  }

  observeMount();
  scheduleInject();
  // Пока SPA догружает колонки — добиваем inject
  let kicks = 0;
  const boot = setInterval(() => {
    scheduleInject();
    kicks += 1;
    if (kicks >= 20) clearInterval(boot);
  }, 500);

  setInterval(() => {
    try {
      if (YvpClipUI.isActive()) {
        YvpClipUI.layoutMarkers();
        YvpClipUI.inject();
      } else if (/\/watch/.test(location.pathname)) {
        YvpClipUI.inject();
      }
    } catch (err) {
      console.warn("[YVP] tick", err);
    }
  }, 2000);
})();
