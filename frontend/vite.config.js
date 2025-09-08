// vite.config.js (in your frontend/ directory)
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,         // Vite's default dev server port
    strictPort: true,   // Ensures port is available or errors
    host: '0.0.0.0',    // Allows access from host machine
    proxy: {
      '/api': { // All requests starting with /api will be proxied
        target: 'https://backend:8443', // Target your backend service by its Docker Compose name and HTTPS port
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false,      // CRITICAL: Allows connection to self-signed HTTPS backend in dev
        ws: true,           // Enable WebSocket proxying (for Socket.IO)
      },
    },
  },
})
