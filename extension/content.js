// YVP Clipper — Chromium extension
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later
// See ../../LICENSE

/** Read current YouTube watch page state for the popup. */

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
