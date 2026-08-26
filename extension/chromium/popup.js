// YVP Clipper — Chromium extension
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later
// See ../../LICENSE

const COMPANION_URL = "http://127.0.0.1:8765";

const els = {
  pageError: document.getElementById("page-error"),
  companionError: document.getElementById("companion-error"),
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
  el.textContent = text;
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
  if (!tab?.id || !tab.url?.includes("youtube.com/watch") && !tab.url?.includes("youtu.be/")) {
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

async function checkCompanion() {
  try {
    const res = await fetch(`${COMPANION_URL}/health`, { method: "GET" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const info = await res.json();
    hide(els.companionError);
    if (!info.temp_root) {
      show(
        els.companionError,
        "Companion устарел — закрой и перезапусти extension/companion/run.bat."
      );
      return false;
    }
    return true;
  } catch {
    show(
      els.companionError,
      "Companion не запущен. В терминале: extension/companion/run.bat (Windows) или ./run.sh (Linux)."
    );
    return false;
  }
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

function basenameOnly(name) {
  const raw = String(name || "clip").trim() || "clip";
  const base = raw.replace(/[/\\]/g, "_").replace(/[<>:"|?*]/g, "_");
  return base.toLowerCase().endsWith(".mp4") ? base : `${base}.mp4`;
}

async function triggerBrowserDownload(jobId, filename) {
  const res = await fetch(`${COMPANION_URL}/jobs/${jobId}/file`);
  if (!res.ok) {
    throw new Error(`Companion не отдал файл (HTTP ${res.status})`);
  }

  const blob = await res.blob();
  const blobUrl = URL.createObjectURL(blob);
  const safeName = basenameOnly(filename);

  try {
    const downloadId = await new Promise((resolve, reject) => {
      chrome.downloads.download(
        {
          url: blobUrl,
          filename: safeName,
          saveAs: false,
          conflictAction: "uniquify",
        },
        (id) => {
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message));
            return;
          }
          if (id === undefined) {
            reject(new Error("Браузер не начал скачивание"));
            return;
          }
          resolve(id);
        }
      );
    });
    return { downloadId, safeName };
  } finally {
    setTimeout(() => URL.revokeObjectURL(blobUrl), 60_000);
  }
}

async function pollJob(jobId) {
  const res = await fetch(`${COMPANION_URL}/jobs/${jobId}`);
  if (!res.ok) {
    throw new Error(`Companion HTTP ${res.status}`);
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
    setStatus("Скачивание…");
    try {
      const { safeName } = await triggerBrowserDownload(
        jobId,
        data.filename || els.title.value.trim()
      );
      setStatus("Готово");
      appendLog(`Chrome сохраняет: ${safeName}`);
      appendLog("Папка — из chrome://settings/downloads (у тебя D:\\Downloads1).");
    } catch (err) {
      setStatus("Ошибка");
      appendLog(`Не удалось скачать через браузер: ${err.message}`);
    }
    return;
  }

  setStatus("Ошибка");
  appendLog(data.error || "Неизвестная ошибка");
}

async function startDownload(event) {
  event.preventDefault();
  clearLog();

  if (!(await checkCompanion())) {
    setStatus("Companion offline");
    return;
  }

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
  setStatus("Запуск…");

  const payload = {
    url: videoInfo.url,
    start,
    end,
    title: els.title.value.trim(),
  };

  try {
    const res = await fetch(`${COMPANION_URL}/clip`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || `HTTP ${res.status}`);
    }

    pollTimer = setInterval(() => {
      pollJob(data.job_id).catch((err) => {
        clearInterval(pollTimer);
        pollTimer = null;
        setBusy(false);
        setStatus("Ошибка");
        appendLog(err.message);
      });
    }, 500);
    await pollJob(data.job_id);
  } catch (err) {
    setBusy(false);
    setStatus("Ошибка");
    appendLog(err.message);
  }
}

els.btnRefreshStart.addEventListener("click", refreshStartFromPlayer);
els.btnCalcEnd.addEventListener("click", calcEndFromPlus);
els.form.addEventListener("submit", startDownload);

(async function init() {
  setStatus("Готов");
  await loadVideoInfo();
  await checkCompanion();
})();
