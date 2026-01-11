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
 * Dashboard Store - Pinia state management for dashboard data and polling
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-4-4.2-1
 * LAST MODIFIED: 2026-01-07
 * PHASE: Phase 4 - Dashboard & Metrics
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 *
 * POLLING STRATEGY:
 *   - Active Sessions: 10 second interval (real-time critical)
 *   - Metrics/Charts: 30 second interval (aggregated data)
 *
 * USAGE:
 *   import { useDashboardStore } from '@/stores/dashboard'
 *   const dashboard = useDashboardStore()
 *   
 *   // Start polling on component mount
 *   onMounted(() => dashboard.startPolling())
 *   
 *   // Stop polling on component unmount
 *   onUnmounted(() => dashboard.stopPolling())
 */

import { defineStore } from 'pinia'
import { dashboardApi } from '@/services/api'

// =============================================================================
// Constants
// =============================================================================

/** Polling interval for active sessions (ms) - updates frequently for real-time feel */
const SESSIONS_POLL_INTERVAL = 10000 // 10 seconds

/** Polling interval for metrics and charts (ms) - less frequent for aggregated data */
const METRICS_POLL_INTERVAL = 30000 // 30 seconds

// =============================================================================
// Dashboard Store
// =============================================================================

export const useDashboardStore = defineStore('dashboard', {
  // ===========================================================================
  // State
  // ===========================================================================
  state: () => ({
    // Data
    metrics: null,
    crisisTrends: [],
    crtActivity: [],
    activeSessions: [],

    // Loading states
    isLoading: false,
    isLoadingMetrics: false,
    isLoadingSessions: false,
    isLoadingTrends: false,
    isLoadingActivity: false,

    // Error handling
    error: null,
    lastError: null,

    // Polling state
    pollIntervals: {
      metrics: null,
      sessions: null,
    },
    isPolling: false,

    // Timestamps
    lastUpdated: null,
    lastSessionsUpdate: null,
  }),

  // ===========================================================================
  // Getters
  // ===========================================================================
  getters: {
    /**
     * Count of active sessions
     */
    activeSessionCount: (state) => state.activeSessions.length,

    /**
     * Count of critical + high severity active sessions
     */
    criticalHighCount: (state) => {
      return state.activeSessions.filter(
        s => s.severity === 'critical' || s.severity === 'high'
      ).length
    },

    /**
     * Check if any critical sessions exist
     */
    hasCriticalSessions: (state) => {
      return state.activeSessions.some(s => s.severity === 'critical')
    },

    /**
     * Sessions grouped by severity
     */
    sessionsBySeverity: (state) => {
      const groups = {
        critical: [],
        high: [],
        medium: [],
        low: [],
      }
      state.activeSessions.forEach(session => {
        if (groups[session.severity]) {
          groups[session.severity].push(session)
        }
      })
      return groups
    },

    /**
     * Formatted last updated time
     */
    lastUpdatedFormatted: (state) => {
      if (!state.lastUpdated) return 'Never'
      const now = new Date()
      const diff = now - state.lastUpdated
      if (diff < 5000) return 'Just now'
      if (diff < 60000) return `${Math.floor(diff / 1000)}s ago`
      if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
      return state.lastUpdated.toLocaleTimeString()
    },

    /**
     * Check if there are any errors
     */
    hasError: (state) => state.error !== null,
  },

  // ===========================================================================
  // Actions
  // ===========================================================================
  actions: {
    // -------------------------------------------------------------------------
    // Data Fetching
    // -------------------------------------------------------------------------

    /**
     * Fetch aggregated metrics for dashboard cards
     */
    async fetchMetrics() {
      this.isLoadingMetrics = true
      try {
        const response = await dashboardApi.getMetrics()
        this.metrics = response.data
        this.clearError()
      } catch (error) {
        this.setError('Failed to fetch metrics', error)
      } finally {
        this.isLoadingMetrics = false
      }
    },

    /**
     * Fetch active sessions for real-time display
     */
    async fetchActiveSessions() {
      this.isLoadingSessions = true
      try {
        const response = await dashboardApi.getActiveSessions()
        this.activeSessions = response.data || []
        this.lastSessionsUpdate = new Date()
        this.clearError()
      } catch (error) {
        this.setError('Failed to fetch active sessions', error)
      } finally {
        this.isLoadingSessions = false
      }
    },

    /**
     * Fetch crisis trend data for chart
     * @param {number} days - Number of days to fetch (default: 30)
     */
    async fetchCrisisTrends(days = 30) {
      this.isLoadingTrends = true
      try {
        const response = await dashboardApi.getCrisisTrends(days)
        this.crisisTrends = response.data || []
        this.clearError()
      } catch (error) {
        this.setError('Failed to fetch crisis trends', error)
      } finally {
        this.isLoadingTrends = false
      }
    },

    /**
     * Fetch CRT member activity statistics
     * @param {number} days - Number of days to analyze (default: 7)
     */
    async fetchCRTActivity(days = 7) {
      this.isLoadingActivity = true
      try {
        const response = await dashboardApi.getCRTActivity(days)
        this.crtActivity = response.data || []
        this.clearError()
      } catch (error) {
        this.setError('Failed to fetch CRT activity', error)
      } finally {
        this.isLoadingActivity = false
      }
    },

    /**
     * Fetch all dashboard data at once
     * Used for initial load and manual refresh
     */
    async fetchAll() {
      this.isLoading = true
      this.error = null

      try {
        // Fetch all data in parallel
        await Promise.all([
          this.fetchMetrics(),
          this.fetchActiveSessions(),
          this.fetchCrisisTrends(),
          this.fetchCRTActivity(),
        ])
        this.lastUpdated = new Date()
      } catch (error) {
        // Individual fetch methods handle their own errors
        console.error('Error fetching dashboard data:', error)
      } finally {
        this.isLoading = false
      }
    },

    // -------------------------------------------------------------------------
    // Polling Management
    // -------------------------------------------------------------------------

    /**
     * Start polling for dashboard data
     * Uses dual intervals: fast for sessions, slower for aggregated data
     * 
     * @param {number} metricsInterval - Interval for metrics/charts in ms (default: 30000)
     * @param {number} sessionsInterval - Interval for active sessions in ms (default: 10000)
     */
    startPolling(
      metricsInterval = METRICS_POLL_INTERVAL,
      sessionsInterval = SESSIONS_POLL_INTERVAL
    ) {
      // Don't start if already polling
      if (this.isPolling) {
        console.warn('Dashboard polling already active')
        return
      }

      // Initial fetch
      this.fetchAll()

      // Set up metrics/charts polling (slower interval)
      this.pollIntervals.metrics = setInterval(() => {
        this.fetchMetrics()
        this.fetchCrisisTrends()
        this.fetchCRTActivity()
        this.lastUpdated = new Date()
      }, metricsInterval)

      // Set up active sessions polling (faster interval)
      this.pollIntervals.sessions = setInterval(() => {
        this.fetchActiveSessions()
      }, sessionsInterval)

      this.isPolling = true
      console.log('Dashboard polling started')
    },

    /**
     * Stop all polling intervals
     * IMPORTANT: Call this when unmounting the dashboard component
     */
    stopPolling() {
      if (this.pollIntervals.metrics) {
        clearInterval(this.pollIntervals.metrics)
        this.pollIntervals.metrics = null
      }

      if (this.pollIntervals.sessions) {
        clearInterval(this.pollIntervals.sessions)
        this.pollIntervals.sessions = null
      }

      this.isPolling = false
      console.log('Dashboard polling stopped')
    },

    /**
     * Restart polling (useful after reconnection)
     */
    restartPolling() {
      this.stopPolling()
      this.startPolling()
    },

    // -------------------------------------------------------------------------
    // Error Handling
    // -------------------------------------------------------------------------

    /**
     * Set error state
     * @param {string} message - Human-readable error message
     * @param {Error} error - Original error object
     */
    setError(message, error) {
      this.error = message
      this.lastError = {
        message,
        details: error?.message || 'Unknown error',
        timestamp: new Date(),
      }
      console.error(`Dashboard error: ${message}`, error)
    },

    /**
     * Clear error state
     */
    clearError() {
      this.error = null
    },

    // -------------------------------------------------------------------------
    // State Management
    // -------------------------------------------------------------------------

    /**
     * Reset store to initial state
     */
    $reset() {
      this.stopPolling()
      this.metrics = null
      this.crisisTrends = []
      this.crtActivity = []
      this.activeSessions = []
      this.isLoading = false
      this.error = null
      this.lastUpdated = null
    },
  },
})
