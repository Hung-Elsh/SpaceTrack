export interface CooldownStatus {
  available: boolean;
  next_available_at: string | null;
  last_run_at: string | null;
}

export interface BackfillStatusResponse {
  tracked_objects: CooldownStatus;
  orbital_snapshots: CooldownStatus;
}

export interface PullCardConfig {
  key: keyof BackfillStatusResponse;
  buttonId: string;
  statusId: string;
  treeId: string;
  pullPath: string;
  loadDataPath: string;
}

function formatRemaining(ms: number): string {
  if (ms <= 0) return 'now';
  const totalMinutes = Math.ceil(ms / 60_000);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
}

function escapeHtml(value: string): string {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

function summarize(row: unknown): string {
  if (row && typeof row === 'object') {
    const obj = row as Record<string, unknown>;
    const label = obj['object_name'] ?? obj['name'] ?? obj['norad_id'] ?? obj['snapshot_date'] ?? obj['id'];
    return escapeHtml(String(label ?? 'row'));
  }
  return escapeHtml(String(row));
}

function renderTree(container: HTMLElement, rows: unknown): void {
  const list = Array.isArray(rows) ? rows : rows ? [rows] : [];
  if (list.length === 0) {
    container.innerHTML = '<p class="tree-empty">No data loaded yet.</p>';
    return;
  }
  container.innerHTML = `<ul class="tree-root">${list
    .map((row) => `<li class="tree-node"><details><summary>${summarize(row)}</summary><pre>${escapeHtml(
      JSON.stringify(row, null, 2)
    )}</pre></details></li>`)
    .join('')}</ul>`;
}

export function setupPullCard(config: PullCardConfig): void {
  const button = document.getElementById(config.buttonId) as HTMLButtonElement;
  const statusEl = document.getElementById(config.statusId) as HTMLElement;
  const treeEl = document.getElementById(config.treeId) as HTMLElement;

  async function loadData(): Promise<void> {
    try {
      const res = await fetch(config.loadDataPath);
      const data = res.ok ? await res.json() : null;
      renderTree(treeEl, data);
    } catch {
      treeEl.innerHTML = `<p class="tree-empty">Unable to load ${config.key}.</p>`;
    }
  }

  function applyStatus(status: CooldownStatus): void {
    if (status.available) {
      button.disabled = false;
      statusEl.textContent = status.last_run_at
        ? `Ready — last pulled ${new Date(status.last_run_at).toLocaleString()}`
        : 'Ready — never pulled yet';
    } else {
      button.disabled = true;
      const nextAt = status.next_available_at ? new Date(status.next_available_at) : null;
      const remaining = nextAt ? formatRemaining(nextAt.getTime() - Date.now()) : 'soon';
      statusEl.textContent = `On cooldown — available in ${remaining} (resets 00:00 UTC)`;
    }
  }

  async function refreshStatus(): Promise<void> {
    try {
      const res = await fetch('/api/backfill/status');
      if (!res.ok) throw new Error(`status ${res.status}`);
      const data: BackfillStatusResponse = await res.json();
      applyStatus(data[config.key]);
    } catch {
      statusEl.textContent = 'Unable to reach backend';
    }
  }

  async function handlePull(): Promise<void> {
    button.disabled = true;
    const originalLabel = button.textContent;
    button.textContent = 'Pulling…';

    try {
      const res = await fetch(config.pullPath, { method: 'POST' });
      const body = await res.json().catch(() => null);

      if (res.status === 429) {
        statusEl.textContent = body?.message ?? 'On cooldown.';
      } else if (!res.ok) {
        statusEl.textContent = body?.error ?? `Pull failed (${res.status})`;
      } else {
        const loaded = body?.records_loaded ?? '?';
        statusEl.textContent = `Pulled ${loaded} record(s).`;
        await loadData();
      }
    } catch {
      statusEl.textContent = 'Unable to reach backend.';
    } finally {
      button.textContent = originalLabel;
      await refreshStatus();
    }
  }

  button.addEventListener('click', () => handlePull());

  // --- Init ---
  refreshStatus();
  loadData();

  // Re-poll cooldown status periodically so the UI re-enables itself across the UTC-midnight
  // rollover without needing a page reload.
  window.setInterval(refreshStatus, 60_000);
}
