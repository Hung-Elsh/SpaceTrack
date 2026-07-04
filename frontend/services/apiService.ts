import dotenv from 'dotenv';
dotenv.config();

// Flask blueprints are all registered under /api (see backend/app/__init__.py)
const API_BASE = (process.env.FLASK_API_URL ?? 'http://localhost:5000') + '/api';

export interface ProxyResult {
  status: number;
  body: unknown;
}

async function proxyJson(url: string, init?: RequestInit): Promise<ProxyResult> {
  const res = await fetch(url, init);
  const body = await res.json().catch(() => null);
  return { status: res.status, body };
}

export async function fetchObjects(params?: Record<string, string>): Promise<unknown> {
  const query = params && Object.keys(params).length ? '?' + new URLSearchParams(params).toString() : '';
  const res = await fetch(`${API_BASE}/objects${query}`);
  if (!res.ok) throw new Error(`Flask API ${res.status}`);
  return res.json();
}

export async function fetchObjectDetail(noradId: string): Promise<unknown> {
  const res = await fetch(`${API_BASE}/objects/${noradId}`);
  if (!res.ok) throw new Error(`Flask API ${res.status}`);
  return res.json();
}

export async function fetchSnapshotDates(): Promise<unknown> {
  const res = await fetch(`${API_BASE}/snapshot/dates`);
  if (!res.ok) throw new Error(`Flask API ${res.status}`);
  return res.json();
}

export async function fetchTodaySnapshots(): Promise<unknown> {
  const res = await fetch(`${API_BASE}/snapshot/today`);
  if (!res.ok) throw new Error(`Flask API ${res.status}`);
  return res.json();
}

// --- Proactive pull APIs (status-code-aware — the caller relays 200/429/etc as-is) ---

export async function pullObjects(): Promise<ProxyResult> {
  return proxyJson(`${API_BASE}/objects`, { method: 'POST' });
}

export async function pullSnapshots(): Promise<ProxyResult> {
  return proxyJson(`${API_BASE}/snapshot`, { method: 'POST' });
}

export async function fetchBackfillStatus(): Promise<ProxyResult> {
  return proxyJson(`${API_BASE}/backfill/status`);
}
