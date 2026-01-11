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
 * Vite Configuration - Build optimization and dev server setup
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-11-11.3-1
 * LAST MODIFIED: 2026-01-10
 * PHASE: Phase 11 - Polish & Documentation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 * 
 * PERFORMANCE OPTIMIZATIONS:
 *   - Manual chunk splitting for vendor, icons, and editor libraries
 *   - Tree-shaking enabled for production builds
 *   - CSS code splitting
 *   - Asset hashing for cache busting
 *   - Chunk size warnings at 500KB
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
      // Proxy health endpoints
      '/health': {
        target: 'http://localhost:30883',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    
    // Source maps only in development
    sourcemap: false,
    
    // Warn if chunks exceed 500KB
    chunkSizeWarningLimit: 500,
    
    // CSS code splitting
    cssCodeSplit: true,
    
    // Minification settings
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // Remove console.log in production
        drop_debugger: true, // Remove debugger statements
      },
    },
    
    // Rollup optimization settings
    rollupOptions: {
      output: {
        // Manual chunk splitting for optimal caching
        manualChunks: (id) => {
          // Core Vue framework
          if (id.includes('node_modules/vue') || 
              id.includes('node_modules/@vue') ||
              id.includes('node_modules/vue-router') ||
              id.includes('node_modules/pinia')) {
            return 'vendor-vue'
          }
          
          // Icons library (large, rarely changes)
          if (id.includes('node_modules/lucide-vue-next')) {
            return 'vendor-icons'
          }
          
          // TipTap editor (heavy, only used in session detail)
          if (id.includes('node_modules/@tiptap') || 
              id.includes('node_modules/prosemirror')) {
            return 'vendor-editor'
          }
          
          // Chart libraries
          if (id.includes('node_modules/chart.js') ||
              id.includes('node_modules/vue-chartjs')) {
            return 'vendor-charts'
          }
          
          // Other node_modules
          if (id.includes('node_modules')) {
            return 'vendor-misc'
          }
        },
        
        // Asset file naming with hash for cache busting
        assetFileNames: (assetInfo) => {
          // CSS files
          if (assetInfo.name?.endsWith('.css')) {
            return 'assets/css/[name]-[hash][extname]'
          }
          // Images
          if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(assetInfo.name || '')) {
            return 'assets/images/[name]-[hash][extname]'
          }
          // Fonts
          if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name || '')) {
            return 'assets/fonts/[name]-[hash][extname]'
          }
          // Default
          return 'assets/[name]-[hash][extname]'
        },
        
        // Chunk file naming
        chunkFileNames: 'assets/js/[name]-[hash].js',
        
        // Entry file naming
        entryFileNames: 'assets/js/[name]-[hash].js',
      },
    },
  },
  
  // Optimize dependency pre-bundling
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      'lucide-vue-next',
    ],
  },
})
