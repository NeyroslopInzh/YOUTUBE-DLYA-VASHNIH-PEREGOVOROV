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
  let dragMoveHandler = null;
  let dragUpHandler = null;

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

/* Глушим нативный YT scrubber, пока активен режим клипа */
html.yvp-clip-active .ytp-progress-bar,
html.yvp-clip-active .ytp-progress-list,
html.yvp-clip-active .ytp-chapters-container,
html.yvp-clip-active .ytp-hover-progress,
html.yvp-clip-active .ytp-progress-bar-padding{
  pointer-events:none!important;
}
html.yvp-clip-active .ytp-progress-bar-container{
  cursor:ew-resize!important;
}

#yvp-marker-layer{
  position:absolute!important;left:0!important;right:0!important;top:-12px!important;bottom:-12px!important;
  height:auto!important;min-height:40px!important;pointer-events:auto!important;
  z-index:2147483646!important;overflow:visible!important;cursor:ew-resize!important;
  touch-action:none!important;background:transparent!important;
}
#yvp-marker-layer .yvp-range-fill{
  position:absolute!important;top:50%!important;transform:translateY(-50%)!important;height:6px!important;
  border-radius:3px!important;background:rgba(62,166,255,.55)!important;pointer-events:none!important;
}
#yvp-marker-layer .yvp-marker{
  position:absolute!important;top:50%!important;width:18px!important;height:18px!important;
  margin:0!important;transform:translate(-50%,-50%)!important;border-radius:50%!important;
  border:2px solid #fff!important;box-shadow:0 1px 4px rgba(0,0,0,.65)!important;
  pointer-events:none!important;box-sizing:border-box!important;
}
#yvp-marker-layer .yvp-marker-start{background:#3ea6ff!important}
#yvp-marker-layer .yvp-marker-end{background:#2ba640!important}

/* Бар кнопок не должен торчать поверх fullscreen */
html.yvp-fs-hide-bar #yvp-clip-bar,
#movie_player.ytp-fullscreen ~ #yvp-clip-bar,
.ytp-fullscreen #yvp-clip-bar{
  display:none!important;
}
`;
    (document.head || document.documentElement).appendChild(style);
  }

  function setYtScrubberBlocked(blocked) {
    document.documentElement.classList.toggle("yvp-clip-active", Boolean(blocked));
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
    return document.querySelector("#movie_player") || document.querySelector(".html5-video-player") || null;
  }

  function findProgressContainer() {
    const root = getMoviePlayer() || document;
    return (
      root.querySelector(".ytp-progress-bar-container") ||
      root.querySelector(".ytp-progress-bar")?.parentElement ||
      null
    );
  }

  function findPrimaryInner() {
    const candidates = [
      ...document.querySelectorAll("ytd-watch-flexy #primary-inner"),
      ...document.querySelectorAll("#columns #primary-inner"),
      ...document.querySelectorAll("#primary-inner"),
    ];
    for (const el of candidates) {
      if (!el?.isConnected) continue;
      if (el.closest("[hidden]")) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width > 200 && rect.height > 100) return el;
    }
    return null;
  }

  function isForbiddenParent(el) {
    if (!el) return true;
    if (el === document.body || el === document.documentElement) return true;
    if (el.id === "watch7-content") return true;
    return false;
  }

  /** Только под плеером. Никогда body — иначе кнопка у логотипа / поверх fullscreen. */
  function findMountPoint() {
    const primary = findPrimaryInner();
    if (primary) {
      const below = primary.querySelector("#below");
      if (below && !isForbiddenParent(below)) {
        return { parent: below, after: null, prepend: true };
      }
      const player =
        primary.querySelector("#player") ||
        primary.querySelector("ytd-player") ||
        primary.querySelector("#player-container-outer");
      if (player?.parentElement && !isForbiddenParent(player.parentElement)) {
        return { parent: player.parentElement, after: player };
      }
      if (!isForbiddenParent(primary)) {
        return { parent: primary, after: null, prepend: true };
      }
    }

    const below =
      document.querySelector("ytd-watch-flexy #below") ||
      document.querySelector("ytd-app #below");
    if (below && below.closest("ytd-app, ytd-watch-flexy") && !isForbiddenParent(below)) {
      return { parent: below, after: null, prepend: true };
    }
    return null;
  }

  function placeBar(bar) {
    const mount = findMountPoint();
    if (!mount?.parent || isForbiddenParent(mount.parent)) return false;
    if (mount.prepend) mount.parent.insertBefore(bar, mount.parent.firstChild);
    else if (mount.after) mount.after.after(bar);
    else mount.parent.appendChild(bar);
    if (isForbiddenParent(bar.parentElement)) {
      bar.remove();
      return false;
    }
    return true;
  }

  function isFullscreenUi() {
    if (document.fullscreenElement || document.webkitFullscreenElement) return true;
    const player = getMoviePlayer();
    if (player?.classList.contains("ytp-fullscreen")) return true;
    if (document.body?.classList.contains("ytp-fullscreen") || document.documentElement?.classList.contains("ytp-fullscreen")) {
      return true;
    }
    return Boolean(document.querySelector("#movie_player.ytp-fullscreen, .html5-video-player.ytp-fullscreen"));
  }

  function syncBarVisibility() {
    const bar = document.getElementById(YVP_BAR_ID);
    if (!bar) return;
    const hide = isFullscreenUi();
    bar.style.setProperty("display", hide ? "none" : "flex", "important");
    document.documentElement.classList.toggle("yvp-fs-hide-bar", hide);
  }

  function isBarInGoodPlace(bar) {
    if (!bar?.isConnected) return false;
    if (isForbiddenParent(bar.parentElement)) return false;
    const primary = findPrimaryInner();
    if (primary && primary.contains(bar)) return bar.getBoundingClientRect().width > 20;
    if (bar.closest("ytd-watch-flexy #below, ytd-watch-flexy #primary-inner, #primary-inner #below")) {
      return bar.getBoundingClientRect().width > 20;
    }
    return false;
  }

  function ensureBar() {
    ensureStyles();
    let bar = document.getElementById(YVP_BAR_ID);
    if (bar && isBarInGoodPlace(bar)) return bar;
    if (bar) bar.remove();

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

  function markerXs(width, duration) {
    const minGapPx = Math.max(16, (YVP_MIN_GAP / duration) * width);
    let startX = (startSec / duration) * width;
    let endX = (endSec / duration) * width;
    startX = Math.max(0, Math.min(startX, width - minGapPx));
    endX = Math.max(startX + minGapPx, Math.min(endX, width));
    return { startX, endX };
  }

  function killEvent(e) {
    e.preventDefault();
    e.stopPropagation();
    if (typeof e.stopImmediatePropagation === "function") e.stopImmediatePropagation();
  }

  function onLayerPointerDown(event) {
    if (!active || busy || !markerLayer) return;
    if (event.button != null && event.button !== 0) return;
    killEvent(event);

    const video = getVideo();
    const duration = getDuration(video);
    if (!duration) return;

    const rect = markerLayer.getBoundingClientRect();
    if (rect.width <= 0) return;
    const x = event.clientX - rect.left;
    const { startX, endX } = markerXs(rect.width, duration);
    const which = Math.abs(x - startX) <= Math.abs(x - endX) ? "start" : "end";
    beginDrag(event, which);
  }

  function ensureMarkers() {
    ensureStyles();
    const container = findProgressContainer();
    if (!container) return false;

    if (getComputedStyle(container).position === "static") {
      container.style.position = "relative";
    }

    if (markerLayer && markerLayer.isConnected && markerLayer.parentElement === container) {
      layoutMarkers();
      return true;
    }

    destroyMarkers();
    progressHost = container;
    markerLayer = document.createElement("div");
    markerLayer.id = YVP_LAYER_ID;
    markerLayer.innerHTML = `
      <div class="yvp-range-fill" data-yvp="fill"></div>
      <div class="yvp-marker yvp-marker-start" data-yvp="m-start" title="Начало"></div>
      <div class="yvp-marker yvp-marker-end" data-yvp="m-end" title="Конец"></div>
    `;
    container.appendChild(markerLayer);

    markerLayer.addEventListener("pointerdown", onLayerPointerDown, true);
    markerLayer.addEventListener("mousedown", killEvent, true);
    markerLayer.addEventListener("click", killEvent, true);
    markerLayer.addEventListener("dblclick", killEvent, true);

    layoutMarkers();
    return true;
  }

  function clearDragListeners() {
    if (dragMoveHandler) {
      window.removeEventListener("pointermove", dragMoveHandler, true);
      window.removeEventListener("mousemove", dragMoveHandler, true);
      dragMoveHandler = null;
    }
    if (dragUpHandler) {
      window.removeEventListener("pointerup", dragUpHandler, true);
      window.removeEventListener("pointercancel", dragUpHandler, true);
      window.removeEventListener("mouseup", dragUpHandler, true);
      dragUpHandler = null;
    }
  }

  function destroyMarkers() {
    clearDragListeners();
    dragging = null;
    markerLayer?.remove();
    markerLayer = null;
    progressHost = null;
  }

  function layoutMarkers() {
    if (!markerLayer) return;
    const video = getVideo();
    const duration = getDuration(video);
    const width = markerLayer.getBoundingClientRect().width || markerLayer.clientWidth;
    if (!duration || width <= 0) return;

    const fill = markerLayer.querySelector('[data-yvp="fill"]');
    const mStart = markerLayer.querySelector('[data-yvp="m-start"]');
    const mEnd = markerLayer.querySelector('[data-yvp="m-end"]');
    const { startX, endX } = markerXs(width, duration);

    fill.style.left = `${startX}px`;
    fill.style.width = `${Math.max(0, endX - startX)}px`;
    mStart.style.left = `${startX}px`;
    mEnd.style.left = `${endX}px`;
  }

  function scheduleLayout() {
    if (layoutRaf) return;
    layoutRaf = requestAnimationFrame(() => {
      layoutRaf = 0;
      layoutMarkers();
    });
  }

  function beginDrag(event, which) {
    if (!active || busy || !markerLayer) return;
    clearDragListeners();
    dragging = which;

    try {
      markerLayer.setPointerCapture(event.pointerId);
    } catch {
      /* ignore */
    }

    dragMoveHandler = (e) => {
      killEvent(e);
      moveDrag(e);
    };
    dragUpHandler = (e) => {
      killEvent(e);
      dragging = null;
      try {
        markerLayer?.releasePointerCapture(e.pointerId);
      } catch {
        /* ignore */
      }
      clearDragListeners();
    };

    window.addEventListener("pointermove", dragMoveHandler, true);
    window.addEventListener("pointerup", dragUpHandler, true);
    window.addEventListener("pointercancel", dragUpHandler, true);
    window.addEventListener("mousemove", dragMoveHandler, true);
    window.addEventListener("mouseup", dragUpHandler, true);
    moveDrag(event);
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
      if (video.currentTime < startSec - 0.05) video.currentTime = startSec;
      else if (video.currentTime > endSec) video.currentTime = startSec;
    };
    video.addEventListener("timeupdate", loopHandler);
  }

  function stopLoop() {
    const video = getVideo();
    if (video && loopHandler) video.removeEventListener("timeupdate", loopHandler);
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
    setYtScrubberBlocked(true);
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
    setBusy(false);
    setYtScrubberBlocked(false);
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
      syncBarVisibility();
      if (active && !isFullscreenUi()) ensureMarkers();
    } catch (err) {
      console.warn("[YVP] inject failed", err);
    }
  }

  function onNavigated() {
    deactivate();
    inject();
  }

  // fullscreen / theater
  document.addEventListener("fullscreenchange", syncBarVisibility);
  document.addEventListener("webkitfullscreenchange", syncBarVisibility);
  window.addEventListener("resize", () => {
    syncBarVisibility();
    scheduleLayout();
  });

  return {
    inject,
    onNavigated,
    deactivate,
    isActive: () => active,
    layoutMarkers: scheduleLayout,
    syncBarVisibility,
  };
})();
