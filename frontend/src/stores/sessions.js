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
 * Sessions Store - Pinia store for session list state management
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-11-11.4-1
 * LAST MODIFIED: 2026-01-11
 * PHASE: Phase 11 - Session Claim Feature
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sessionsApi } from '@/services'

export const useSessionsStore = defineStore('sessions', () => {
  // ==========================================================================
  // State
  // ==========================================================================
  
  // Session list data
  const sessions = ref([])
  const total = ref(0)
  const totalPages = ref(1)
  const hasMore = ref(false)
  
  // Pagination state
  const currentPage = ref(1)
  const pageSize = ref(20)
  
  // Filter state
  const filters = ref({
    search: '',
    severity: '',
    status: '',
    dateFrom: null,
    dateTo: null,
  })
  
  // Loading and error state
  const isLoading = ref(false)
  const error = ref(null)
  
  // Current session detail
  const currentSession = ref(null)
  const isLoadingDetail = ref(false)
  
  // User history
  const userHistory = ref(null)
  const isLoadingHistory = ref(false)

  // ==========================================================================
  // Computed
  // ==========================================================================
  
  const hasFilters = computed(() => {
    return filters.value.search || 
           filters.value.severity || 
           filters.value.status ||
           filters.value.dateFrom ||
           filters.value.dateTo
  })
  
  const filterSummary = computed(() => {
    const parts = []
    if (filters.value.severity) parts.push(`Severity: ${filters.value.severity}`)
    if (filters.value.status) parts.push(`Status: ${filters.value.status}`)
    if (filters.value.dateFrom || filters.value.dateTo) parts.push('Date filtered')
    return parts.join(' • ')
  })

  // ==========================================================================
  // Actions
  // ==========================================================================
  
  /**
   * Fetch sessions with current filters and pagination
   */
  async function fetchSessions() {
    isLoading.value = true
    error.value = null
    
    try {
      const params = {
        page: currentPage.value,
        page_size: pageSize.value,
      }
      
      // Add filters if set
      if (filters.value.search) params.search = filters.value.search
      if (filters.value.severity) params.severity = filters.value.severity
      if (filters.value.status) params.status = filters.value.status
      if (filters.value.dateFrom) params.date_from = filters.value.dateFrom
      if (filters.value.dateTo) params.date_to = filters.value.dateTo
      
      const response = await sessionsApi.list(params)
      const data = response.data
      
      sessions.value = data.items
      total.value = data.total
      totalPages.value = data.total_pages
      hasMore.value = data.has_more
      
    } catch (err) {
      console.error('Failed to fetch sessions:', err)
      error.value = err.response?.data?.detail || 'Failed to load sessions'
      sessions.value = []
      total.value = 0
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Update search filter with debounce support
   */
  function setSearch(value) {
    filters.value.search = value
    currentPage.value = 1 // Reset to first page on search
  }
  
  /**
   * Update severity filter
   */
  function setSeverity(value) {
    filters.value.severity = value
    currentPage.value = 1
    fetchSessions()
  }
  
  /**
   * Update status filter
   */
  function setStatus(value) {
    filters.value.status = value
    currentPage.value = 1
    fetchSessions()
  }
  
  /**
   * Update date range filters
   */
  function setDateRange(from, to) {
    filters.value.dateFrom = from
    filters.value.dateTo = to
    currentPage.value = 1
    fetchSessions()
  }
  
  /**
   * Clear all filters
   */
  function clearFilters() {
    filters.value = {
      search: '',
      severity: '',
      status: '',
      dateFrom: null,
      dateTo: null,
    }
    currentPage.value = 1
    fetchSessions()
  }
  
  /**
   * Change page
   */
  function setPage(page) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
      fetchSessions()
    }
  }
  
  /**
   * Change page size
   */
  function setPageSize(size) {
    pageSize.value = size
    currentPage.value = 1
    fetchSessions()
  }
  
  /**
   * Fetch a single session's details
   */
  async function fetchSessionDetail(sessionId) {
    isLoadingDetail.value = true
    error.value = null
    
    try {
      const response = await sessionsApi.get(sessionId)
      currentSession.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch session detail:', err)
      error.value = err.response?.data?.detail || 'Failed to load session'
      currentSession.value = null
      throw err
    } finally {
      isLoadingDetail.value = false
    }
  }
  
  /**
   * Fetch user session history with patterns
   */
  async function fetchUserHistory(discordUserId, excludeSessionId = null) {
    isLoadingHistory.value = true
    
    try {
      const params = { limit: 10 }
      if (excludeSessionId) params.exclude_session = excludeSessionId
      
      const response = await sessionsApi.getUserHistory(discordUserId, params)
      userHistory.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch user history:', err)
      userHistory.value = null
      throw err
    } finally {
      isLoadingHistory.value = false
    }
  }
  
  /**
   * Close a session
   */
  async function closeSession(sessionId, summary = null) {
    try {
      const response = await sessionsApi.close(sessionId, summary)
      
      // Update in list if present
      const index = sessions.value.findIndex(s => s.id === sessionId)
      if (index !== -1) {
        sessions.value[index] = { ...sessions.value[index], status: 'closed' }
      }
      
      // Update current session if it's the one we closed
      if (currentSession.value?.id === sessionId) {
        currentSession.value = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to close session:', err)
      throw err
    }
  }
  
  /**
   * Reopen a session (admin only)
   */
  async function reopenSession(sessionId) {
    try {
      const response = await sessionsApi.reopen(sessionId)
      
      // Update in list if present
      const index = sessions.value.findIndex(s => s.id === sessionId)
      if (index !== -1) {
        sessions.value[index] = { ...sessions.value[index], status: 'active' }
      }
      
      // Update current session if it's the one we reopened
      if (currentSession.value?.id === sessionId) {
        currentSession.value = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to reopen session:', err)
      throw err
    }
  }
  
  /**
  * Assign current user to a session (claim)
  * @param {string} sessionId - Session ID
  * @param {string} userId - CRT user UUID to assign
  */
  async function assignSession(sessionId, userId) {
    try {
      const response = await sessionsApi.assign(sessionId, userId)
      
      // Update in list if present
      const index = sessions.value.findIndex(s => s.id === sessionId)
      if (index !== -1) {
        sessions.value[index] = response.data
      }
      
      // Update current session if it's the one we assigned
      if (currentSession.value?.id === sessionId) {
        currentSession.value = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to assign session:', err)
      throw err
    }
  }
  
  /**
   * Unassign current user from a session (release)
   * @param {string} sessionId - Session ID
   */
  async function unassignSession(sessionId) {
    try {
      const response = await sessionsApi.unassign(sessionId)
      
      // Update in list if present
      const index = sessions.value.findIndex(s => s.id === sessionId)
      if (index !== -1) {
        sessions.value[index] = response.data
      }
      
      // Update current session if it's the one we unassigned
      if (currentSession.value?.id === sessionId) {
        currentSession.value = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to unassign session:', err)
      throw err
    }
  }
  
  /**
   * Clear current session detail
   */
  function clearCurrentSession() {
    currentSession.value = null
    userHistory.value = null
  }

  // ==========================================================================
  // Return
  // ==========================================================================
  
  return {
    // State
    sessions,
    total,
    totalPages,
    hasMore,
    currentPage,
    pageSize,
    filters,
    isLoading,
    error,
    currentSession,
    isLoadingDetail,
    userHistory,
    isLoadingHistory,
    
    // Computed
    hasFilters,
    filterSummary,
    
    // Actions
    fetchSessions,
    setSearch,
    setSeverity,
    setStatus,
    setDateRange,
    clearFilters,
    setPage,
    setPageSize,
    fetchSessionDetail,
    fetchUserHistory,
    closeSession,
    reopenSession,
    assignSession,
    unassignSession,
    clearCurrentSession,
  }
})

export default useSessionsStore
