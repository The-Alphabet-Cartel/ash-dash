/**
 * ============================================================================
 * Ash-DASH: Discord Crisis Detection Dashboard
 * The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
 * ============================================================================
 *
 * MISSION - NEVER TO BE VIOLATED:
 *     Reveal   → Surface crisis alerts and user escalation patterns in real-time
 *     Enable   → Equip Crisis Response Teams with tools for swift intervention
 *     Clarify  → Translate detection data into actionable intelligence
 *     Protect  → Safeguard our LGBTQIA+ community through vigilant oversight
 *
 * ============================================================================
 * Vite Configuration - Build tool and dev server setup
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-3-3.1-1
 * LAST MODIFIED: 2026-01-07
 * PHASE: Phase 3 - Frontend Foundation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  
  server: {
    port: 3000,
    proxy: {
      // Proxy API requests to FastAPI backend during development
      '/api': {
        target: 'http://localhost:30883',
        changeOrigin: true,
        secure: false,
      },
      // Proxy auth requests
      '/auth': {
        target: 'http://localhost:30883',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    // Optimize for production
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'icons': ['lucide-vue-next'],
        },
      },
    },
  },
})
