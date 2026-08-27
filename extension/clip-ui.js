// YVP Clipper — under-player bar + progress markers
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later

const YVP_MIN_GAP = 0.5;
const YVP_DEFAULT_LEN = 10;
const YVP_BAR_ID = "yvp-clip-bar";
const YVP_STYLE_ID = "yvp-clip-styles";
const YVP_LAYER_ID = "yvp-marker-layer";

const YvpClipUI = (() => {
  let active = false;
  let startSec = 0;
  let endSec = 10;
  let dragging = null;
  let loopHandler = null;
  let markerLayer = null;
  let progressHost = null;
  let busy = false;
  let layoutRaf = 0;

  function ensureStyles() {
    if (document.getElementById(YVP_STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = YVP_STYLE_ID;
    style.textContent = `
#yvp-clip-bar{
  display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:8px!important;
  margin:12px 0 8px!important;padding:0!important;border:none!important;background:transparent!important;
  font-family:Roboto,Arial,sans-serif!important;box-sizing:border-box!important;width:100%!important;
  position:relative!important;z-index:10!important;min-height:36px!important;
}
#yvp-clip-bar button.yvp-btn{
  appearance:none!important;-webkit-appearance:none!important;border:none!important;outline:none!important;
  margin:0!important;border-radius:18px!important;padding:0 16px!important;height:36px!important;
  font-size:14px!important;font-weight:500!important;font-family:Roboto,Arial,sans-serif!important;
  line-height:36px!important;cursor:pointer!important;white-space:nowrap!important;box-shadow:none!important;
  display:inline-block!important;visibility:visible!important;opacity:1!important;
}
#yvp-clip-bar button.yvp-btn[hidden]{display:none!important}
#yvp-clip-bar button.yvp-btn:disabled{opacity:.5!important;cursor:not-allowed!important}
#yvp-clip-bar button.yvp-btn-subscribe{background:#f1f1f1!important;color:#0f0f0f!important}
#yvp-clip-bar button.yvp-btn-subscribe:hover:not(:disabled){background:#d9d9d9!important}
#yvp-clip-bar button.yvp-btn-ghost{background:rgba(255,255,255,.1)!important;color:#f1f1f1!important}
#yvp-clip-bar button.yvp-btn-ghost:hover:not(:disabled){background:rgba(255,255,255,.2)!important}
#yvp-marker-layer{position:absolute!important;left:0!important;right:0!important;height:18px!important;pointer-events:none!important;z-index:60!important;overflow:visible!important}
#yvp-marker-layer .yvp-range-fill{position:absolute!important;top:6px!important;height:6px!important;border-radius:3px!important;background:rgba(62,166,255,.55)!important;pointer-events:none!important}
#yvp-marker-layer .yvp-marker{position:absolute!important;top:1px!important;width:16px!important;height:16px!important;margin-left:-8px!important;border-radius:50%!important;border:2px solid #fff!important;box-shadow:0 1px 4px rgba(0,0,0,.6)!important;pointer-events:auto!important;cursor:ew-resize!important;z-index:61!important;box-sizing:border-box!important}
#yvp-marker-layer .yvp-marker-start{background:#3ea6ff!important}
#yvp-marker-layer .yvp-marker-end{background:#2ba640!important}
`;
    (document.head || document.documentElement).appendChild(style);
  }

  function getVideo() {
    return (
      document.querySelector("#movie_player video.html5-main-video") ||
      document.querySelector(".html5-video-player video") ||
      document.querySelector("ytd-watch-flexy video") ||
      document.querySelector("video")
    );
  }

  function getDuration(video) {
    const d = video?.duration;
    return Number.isFinite(d) && d > 0 ? d : null;
  }

  function getMoviePlayer() {
    return (
      document.querySelector("#movie_player") ||
      document.querySelector(".html5-video-player") ||
      null
    );
  }

  function findProgressBar() {
    const root = getMoviePlayer() || document;
    return (
      root.querySelector(".ytp-progress-bar") ||
      root.querySelector(".ytp-progress-bar-container") ||
      null
    );
  }

  /** Видимая колонка primary — не скрытый дубль DOM. */
  function findPrimaryInner() {
    const candidates = [
      ...document.querySelectorAll("ytd-watch-flexy #primary-inner"),
      ...document.querySelectorAll("#primary-inner"),
    ];
    for (const el of candidates) {
      if (!el || !el.isConnected) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width > 200 && rect.height > 100) return el;
    }
    return candidates[0] || null;
  }

  function findMountPoint() {
    const primary = findPrimaryInner();
    if (primary) {
      const player =
        primary.querySelector("#player") ||
        primary.querySelector("ytd-player") ||
        primary.querySelector("#player-container-outer");
      if (player) return { parent: player.parentElement || primary, after: player };
      const below = primary.querySelector("#below");
      if (below) return { parent: below, after: null, prepend: true };
      return { parent: primary, after: null, prepend: true };
    }

    const player =
      document.querySelector("ytd-watch-flexy #player") ||
      document.querySelector("#player-container-outer") ||
      document.querySelector("#player");
    if (player?.parentElement) {
      return { parent: player.parentElement, after: player };
    }
    return null;
  }

  function placeBar(bar) {
    const mount = findMountPoint();
    if (!mount?.parent) return false;

    if (mount.prepend) {
      mount.parent.insertBefore(bar, mount.parent.firstChild);
    } else if (mount.after) {
      mount.after.after(bar);
    } else {
      mount.parent.appendChild(bar);
    }
    return true;
  }

  function isBarInGoodPlace(bar) {
    if (!bar?.isConnected) return false;
    const primary = findPrimaryInner();
    if (primary && primary.contains(bar)) {
      const rect = bar.getBoundingClientRect();
      return rect.width > 20;
    }
    // нет primary — хотя бы в документе и видима
    const rect = bar.getBoundingClientRect();
    return rect.width > 20 && rect.bottom > 0;
  }

  function ensureBar() {
    ensureStyles();
    let bar = document.getElementById(YVP_BAR_ID);

    if (bar && isBarInGoodPlace(bar)) {
      return bar;
    }

    if (bar) {
      bar.remove();
    }

    bar = document.createElement("div");
    bar.id = YVP_BAR_ID;

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "yvp-btn yvp-btn-subscribe";
    toggle.dataset.yvp = "toggle";
    toggle.textContent = "Скачать отрезок";
    toggle.style.cssText =
      "appearance:none;border:none;border-radius:18px;padding:0 16px;height:36px;background:#f1f1f1;color:#0f0f0f;font:500 14px Roboto,Arial,sans-serif;cursor:pointer;";

    const download = document.createElement("button");
    download.type = "button";
    download.className = "yvp-btn yvp-btn-subscribe";
    download.dataset.yvp = "download";
    download.textContent = "Скачать";
    download.hidden = true;
    download.style.cssText = toggle.style.cssText;

    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.className = "yvp-btn yvp-btn-ghost";
    cancel.dataset.yvp = "cancel";
    cancel.textContent = "Удалить";
    cancel.hidden = true;
    cancel.style.cssText =
      "appearance:none;border:none;border-radius:18px;padding:0 16px;height:36px;background:rgba(255,255,255,.1);color:#f1f1f1;font:500 14px Roboto,Arial,sans-serif;cursor:pointer;";

    bar.append(toggle, download, cancel);

    if (!placeBar(bar)) {
      bar.remove();
      return null;
    }

    toggle.addEventListener("click", onToggle);
    download.addEventListener("click", onDownload);
    cancel.addEventListener("click", deactivate);
    return bar;
  }

  function setIdleUi() {
    const bar = document.getElementById(YVP_BAR_ID);
    if (!bar) return;
    bar.querySelector('[data-yvp="toggle"]').hidden = false;
    bar.querySelector('[data-yvp="download"]').hidden = true;
    bar.querySelector('[data-yvp="cancel"]').hidden = true;
  }

  function setActiveUi() {
    const bar = document.getElementById(YVP_BAR_ID);
    if (!bar) return;
    bar.querySelector('[data-yvp="toggle"]').hidden = true;
    bar.querySelector('[data-yvp="download"]').hidden = false;
    bar.querySelector('[data-yvp="cancel"]').hidden = false;
  }

  function setBusy(next) {
    busy = next;
    const bar = document.getElementById(YVP_BAR_ID);
    if (!bar) return;
    for (const key of ["download", "cancel", "toggle"]) {
      const el = bar.querySelector(`[data-yvp="${key}"]`);
      if (el) el.disabled = next;
    }
  }

  function pct(time, duration) {
    if (!duration) return 0;
    return Math.max(0, Math.min(100, (time / duration) * 100));
  }

  function ensureMarkers() {
    ensureStyles();
    const player = getMoviePlayer();
    const progress = findProgressBar();
    if (!player || !progress) return false;

    if (getComputedStyle(player).position === "static") {
      player.style.position = "relative";
    }

    if (markerLayer && markerLayer.isConnected && markerLayer.parentElement === player) {
      layoutMarkers();
      return true;
    }

    destroyMarkers();
    progressHost = progress;
    markerLayer = document.createElement("div");
    markerLayer.id = YVP_LAYER_ID;
    markerLayer.innerHTML = `
      <div class="yvp-range-fill" data-yvp="fill"></div>
      <div class="yvp-marker yvp-marker-start" data-yvp="m-start" title="Начало"></div>
      <div class="yvp-marker yvp-marker-end" data-yvp="m-end" title="Конец"></div>
    `;
    player.appendChild(markerLayer);

    markerLayer.querySelector('[data-yvp="m-start"]').addEventListener("pointerdown", (e) => beginDrag(e, "start"));
    markerLayer.querySelector('[data-yvp="m-end"]').addEventListener("pointerdown", (e) => beginDrag(e, "end"));
    layoutMarkers();
    return true;
  }

  function destroyMarkers() {
    markerLayer?.remove();
    markerLayer = null;
    progressHost = null;
  }

  function layoutMarkers() {
    if (!markerLayer) return;
    const player = getMoviePlayer();
    const progress = findProgressBar() || progressHost;
    const video = getVideo();
    const duration = getDuration(video);
    if (!player || !progress || !duration) return;

    progressHost = progress;
    const playerRect = player.getBoundingClientRect();
    const barRect = progress.getBoundingClientRect();
    if (playerRect.width <= 0 || barRect.width <= 0) return;

    const top = barRect.top - playerRect.top + (barRect.height - 18) / 2;
    const left = barRect.left - playerRect.left;
    const width = barRect.width;

    markerLayer.style.top = `${Math.max(0, top)}px`;
    markerLayer.style.left = `${left}px`;
    markerLayer.style.width = `${width}px`;
    markerLayer.style.right = "auto";

    const fill = markerLayer.querySelector('[data-yvp="fill"]');
    const mStart = markerLayer.querySelector('[data-yvp="m-start"]');
    const mEnd = markerLayer.querySelector('[data-yvp="m-end"]');
    const leftPct = pct(startSec, duration);
    const rightPct = pct(endSec, duration);
    fill.style.left = `${leftPct}%`;
    fill.style.width = `${Math.max(0, rightPct - leftPct)}%`;
    mStart.style.left = `${leftPct}%`;
    mEnd.style.left = `${rightPct}%`;
  }

  function scheduleLayout() {
    if (layoutRaf) return;
    layoutRaf = requestAnimationFrame(() => {
      layoutRaf = 0;
      layoutMarkers();
    });
  }

  function beginDrag(event, which) {
    if (!active || busy) return;
    event.preventDefault();
    event.stopPropagation();
    dragging = which;
    const onMove = (e) => {
      e.preventDefault();
      e.stopPropagation();
      moveDrag(e);
    };
    const onUp = (e) => {
      e.preventDefault();
      e.stopPropagation();
      dragging = null;
      window.removeEventListener("pointermove", onMove, true);
      window.removeEventListener("pointerup", onUp, true);
      window.removeEventListener("pointercancel", onUp, true);
    };
    window.addEventListener("pointermove", onMove, true);
    window.addEventListener("pointerup", onUp, true);
    window.addEventListener("pointercancel", onUp, true);
  }

  function moveDrag(event) {
    if (!dragging || !markerLayer) return;
    const video = getVideo();
    const duration = getDuration(video);
    if (!duration) return;

    const rect = markerLayer.getBoundingClientRect();
    if (rect.width <= 0) return;
    const ratio = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    const t = ratio * duration;

    if (dragging === "start") {
      startSec = Math.max(0, Math.min(t, endSec - YVP_MIN_GAP));
      if (video) video.currentTime = startSec;
    } else {
      endSec = Math.min(duration, Math.max(t, startSec + YVP_MIN_GAP));
    }
    layoutMarkers();
  }

  function startLoop() {
    stopLoop();
    const video = getVideo();
    if (!video) return;
    loopHandler = () => {
      if (!active) return;
      if (video.currentTime < startSec - 0.05) {
        video.currentTime = startSec;
      } else if (video.currentTime > endSec) {
        video.currentTime = startSec;
      }
    };
    video.addEventListener("timeupdate", loopHandler);
  }

  function stopLoop() {
    const video = getVideo();
    if (video && loopHandler) {
      video.removeEventListener("timeupdate", loopHandler);
    }
    loopHandler = null;
  }

  function activate() {
    const video = getVideo();
    if (!video) return;

    const duration = getDuration(video);
    startSec = Math.max(0, video.currentTime || 0);
    endSec = startSec + YVP_DEFAULT_LEN;
    if (duration != null) {
      endSec = Math.min(endSec, duration);
      if (endSec - startSec < YVP_MIN_GAP) {
        startSec = Math.max(0, duration - YVP_DEFAULT_LEN);
        endSec = duration;
      }
    }

    active = true;
    setActiveUi();

    let tries = 0;
    const tryMarkers = () => {
      if (!active) return;
      if (ensureMarkers() || tries >= 25) return;
      tries += 1;
      setTimeout(tryMarkers, 120);
    };
    tryMarkers();

    const player = getMoviePlayer();
    if (player) {
      player.classList.remove("ytp-autohide");
      player.dispatchEvent(new MouseEvent("mousemove", { bubbles: true }));
    }

    startLoop();
    window.addEventListener("resize", scheduleLayout);
  }

  function deactivate() {
    active = false;
    busy = false;
    dragging = null;
    stopLoop();
    destroyMarkers();
    setIdleUi();
    window.removeEventListener("resize", scheduleLayout);
  }

  function onToggle() {
    if (busy) return;
    if (active) deactivate();
    else activate();
  }

  function readPageMeta() {
    const h1 =
      document.querySelector("h1.ytd-watch-metadata yt-formatted-string") ||
      document.querySelector("#title h1 yt-formatted-string") ||
      document.querySelector("h1 yt-formatted-string");
    const title = (h1?.textContent || document.title.replace(/\s*-\s*YouTube\s*$/i, "")).trim();
    const suggested = title
      .replace(/[<>:"/\\|?*]/g, "_")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 120);
    return { url: window.location.href, title: suggested || "clip" };
  }

  async function onDownload() {
    if (!active || busy) return;
    if (endSec <= startSec) return;

    setBusy(true);
    const ensured = await yvpEnsureAppRunning();
    if (!ensured.ok) {
      setBusy(false);
      return;
    }

    const meta = readPageMeta();
    try {
      const started = await yvpStartClip({
        url: meta.url,
        start: secondsToTime(startSec),
        end: secondsToTime(endSec),
        title: meta.title,
        use_browser_downloads: true,
      });
      const job = await yvpPollJob(started.job_id, () => {});
      if (job.status === "done") deactivate();
      else setBusy(false);
    } catch {
      setBusy(false);
    }
  }

  function isWatchPage() {
    return /\/watch/.test(location.pathname) || location.hostname.includes("youtu.be");
  }

  function inject() {
    if (!isWatchPage()) {
      deactivate();
      document.getElementById(YVP_BAR_ID)?.remove();
      return;
    }
    try {
      ensureBar();
      if (active) ensureMarkers();
    } catch (err) {
      console.warn("[YVP] inject failed", err);
    }
  }

  function onNavigated() {
    deactivate();
    inject();
  }

  return {
    inject,
    onNavigated,
    deactivate,
    isActive: () => active,
    layoutMarkers: scheduleLayout,
  };
})();
