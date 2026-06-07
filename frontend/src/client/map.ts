import L from 'leaflet';
import type { Map as LeafletMap } from 'leaflet';
import type { SpaceObject } from './types';
import { ORBIT_COLORS } from './data';

export function initMap(
  container: HTMLElement,
  objects: SpaceObject[],
  onSelect: (obj: SpaceObject) => void,
): { render: (objs: SpaceObject[]) => void; map: LeafletMap } {
  const map = L.map(container, {
    center: [20, 10],
    zoom: 2,
    minZoom: 2,
    maxBoundsViscosity: 1.0,
    maxBounds: [[-90, -180], [90, 180]],
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
  }).addTo(map);

  const markersLayer = L.layerGroup().addTo(map);

  function render(objs: SpaceObject[]) {
    markersLayer.clearLayers();

    for (const obj of objs) {
      const color = ORBIT_COLORS[obj.orbitType] ?? '#ffffff';

      const marker = L.circleMarker([obj.lat, obj.lon], {
        radius: 9,
        fillColor: color,
        color: 'rgba(255,255,255,0.6)',
        weight: 1.5,
        opacity: 1,
        fillOpacity: 0.85,
      });

      marker.bindTooltip(obj.name, {
        permanent: false,
        direction: 'top',
        offset: [0, -8],
        className: 'st-tooltip',
      });

      marker.on('click', () => onSelect(obj));
      markersLayer.addLayer(marker);
    }
  }

  render(objects);

  return { render, map };
}
