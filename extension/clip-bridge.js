// YVP Clipper — shared bridge to desktop app (popup + content)
// Copyright (C) 2026 NeyroslopInzh contributors
// SPDX-License-Identifier: GPL-3.0-or-later

const YVP_APP_BRIDGE_URL = "http://127.0.0.1:8766";
const YVP_PROTOCOL_URL = "yvp://start";
const YVP_APP_LAUNCH_TIMEOUT_MS = 15000;
const YVP_APP_LAUNCH_POLL_MS = 500;

function yvpSleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function yvpDirectHttp(url, init) {
  return fetch(url, init).then(async (res) => {
    const data = await res.json().catch(() => ({}));
    return { httpOk: res.ok, status: res.status, data };
  });
}

function yvpHttp(url, init) {
  const payload = { type: "YVP_HTTP", url, init: init || {} };
  if (typeof chrome === "undefined" || !chrome.runtime || !chrome.runtime.id) {
    return yvpDirectHttp(url, init);
  }
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(payload, (response) => {
      if (chrome.runtime.lastError) {
        yvpDirectHttp(url, init).then(resolve, reject);
        return;
      }
      if (response?.networkError) {
        reject(new Error(response.networkError));
        return;
      }
      resolve(response);
    });
  });
}

async function yvpCheckAppBridge() {
  try {
    const res = await yvpHttp(`${YVP_APP_BRIDGE_URL}/health`, { method: "GET" });
    if (!res.httpOk) throw new Error(`HTTP ${res.status}`);
    const info = res.data;
    if (info.ok && info.service === "yvp-app-bridge") {
      return info;
    }
    return null;
  } catch {
    return null;
  }
}

function yvpLaunchAppViaProtocol() {
  // Не location.href — иначе content script уедет со страницы YouTube
  let anchor = document.getElementById("yvp-protocol-launch");
  if (!anchor) {
    anchor = document.createElement("a");
    anchor.id = "yvp-protocol-launch";
    anchor.href = YVP_PROTOCOL_URL;
    anchor.style.display = "none";
    document.documentElement.appendChild(anchor);
  }
  anchor.click();
}

async function yvpWaitForAppBridge(timeoutMs = YVP_APP_LAUNCH_TIMEOUT_MS) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const info = await yvpCheckAppBridge();
    if (info) return info;
    await yvpSleep(YVP_APP_LAUNCH_POLL_MS);
  }
  return null;
}

async function yvpEnsureAppRunning() {
  // Protocol click must stay in the user-gesture turn (before any await).
  // Second instance exits immediately if the bridge is already up.
  yvpLaunchAppViaProtocol();
  const info = await yvpWaitForAppBridge();
  if (info) return { ok: true, info };

  return {
    ok: false,
    error:
      "Не удалось запустить desktop-приложение. Если браузер спрашивает «Открыть приложение?» — нажми Разрешить.",
  };
}

async function yvpStartClip(payload) {
  const res = await yvpHttp(`${YVP_APP_BRIDGE_URL}/clip`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = res.data || {};
  if (!res.httpOk) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

async function yvpFetchJob(jobId) {
  const res = await yvpHttp(`${YVP_APP_BRIDGE_URL}/jobs/${jobId}`, { method: "GET" });
  if (!res.httpOk) {
    throw new Error(`App bridge HTTP ${res.status}`);
  }
  return res.data;
}

/**
 * Poll job until done/error. onUpdate(job) each tick.
 * @returns {Promise<object>} final job
 */
async function yvpPollJob(jobId, onUpdate, intervalMs = 500) {
  for (;;) {
    const data = await yvpFetchJob(jobId);
    if (typeof onUpdate === "function") {
      onUpdate(data);
    }
    if (data.status === "running") {
      await yvpSleep(intervalMs);
      continue;
    }
    return data;
  }
}
