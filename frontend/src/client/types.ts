export type ObjectType = 'PAYLOAD' | 'ROCKET_BODY' | 'DEBRIS';
export type OrbitType  = 'LEO' | 'MEO' | 'GEO' | 'HEO';

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
