"use strict";
(() => {
  // src/client/pullShared.ts
  function formatRemaining(ms) {
    if (ms <= 0) return "now";
    const totalMinutes = Math.ceil(ms / 6e4);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
  }
  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
  }
  function summarize(row) {
    if (row && typeof row === "object") {
      const obj = row;
      const label = obj["object_name"] ?? obj["name"] ?? obj["norad_id"] ?? obj["snapshot_date"] ?? obj["id"];
      return escapeHtml(String(label ?? "row"));
    }
    return escapeHtml(String(row));
  }
  function renderTree(container, rows) {
    const list = Array.isArray(rows) ? rows : rows ? [rows] : [];
    if (list.length === 0) {
      container.innerHTML = '<p class="tree-empty">No data loaded yet.</p>';
      return;
    }
    container.innerHTML = `<ul class="tree-root">${list.map((row) => `<li class="tree-node"><details><summary>${summarize(row)}</summary><pre>${escapeHtml(
      JSON.stringify(row, null, 2)
    )}</pre></details></li>`).join("")}</ul>`;
  }
  function setupPullCard(config) {
    const button = document.getElementById(config.buttonId);
    const statusEl = document.getElementById(config.statusId);
    const treeEl = document.getElementById(config.treeId);
    async function loadData() {
      try {
        const res = await fetch(config.loadDataPath);
        const data = res.ok ? await res.json() : null;
        renderTree(treeEl, data);
      } catch {
        treeEl.innerHTML = `<p class="tree-empty">Unable to load ${config.key}.</p>`;
      }
    }
    function applyStatus(status) {
      if (status.available) {
        button.disabled = false;
        statusEl.textContent = status.last_run_at ? `Ready \u2014 last pulled ${new Date(status.last_run_at).toLocaleString()}` : "Ready \u2014 never pulled yet";
      } else {
        button.disabled = true;
        const nextAt = status.next_available_at ? new Date(status.next_available_at) : null;
        const remaining = nextAt ? formatRemaining(nextAt.getTime() - Date.now()) : "soon";
        statusEl.textContent = `On cooldown \u2014 available in ${remaining} (resets 00:00 UTC)`;
      }
    }
    async function refreshStatus() {
      try {
        const res = await fetch("/api/backfill/status");
        if (!res.ok) throw new Error(`status ${res.status}`);
        const data = await res.json();
        applyStatus(data[config.key]);
      } catch {
        statusEl.textContent = "Unable to reach backend";
      }
    }
    async function handlePull() {
      button.disabled = true;
      const originalLabel = button.textContent;
      button.textContent = "Pulling\u2026";
      try {
        const res = await fetch(config.pullPath, { method: "POST" });
        const body = await res.json().catch(() => null);
        if (res.status === 429) {
          statusEl.textContent = body?.message ?? "On cooldown.";
        } else if (!res.ok) {
          statusEl.textContent = body?.error ?? `Pull failed (${res.status})`;
        } else {
          const loaded = body?.records_loaded ?? "?";
          statusEl.textContent = `Pulled ${loaded} record(s).`;
          await loadData();
        }
      } catch {
        statusEl.textContent = "Unable to reach backend.";
      } finally {
        button.textContent = originalLabel;
        await refreshStatus();
      }
    }
    button.addEventListener("click", () => handlePull());
    refreshStatus();
    loadData();
    window.setInterval(refreshStatus, 6e4);
  }

  // src/client/objectsPage.ts
  setupPullCard({
    key: "tracked_objects",
    buttonId: "btn-pull-objects",
    statusId: "status-objects",
    treeId: "tree-objects",
    pullPath: "/api/objects",
    loadDataPath: "/api/objects"
  });
})();
