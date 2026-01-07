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
 * Theme Store - Dark/Light mode state management with localStorage persistence
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-3-3.1-1
 * LAST MODIFIED: 2026-01-07
 * PHASE: Phase 3 - Frontend Foundation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineStore } from 'pinia'

const STORAGE_KEY = 'ash-dash-theme'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    // Default to dark mode - CRT members may respond at night
    isDark: true,
  }),
  
  getters: {
    /**
     * Get current theme mode string
     */
    currentTheme: (state) => state.isDark ? 'dark' : 'light',
  },
  
  actions: {
    /**
     * Initialize theme from localStorage or default to dark
     */
    initTheme() {
      const saved = localStorage.getItem(STORAGE_KEY)
      
      if (saved !== null) {
        this.isDark = saved === 'dark'
      } else {
        // Default to dark mode for CRT comfort during night responses
        this.isDark = true
      }
      
      this.applyTheme()
    },
    
    /**
     * Toggle between dark and light mode
     */
    toggleTheme() {
      this.isDark = !this.isDark
      localStorage.setItem(STORAGE_KEY, this.isDark ? 'dark' : 'light')
      this.applyTheme()
    },
    
    /**
     * Set specific theme mode
     * @param {boolean} dark - True for dark mode, false for light
     */
    setTheme(dark) {
      this.isDark = dark
      localStorage.setItem(STORAGE_KEY, this.isDark ? 'dark' : 'light')
      this.applyTheme()
    },
    
    /**
     * Apply theme class to document element
     */
    applyTheme() {
      if (this.isDark) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
  },
})
