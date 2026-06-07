import dotenv from 'dotenv';
dotenv.config();

const API_BASE = process.env.FLASK_API_URL ?? 'http://localhost:5000';

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
