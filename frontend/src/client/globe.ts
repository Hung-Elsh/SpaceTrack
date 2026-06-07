import Globe from 'globe.gl';
import type { SpaceObject } from './types';
import { ORBIT_COLORS } from './data';

export function initGlobe(
  container: HTMLElement,
  objects: SpaceObject[],
  onSelect: (obj: SpaceObject) => void,
): { render: (objs: SpaceObject[]) => void } {
  const globe = new Globe(container);

  globe
    .width(container.clientWidth)
    .height(container.clientHeight)
    .backgroundColor('#0a0a0f')
    .showAtmosphere(true)
    .atmosphereColor('#1e4d8c')
    .atmosphereAltitude(0.18)
    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg');

  function visualAltitude(km: number): number {
    if (km < 2000)  return 0.08;
    if (km < 35000) return 0.32;
    return 0.62;
  }

  function render(objs: SpaceObject[]) {
    globe
      .pointsData(objs)
      .pointLat('lat')
      .pointLng('lon')
      .pointColor((d: object) => ORBIT_COLORS[(d as SpaceObject).orbitType] ?? '#ffffff')
      .pointAltitude((d: object) => visualAltitude((d as SpaceObject).altitudeKm))
      .pointRadius(0.45)
      .pointLabel((d: object) => {
        const o = d as SpaceObject;
        return `<div style="padding:4px 8px;background:rgba(10,10,15,0.85);border:1px solid #333;border-radius:4px;font-size:12px">
          <b style="color:#e0e0f0">${o.name}</b><br/>
          <span style="color:#7070a0">${o.orbitType} · ${o.altitudeKm.toLocaleString()} km</span>
        </div>`;
      })
      .onPointClick((d: object) => onSelect(d as SpaceObject));
  }

  render(objects);

  window.addEventListener('resize', () => {
    globe.width(container.clientWidth).height(container.clientHeight);
  });

  return { render };
}
