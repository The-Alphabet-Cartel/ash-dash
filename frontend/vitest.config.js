/**
 * ============================================================================
 * Ash-DASH: Discord Crisis Detection Dashboard
 * The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
 * ============================================================================
 *
 * Vitest Configuration - Test runner setup
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-11-11.4-1
 * LAST MODIFIED: 2026-01-10
 * PHASE: Phase 11 - Polish & Documentation
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  
  test: {
    // Use happy-dom for faster DOM simulation
    environment: 'happy-dom',
    
    // Global test APIs (describe, it, expect)
    globals: true,
    
    // Setup files run before each test file
    setupFiles: ['./tests/setup.js'],
    
    // Test file patterns
    include: ['tests/**/*.test.js', 'tests/**/*.spec.js'],
    
    // Exclude patterns
    exclude: ['node_modules', 'dist'],
    
    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      reportsDirectory: './coverage',
      include: ['src/**/*.{js,vue}'],
      exclude: [
        'src/main.js',
        'src/**/*.d.ts',
        'src/**/index.js',
      ],
    },
    
    // Reporter for test results
    reporters: ['verbose'],
    
    // Timeout for each test (ms)
    testTimeout: 10000,
  },
})
