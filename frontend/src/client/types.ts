export type ObjectType = 'PAYLOAD' | 'ROCKET BODY' | 'DEBRIS' | 'UNKNOWN';
export type OrbitType  = 'LEO' | 'MEO' | 'GEO' | 'HEO';

export interface TodaySnapshotApiRow {
  id: number;
  name: string | null;
  norad_id: number;
  type: ObjectType;
  country: string | null;
  launch_date: string | null;
  lat: number;
  lon: number;
  altitude_km: number;
  orbit_type: OrbitType;
  inclination: number;
  period_min: number;
}

export interface SpaceObject {
  id: string;
  name: string;
  noradId: number;
  type: ObjectType;
  country: string;
  launchDate: string;
  lat: number;
  lon: number;
  altitudeKm: number;
  orbitType: OrbitType;
  inclination: number;
  periodMin: number;
  description: string;
}
