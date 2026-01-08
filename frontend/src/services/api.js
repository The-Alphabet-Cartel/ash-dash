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
 * API Client - Axios-based service for backend communication
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-7-7.4-1
 * LAST MODIFIED: 2026-01-08
 * PHASE: Phase 7 - Documentation Wiki
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import axios from 'axios'

// =============================================================================
// Axios Instance Configuration
// =============================================================================

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for Pocket-ID auth
})

// =============================================================================
// Request Interceptor
// =============================================================================

api.interceptors.request.use(
  (config) => {
    // Could add auth headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// =============================================================================
// Response Interceptor
// =============================================================================

api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Unauthorized - redirect to login (Phase 4)
          console.warn('Unauthorized - authentication required')
          // window.location.href = '/auth/login'
          break
        case 403:
          console.warn('Forbidden - insufficient permissions')
          break
        case 404:
          console.warn('Resource not found')
          break
        case 500:
          console.error('Server error:', error.response.data)
          break
      }
    } else if (error.request) {
      // Network error
      console.error('Network error - no response received')
    }
    return Promise.reject(error)
  }
)

// =============================================================================
// Health API (Note: Health endpoints are at root, not under /api)
// =============================================================================

export const healthApi = {
  /**
   * Get system health status
   * @returns {Promise<{status, service, version, timestamp, components?}>}
   */
  getHealth: () => axios.get('/health'),

  /**
   * Get detailed health with component status
   * @returns {Promise<{status, components: {database, redis, sync_service}}>}
   */
  getHealthDetailed: () => axios.get('/health/detailed'),
}

// =============================================================================
// Sessions API (Phase 5 Enhanced)
// =============================================================================

export const sessionsApi = {
  /**
   * List sessions with search, filtering, and pagination
   * @param {Object} params - Query parameters
   * @param {string} params.search - Search by user ID, session ID, or username
   * @param {string} params.severity - Filter by severity (critical, high, medium, low, safe)
   * @param {string} params.status - Filter by status (active, closed, archived)
   * @param {string} params.date_from - Filter sessions started after (ISO datetime)
   * @param {string} params.date_to - Filter sessions started before (ISO datetime)
   * @param {number} params.page - Page number (default: 1)
   * @param {number} params.page_size - Items per page (default: 20, max: 100)
   * @returns {Promise<{items, total, page, page_size, total_pages, has_more}>}
   */
  list: (params = {}) => api.get('/sessions', { params }),

  /**
   * Get active sessions for dashboard
   * @returns {Promise<Array<SessionSummary>>}
   */
  getActive: () => api.get('/sessions/active'),

  /**
   * Get critical severity sessions
   * @returns {Promise<Array<SessionSummary>>}
   */
  getCritical: () => api.get('/sessions/critical'),

  /**
   * Get unassigned sessions (no CRT member assigned)
   * @returns {Promise<Array<SessionSummary>>}
   */
  getUnassigned: () => api.get('/sessions/unassigned'),

  /**
   * Get session statistics
   * @param {number} days - Number of days to include (default: 30)
   * @returns {Promise<{period_days, total_sessions, by_severity, by_status, average_crisis_score}>}
   */
  getStats: (days = 30) => api.get('/sessions/stats', { params: { days } }),

  /**
   * Get detailed session information with Ash analysis
   * @param {string} id - Session ID
   * @returns {Promise<SessionDetail>}
   */
  get: (id) => api.get(`/sessions/${id}`),

  /**
   * Get notes for a session
   * @param {string} id - Session ID
   * @returns {Promise<Array<NoteResponse>>}
   */
  getNotes: (id) => api.get(`/sessions/${id}/notes`),

  /**
   * Get session history for a Discord user with pattern analysis
   * @param {number} discordUserId - Discord user snowflake ID
   * @param {Object} params - Query parameters
   * @param {string} params.exclude_session - Session ID to exclude (current session)
   * @param {number} params.limit - Max sessions to return (default: 10, max: 50)
   * @returns {Promise<UserSessionHistory>}
   */
  getUserHistory: (discordUserId, params = {}) => 
    api.get(`/sessions/user/${discordUserId}`, { params }),

  /**
   * Assign CRT user to session
   * @param {string} id - Session ID
   * @param {string} crtUserId - CRT user UUID to assign
   * @returns {Promise<SessionDetail>}
   */
  assign: (id, crtUserId) => api.post(`/sessions/${id}/assign`, { crt_user_id: crtUserId }),

  /**
   * Remove CRT assignment from session
   * @param {string} id - Session ID
   * @returns {Promise<SessionDetail>}
   */
  unassign: (id) => api.post(`/sessions/${id}/unassign`),

  /**
   * Close an active session
   * @param {string} id - Session ID
   * @param {string} summary - Optional closing summary
   * @returns {Promise<SessionDetail>}
   */
  close: (id, summary = null) => {
    const body = summary ? { summary } : {}
    return api.post(`/sessions/${id}/close`, body)
  },

  /**
   * Reopen a closed session (admin only)
   * @param {string} id - Session ID
   * @returns {Promise<SessionDetail>}
   */
  reopen: (id) => api.post(`/sessions/${id}/reopen`),
}

// =============================================================================
// Users API
// =============================================================================

export const usersApi = {
  /**
   * List CRT users with filters
   * @param {Object} params - Query parameters
   * @returns {Promise<Array>}
   */
  list: (params = {}) => api.get('/users', { params }),

  /**
   * Get admin users only
   * @returns {Promise<Array>}
   */
  getAdmins: () => api.get('/users/admins'),

  /**
   * Get CRT members only
   * @returns {Promise<Array>}
   */
  getCRT: () => api.get('/users/crt'),

  /**
   * Get current authenticated user
   * @returns {Promise<Object>}
   */
  getMe: () => api.get('/users/me'),

  /**
   * Get user by ID with session summary
   * @param {string} id - User UUID
   * @returns {Promise<Object>}
   */
  get: (id) => api.get(`/users/${id}`),

  /**
   * Get sessions assigned to a user
   * @param {string} id - User UUID
   * @returns {Promise<Array>}
   */
  getSessions: (id) => api.get(`/users/${id}/sessions`),
}

// =============================================================================
// Notes API (Phase 6)
// =============================================================================

export const notesApi = {
  /**
   * Get notes for a session
   * @param {string} sessionId - Session ID
   * @returns {Promise<{session_id, notes, total, is_session_locked}>}
   */
  list: (sessionId) => api.get(`/notes/session/${sessionId}`),

  /**
   * Create a note for a session
   * @param {string} sessionId - Session ID
   * @param {Object} data - Note data {content: string, content_html?: string}
   * @returns {Promise<NoteDetail>}
   */
  create: (sessionId, data) => api.post(`/notes/session/${sessionId}`, data),

  /**
   * Get a specific note
   * @param {string} noteId - Note UUID
   * @returns {Promise<NoteDetail>}
   */
  get: (noteId) => api.get(`/notes/${noteId}`),

  /**
   * Update a note's content
   * @param {string} noteId - Note UUID
   * @param {Object} data - Updated note data {content: string, content_html?: string}
   * @returns {Promise<NoteDetail>}
   */
  update: (noteId, data) => api.put(`/notes/${noteId}`, data),

  /**
   * Delete a note (admin only)
   * @param {string} noteId - Note UUID
   * @returns {Promise<void>}
   */
  delete: (noteId) => api.delete(`/notes/${noteId}`),

  /**
   * Lock a note (prevent further edits)
   * @param {string} noteId - Note UUID
   * @returns {Promise<NoteDetail>}
   */
  lock: (noteId) => api.post(`/notes/${noteId}/lock`),

  /**
   * Unlock a note (admin only)
   * @param {string} noteId - Note UUID
   * @returns {Promise<NoteDetail>}
   */
  unlock: (noteId) => api.post(`/notes/${noteId}/unlock`),

  /**
   * Search notes by content
   * @param {string} query - Search query
   * @param {Object} params - Optional parameters
   * @param {string} params.session_id - Filter by session
   * @param {number} params.limit - Max results (default: 50)
   * @returns {Promise<Array<NoteSummary>>}
   */
  search: (query, params = {}) => api.get('/notes/search', { params: { q: query, ...params } }),
}

// =============================================================================
// Dashboard API (Phase 4)
// =============================================================================

export const dashboardApi = {
  /**
   * Get aggregated metrics for dashboard cards
   * @returns {Promise<DashboardMetrics>}
   */
  getMetrics: () => api.get('/dashboard/metrics'),

  /**
   * Get daily crisis trend data for charts
   * @param {number} days - Number of days (default: 30, max: 90)
   * @returns {Promise<Array<CrisisTrendPoint>>}
   */
  getCrisisTrends: (days = 30) => api.get('/dashboard/crisis-trends', { params: { days } }),

  /**
   * Get CRT member activity statistics
   * @param {number} days - Number of days (default: 7, max: 30)
   * @returns {Promise<Array<CRTActivityItem>>}
   */
  getCRTActivity: (days = 7) => api.get('/dashboard/crt-activity', { params: { days } }),

  /**
   * Get active sessions for real-time display
   * @returns {Promise<Array<ActiveSessionItem>>}
   */
  getActiveSessions: () => api.get('/dashboard/active-sessions'),
}

// =============================================================================
// Wiki API (Phase 7)
// =============================================================================

export const wikiApi = {
  /**
   * List wiki documents with optional filtering
   * @param {Object} params - Query parameters
   * @param {string} params.category - Filter by category
   * @param {string} params.tag - Filter by tag
   * @returns {Promise<{documents, total, category_filter, tag_filter}>}
   */
  listDocuments: (params = {}) => api.get('/wiki/documents', { params }),

  /**
   * Get a specific document by slug
   * @param {string} slug - Document slug (e.g., 'crt/crisis-response-guide')
   * @param {boolean} render - Whether to render HTML (default: true)
   * @returns {Promise<WikiDocument>}
   */
  getDocument: (slug, render = true) => api.get(`/wiki/documents/${slug}`, { params: { render } }),

  /**
   * Download document as PDF
   * @param {string} slug - Document slug
   * @returns {Promise<Blob>}
   */
  downloadPDF: (slug) => api.get(`/wiki/documents/${slug}/pdf`, { responseType: 'blob' }),

  /**
   * Get navigation structure grouped by category
   * @returns {Promise<{categories, total_documents}>}
   */
  getNavigation: () => api.get('/wiki/navigation'),

  /**
   * Search documents
   * @param {string} query - Search query
   * @param {number} limit - Max results (default: 20)
   * @returns {Promise<{query, results, total}>}
   */
  search: (query, limit = 20) => api.get('/wiki/search', { params: { q: query, limit } }),

  /**
   * Get all categories with document counts
   * @returns {Promise<Array<WikiCategory>>}
   */
  getCategories: () => api.get('/wiki/categories'),

  /**
   * Get all tags with document counts
   * @returns {Promise<Array<WikiTag>>}
   */
  getTags: () => api.get('/wiki/tags'),

  /**
   * Get CSS styles for wiki content
   * @param {boolean} includeSyntax - Include syntax highlighting CSS
   * @returns {Promise<string>}
   */
  getStyles: (includeSyntax = true) => api.get('/wiki/styles', { 
    params: { include_syntax: includeSyntax },
    transformResponse: [(data) => data], // Return raw CSS string
  }),

  /**
   * Force refresh wiki cache
   * @returns {Promise<{status, documents_found}>}
   */
  refresh: () => api.post('/wiki/refresh'),

  /**
   * Get wiki system status
   * @returns {Promise<{status, docs_path, document_count, pdf_available, categories, tags}>}
   */
  getStatus: () => api.get('/wiki/status'),
}

// =============================================================================
// Default Export
// =============================================================================

export default api
