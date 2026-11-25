import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  server: { proxy: { '/api': 'http://127.0.0.1:8080' } },
  preview: { proxy: { '/api': 'http://127.0.0.1:8080' } },
  plugins: [react(), tailwindcss(), VitePWA({
    registerType: 'autoUpdate',
    includeAssets: ['favicon.svg', 'icons/*.png'],
    manifest: {
      name: 'FoodBridge – Surplus Food Rescue', short_name: 'FoodBridge',
      description: 'Share good food. Build a kinder community. Frontend demo.',
      theme_color: '#246B45', background_color: '#FAF6EF', display: 'standalone',
      start_url: '/', scope: '/',
      icons: [{ src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' }, { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' }, { src: '/icons/maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }]
    },
    workbox: { globPatterns: ['**/*.{js,css,html,svg,png,woff2}'], navigateFallback: '/index.html', navigateFallbackDenylist: [/^\/api(?:\/|$)/], runtimeCaching: [{ urlPattern: /^https:\/\/images\.unsplash\.com\//, handler: 'CacheFirst', options: { cacheName: 'food-photography', expiration: { maxEntries: 40, maxAgeSeconds: 2592000 }, cacheableResponse: { statuses: [0, 200] } } }] }
  })],
})
