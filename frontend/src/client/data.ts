import type { SpaceObject, TodaySnapshotApiRow } from './types';

export const ORBIT_COLORS: Record<string, string> = {
  LEO: '#4fc3f7',
  MEO: '#81c784',
  GEO: '#ffb74d',
  HEO: '#e57373',
};

export const COUNTRY_FLAG: Record<string, string> = {
  USA: '🇺🇸',
  RUS: '🇷🇺',
  CHN: '🇨🇳',
  ISS: '🌍',
  ESA: '🇪🇺',
  JPN: '🇯🇵',
  IND: '🇮🇳',
};

function toSpaceObject(row: TodaySnapshotApiRow): SpaceObject {
  return {
    id: String(row.id),
    name: row.name ?? `NORAD ${row.norad_id}`,
    noradId: row.norad_id,
    type: row.type,
    country: row.country ?? 'UNK',
    launchDate: row.launch_date ?? '',
    lat: row.lat,
    lon: row.lon,
    altitudeKm: row.altitude_km,
    orbitType: row.orbit_type,
    inclination: row.inclination,
    periodMin: row.period_min,
    description: `${row.type} object in ${row.orbit_type} orbit, tracked from today's orbital_snapshots pull.`,
  };
}

export async function fetchSpaceObjects(): Promise<SpaceObject[]> {
  const res = await fetch('/api/snapshot/today');
  if (!res.ok) throw new Error(`snapshot/today ${res.status}`);
  const rows: TodaySnapshotApiRow[] = await res.json();
  return rows.map(toSpaceObject);
}
