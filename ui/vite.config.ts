import { defineConfig } from 'vite';

export default defineConfig({
  optimizeDeps: {
    include: ['leaflet', 'globe.gl'],
  },
});
