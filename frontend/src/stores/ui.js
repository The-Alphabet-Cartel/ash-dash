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
 * UI Store - User interface state management (sidebar, layout preferences)
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-11-11.1-1
 * LAST MODIFIED: 2026-01-10
 * PHASE: Phase 11 - Polish & Documentation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineStore } from 'pinia'

// localStorage keys
const SIDEBAR_KEY = 'ash-dash-sidebar'

export const useUiStore = defineStore('ui', {
  state: () => ({
    // Sidebar state - default to expanded
    sidebarCollapsed: false,
    
    // Mobile sidebar visibility (for responsive design)
    mobileSidebarOpen: false,
  }),
  
  getters: {
    /**
     * Get sidebar width class for main content margin
     * @returns {string} Tailwind margin class
     */
    sidebarMarginClass: (state) => {
      return state.sidebarCollapsed ? 'ml-16' : 'ml-64'
    },
    
    /**
     * Get sidebar width in pixels
     * @returns {number} Width in pixels
     */
    sidebarWidth: (state) => {
      return state.sidebarCollapsed ? 64 : 256
    },
  },
  
  actions: {
    /**
     * Initialize UI state from localStorage
     * Called once on app startup
     */
    initUiState() {
      // Load sidebar preference
      const savedSidebar = localStorage.getItem(SIDEBAR_KEY)
      if (savedSidebar !== null) {
        this.sidebarCollapsed = savedSidebar === 'collapsed'
      }
    },
    
    /**
     * Toggle sidebar between collapsed and expanded states
     */
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
      localStorage.setItem(SIDEBAR_KEY, this.sidebarCollapsed ? 'collapsed' : 'expanded')
    },
    
    /**
     * Set sidebar to specific state
     * @param {boolean} collapsed - True to collapse, false to expand
     */
    setSidebarCollapsed(collapsed) {
      this.sidebarCollapsed = collapsed
      localStorage.setItem(SIDEBAR_KEY, collapsed ? 'collapsed' : 'expanded')
    },
    
    /**
     * Expand sidebar (convenience method)
     */
    expandSidebar() {
      this.setSidebarCollapsed(false)
    },
    
    /**
     * Collapse sidebar (convenience method)
     */
    collapseSidebar() {
      this.setSidebarCollapsed(true)
    },
    
    /**
     * Toggle mobile sidebar visibility
     */
    toggleMobileSidebar() {
      this.mobileSidebarOpen = !this.mobileSidebarOpen
    },
    
    /**
     * Close mobile sidebar
     */
    closeMobileSidebar() {
      this.mobileSidebarOpen = false
    },
    
    /**
     * Open mobile sidebar
     */
    openMobileSidebar() {
      this.mobileSidebarOpen = true
    },
  },
})
