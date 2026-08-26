// YVP Clipper — Chromium extension → desktop app bridge
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later

const APP_BRIDGE_URL = "http://127.0.0.1:8766";
const YVP_PROTOCOL_URL = "yvp://start";
const GITHUB_RELEASES_URL =
  "https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases/latest";
const APP_LAUNCH_TIMEOUT_MS = 15000;
const APP_LAUNCH_POLL_MS = 500;

const els = {
  pageError: document.getElementById("page-error"),
  hostError: document.getElementById("host-error"),
  installPanel: document.getElementById("install-panel"),
  linkReleases: document.getElementById("link-releases"),
  btnRetryApp: document.getElementById("btn-retry-app"),
  form: document.getElementById("clip-form"),
  start: document.getElementById("start"),
  end: document.getElementById("end"),
  plusSeconds: document.getElementById("plus-seconds"),
  title: document.getElementById("title"),
  btnRefreshStart: document.getElementById("btn-refresh-start"),
  btnCalcEnd: document.getElementById("btn-calc-end"),
  btnDownload: document.getElementById("btn-download"),
  log: document.getElementById("log"),
  status: document.getElementById("status"),
};

let videoInfo = null;
let pollTimer = null;
let appBridgeOk = false;
let bridgeInfo = null;

function setStatus(text) {
  els.status.textContent = text;
}

function appendLog(line) {
  els.log.textContent += `${line}\n`;
  els.log.scrollTop = els.log.scrollHeight;
}

function clearLog() {
  els.log.textContent = "";
}

function show(el, text) {
  if (text !== undefined) {
    el.textContent = text;
  }
  el.classList.remove("hidden");
}

function hide(el) {
  el.classList.add("hidden");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function loadVideoInfo() {
  const tab = await getActiveTab();
  if (!tab?.id || (!tab.url?.includes("youtube.com/watch") && !tab.url?.includes("youtu.be/"))) {
    show(els.pageError, "Открой страницу YouTube с видео (watch) и снова нажми на иконку расширения.");
    els.btnDownload.disabled = true;
    return null;
  }

  hide(els.pageError);

  let info;
  try {
    info = await chrome.tabs.sendMessage(tab.id, { type: "GET_VIDEO_INFO" });
  } catch {
    try {
      await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
      info = await chrome.tabs.sendMessage(tab.id, { type: "GET_VIDEO_INFO" });
    } catch (err) {
      show(els.pageError, `Не удалось прочитать плеер: ${err.message}`);
      els.btnDownload.disabled = true;
      return null;
    }
  }

  if (!info?.ok) {
    show(els.pageError, "На странице нет видеоплеера. Запусти ролик и открой popup снова.");
    els.btnDownload.disabled = true;
    return null;
  }

  videoInfo = info;
  els.start.value = secondsToTime(info.startSeconds);
  if (!els.end.value) {
    els.end.value = secondsToTime(info.startSeconds + Number(els.plusSeconds.value || 10));
  }
  if (!els.title.value) {
    els.title.value = info.suggestedFilename || "clip";
  }
  els.btnDownload.disabled = false;
  return info;
}

async function checkAppBridge() {
  try {
    const res = await fetch(`${APP_BRIDGE_URL}/health`, { method: "GET" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const info = await res.json();
    appBridgeOk = Boolean(info.ok && info.service === "yvp-app-bridge");
    bridgeInfo = info;
    return appBridgeOk;
  } catch {
    appBridgeOk = false;
    bridgeInfo = null;
    return false;
  }
}

function launchAppViaProtocol() {
  window.location.href = YVP_PROTOCOL_URL;
}

async function waitForAppBridge(timeoutMs = APP_LAUNCH_TIMEOUT_MS) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await checkAppBridge()) {
      return true;
    }
    await sleep(APP_LAUNCH_POLL_MS);
  }
  return false;
}

function showInstallPanel(reason) {
  const textEl = document.getElementById("install-text");
  if (textEl) {
    textEl.textContent = reason;
  }
  show(els.installPanel);
}

function hideInstallPanel() {
  hide(els.installPanel);
}

async function ensureAppRunning() {
  if (await checkAppBridge()) {
    hide(els.hostError);
    hideInstallPanel();
    return true;
  }

  appendLog("Приложение не отвечает — запускаю через yvp:// …");
  setStatus("Запуск приложения…");
  launchAppViaProtocol();

  if (await waitForAppBridge()) {
    hide(els.hostError);
    hideInstallPanel();
    appendLog("Приложение запущено.");
    return true;
  }

  show(
    els.hostError,
    "Не удалось запустить desktop-приложение. Если Chrome спрашивает «Открыть приложение?» — нажми Разрешить."
  );
  showInstallPanel(
    "Приложение не установлено или не отвечает. Скачай exe с GitHub и запусти windows\\install.bat (регистрирует yvp://)."
  );
  return false;
}

async function updateHostBanner() {
  if (await checkAppBridge()) {
    hide(els.hostError);
    return true;
  }

  hide(els.hostError);
  return false;
}

async function refreshStartFromPlayer() {
  const tab = await getActiveTab();
  if (!tab?.id) return;
  try {
    const info = await chrome.tabs.sendMessage(tab.id, { type: "GET_VIDEO_INFO" });
    if (info?.ok) {
      videoInfo = info;
      els.start.value = secondsToTime(info.startSeconds);
      setStatus("Начало обновлено с плеера");
    }
  } catch (err) {
    appendLog(`Ошибка обновления начала: ${err.message}`);
  }
}

function calcEndFromPlus() {
  try {
    const startSec = parseTimeToSeconds(els.start.value);
    const plus = Math.max(1, parseInt(els.plusSeconds.value, 10) || 0);
    let endSec = startSec + plus;
    if (videoInfo?.durationSeconds && endSec > videoInfo.durationSeconds) {
      endSec = Math.floor(videoInfo.durationSeconds);
    }
    els.end.value = secondsToTime(endSec);
    setStatus(`Конец = начало + ${plus} сек`);
  } catch (err) {
    appendLog(err.message);
    setStatus("Ошибка");
  }
}

function setBusy(busy) {
  els.btnDownload.disabled = busy;
  els.btnRefreshStart.disabled = busy;
  els.btnCalcEnd.disabled = busy;
}

async function pollAppJob(jobId) {
  const res = await fetch(`${APP_BRIDGE_URL}/jobs/${jobId}`);
  if (!res.ok) {
    throw new Error(`App bridge HTTP ${res.status}`);
  }
  const data = await res.json();

  if (Array.isArray(data.log)) {
    els.log.textContent = data.log.join("\n");
    if (data.log.length) {
      els.log.textContent += "\n";
    }
    els.log.scrollTop = els.log.scrollHeight;
  }

  if (data.status === "running") {
    setStatus("Загрузка…");
    return;
  }

  clearInterval(pollTimer);
  pollTimer = null;
  setBusy(false);

  if (data.status === "done") {
    setStatus("Готово");
    appendLog(`Сохранено: ${data.output_path || data.filename}`);
    return;
  }

  setStatus("Ошибка");
  appendLog(data.error || "Неизвестная ошибка");
}

async function downloadViaApp(payload) {
  const res = await fetch(`${APP_BRIDGE_URL}/clip`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }

  if (data.output_dir) {
    appendLog(`Папка: ${data.output_dir}`);
  }

  pollTimer = setInterval(() => {
    pollAppJob(data.job_id).catch((err) => {
      clearInterval(pollTimer);
      pollTimer = null;
      setBusy(false);
      setStatus("Ошибка");
      appendLog(err.message);
    });
  }, 500);
  await pollAppJob(data.job_id);
}

async function startDownload(event) {
  event.preventDefault();
  clearLog();
  hideInstallPanel();

  let start;
  let end;
  try {
    start = els.start.value.trim();
    end = els.end.value.trim();
    parseTimeToSeconds(start);
    parseTimeToSeconds(end);
    if (parseTimeToSeconds(end) <= parseTimeToSeconds(start)) {
      throw new Error("Конец должен быть позже начала");
    }
  } catch (err) {
    appendLog(err.message);
    setStatus("Ошибка");
    return;
  }

  if (!videoInfo?.url) {
    await loadVideoInfo();
  }
  if (!videoInfo?.url) {
    return;
  }

  setBusy(true);
  setStatus("Проверка приложения…");

  if (!(await ensureAppRunning())) {
    setStatus("Нужна установка");
    setBusy(false);
    return;
  }

  setStatus("Запуск…");

  if (bridgeInfo?.browser_download_dir) {
    appendLog(`Папка Chrome: ${bridgeInfo.browser_download_dir}`);
  }

  const payload = {
    url: videoInfo.url,
    start,
    end,
    title: els.title.value.trim(),
    use_browser_downloads: true,
  };

  try {
    await downloadViaApp(payload);
  } catch (err) {
    setStatus("Ошибка");
    appendLog(err.message);
  } finally {
    if (!pollTimer) {
      setBusy(false);
    }
  }
}

async function retryAfterInstall() {
  clearLog();
  setBusy(true);
  setStatus("Проверка…");
  hideInstallPanel();

  if (await ensureAppRunning()) {
    appendLog("Приложение доступно. Жми «Скачать отрезок».");
    setStatus("Готов");
  } else {
    setStatus("Всё ещё offline");
  }
  setBusy(false);
}

function openReleasesPage(event) {
  event.preventDefault();
  chrome.tabs.create({ url: GITHUB_RELEASES_URL });
}

els.btnRefreshStart.addEventListener("click", refreshStartFromPlayer);
els.btnCalcEnd.addEventListener("click", calcEndFromPlus);
els.form.addEventListener("submit", startDownload);
els.btnRetryApp.addEventListener("click", retryAfterInstall);
els.linkReleases.addEventListener("click", openReleasesPage);

(async function init() {
  setStatus("Готов");
  els.linkReleases.href = GITHUB_RELEASES_URL;
  await loadVideoInfo();
  await updateHostBanner();
})();
