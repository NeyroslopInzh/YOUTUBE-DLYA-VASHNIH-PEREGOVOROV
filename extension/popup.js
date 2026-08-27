// YVP Clipper — Chromium extension → desktop app bridge
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later

const GITHUB_RELEASES_URL =
  "https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases/latest";

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
let pollActive = false;
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
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["time.js", "clip-bridge.js", "clip-ui.js", "content.js"],
      });
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
  const result = await yvpEnsureAppRunning();
  if (result.ok) {
    bridgeInfo = result.info;
    hide(els.hostError);
    hideInstallPanel();
    return true;
  }

  show(
    els.hostError,
    result.error ||
      "Не удалось запустить desktop-приложение. Если Chrome спрашивает «Открыть приложение?» — нажми Разрешить."
  );
  showInstallPanel(
    "Приложение не установлено или не отвечает. Скачай exe с GitHub и запусти windows\\install.bat (регистрирует yvp://)."
  );
  return false;
}

async function updateHostBanner() {
  const info = await yvpCheckAppBridge();
  if (info) {
    bridgeInfo = info;
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

async function downloadViaApp(payload) {
  const started = await yvpStartClip(payload);
  if (started.output_dir) {
    appendLog(`Папка: ${started.output_dir}`);
  }

  pollActive = true;
  const job = await yvpPollJob(started.job_id, (data) => {
    if (Array.isArray(data.log)) {
      els.log.textContent = data.log.join("\n");
      if (data.log.length) {
        els.log.textContent += "\n";
      }
      els.log.scrollTop = els.log.scrollHeight;
    }
    if (data.status === "running") {
      setStatus("Загрузка…");
    }
  });
  pollActive = false;
  setBusy(false);

  if (job.status === "done") {
    setStatus("Готово");
    appendLog(`Сохранено: ${job.output_path || job.filename}`);
    return;
  }

  setStatus("Ошибка");
  appendLog(job.error || "Неизвестная ошибка");
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
    pollActive = false;
    setStatus("Ошибка");
    appendLog(err.message);
    setBusy(false);
  } finally {
    if (!pollActive) {
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
