import { fetchSpaceObjects, ORBIT_COLORS, COUNTRY_FLAG } from './data';
import { initGlobe } from './globe';
import { initMap } from './map';
import type { SpaceObject } from './types';

// --- DOM refs ---
const globeContainer = document.getElementById('globe-view') as HTMLElement;
const mapContainer   = document.getElementById('map-view')   as HTMLElement;
const btnGlobe       = document.getElementById('btn-globe')  as HTMLButtonElement;
const btnMap         = document.getElementById('btn-map')    as HTMLButtonElement;
const sidebar        = document.getElementById('sidebar')    as HTMLElement;
const sidebarContent = document.getElementById('sidebar-content') as HTMLElement;
const sidebarClose   = document.getElementById('sidebar-close')   as HTMLButtonElement;
const objectCount    = document.getElementById('object-count')    as HTMLElement;
const filterCbs      = document.querySelectorAll<HTMLInputElement>('#filter-panel input[type="checkbox"]');

// --- State ---
const activeOrbits = new Set<string>(['LEO', 'MEO', 'GEO', 'HEO']);
let spaceObjects: SpaceObject[] = [];

function filtered(): SpaceObject[] {
  return spaceObjects.filter(o => activeOrbits.has(o.orbitType));
}

// --- Sidebar ---
function showSidebar(obj: SpaceObject) {
  const flag  = COUNTRY_FLAG[obj.country] ?? '🛰️';
  const color = ORBIT_COLORS[obj.orbitType];

  sidebarContent.innerHTML = `
    <div class="obj-header">
      <span class="obj-flag">${flag}</span>
      <div>
        <div class="obj-name">${obj.name}</div>
        <div class="obj-norad">NORAD #${obj.noradId}</div>
      </div>
    </div>
    <div class="obj-badges">
      <span class="obj-badge" style="background:${color}">${obj.orbitType}</span>
      <span class="obj-badge obj-badge-dim">${obj.type}</span>
    </div>
    <p class="obj-desc">${obj.description}</p>
    <table class="obj-table">
      <tr><td>Altitude</td>    <td>${obj.altitudeKm.toLocaleString()} km</td></tr>
      <tr><td>Inclination</td> <td>${obj.inclination}°</td></tr>
      <tr><td>Period</td>      <td>${obj.periodMin} min</td></tr>
      <tr><td>Country</td>     <td>${obj.country}</td></tr>
      <tr><td>Launch date</td> <td>${obj.launchDate}</td></tr>
      <tr><td>Position</td>    <td>${obj.lat.toFixed(2)}°, ${obj.lon.toFixed(2)}°</td></tr>
    </table>
  `;

  sidebar.classList.remove('hidden');
}

sidebarClose.addEventListener('click', () => sidebar.classList.add('hidden'));

// --- Init views ---
async function init(): Promise<void> {
  try {
    spaceObjects = await fetchSpaceObjects();
  } catch {
    objectCount.textContent = 'Unable to load data';
    spaceObjects = [];
  }

  const globe                              = initGlobe(globeContainer, filtered(), showSidebar);
  const { render: renderMap, map: leaflet } = initMap(mapContainer, filtered(), showSidebar);

  // Seed object count on load
  objectCount.textContent = `${filtered().length} objects`;

  // --- View toggle ---
  function switchView(view: 'globe' | 'map') {
    if (view === 'globe') {
      globeContainer.classList.remove('hidden');
      mapContainer.classList.add('hidden');
      btnGlobe.classList.add('active');
      btnMap.classList.remove('active');
    } else {
      mapContainer.classList.remove('hidden');
      globeContainer.classList.add('hidden');
      btnMap.classList.add('active');
      btnGlobe.classList.remove('active');
      leaflet.invalidateSize();
    }
  }

  btnGlobe.addEventListener('click', () => switchView('globe'));
  btnMap.addEventListener('click',   () => switchView('map'));

  // --- Filters ---
  filterCbs.forEach(cb => {
    cb.addEventListener('change', () => {
      const orbit = cb.dataset['orbit']!;
      if (cb.checked) activeOrbits.add(orbit);
      else             activeOrbits.delete(orbit);

      const objs = filtered();
      objectCount.textContent = `${objs.length} object${objs.length !== 1 ? 's' : ''}`;
      globe.render(objs);
      renderMap(objs);
    });
  });
}

init();
