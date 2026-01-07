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
 * FILE VERSION: v5.0-3-3.7-1
 * LAST MODIFIED: 2026-01-07
 * PHASE: Phase 3 - Frontend Foundation
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
// Sessions API
// =============================================================================

export const sessionsApi = {
  /**
   * List sessions with pagination and filters
   * @param {Object} params - Query parameters
   * @param {number} params.skip - Offset for pagination
   * @param {number} params.limit - Max results to return
   * @param {string} params.severity - Filter by severity
   * @param {string} params.status - Filter by status
   * @returns {Promise<Array>}
   */
  list: (params = {}) => api.get('/sessions', { params }),

  /**
   * Get active sessions for dashboard
   * @returns {Promise<Array>}
   */
  getActive: () => api.get('/sessions/active'),

  /**
   * Get critical severity sessions
   * @returns {Promise<Array>}
   */
  getCritical: () => api.get('/sessions/critical'),

  /**
   * Get unassigned sessions (no CRT member assigned)
   * @returns {Promise<Array>}
   */
  getUnassigned: () => api.get('/sessions/unassigned'),

  /**
   * Get session statistics
   * @param {number} days - Number of days to include (default: 30)
   * @returns {Promise<{period_days, total_sessions, by_severity, by_status, average_crisis_score}>}
   */
  getStats: (days = 30) => api.get('/sessions/stats', { params: { days } }),

  /**
   * Get single session by ID
   * @param {string} id - Session ID
   * @returns {Promise<Object>}
   */
  get: (id) => api.get(`/sessions/${id}`),

  /**
   * Get notes for a session
   * @param {string} id - Session ID
   * @returns {Promise<Array>}
   */
  getNotes: (id) => api.get(`/sessions/${id}/notes`),

  /**
   * Assign CRT user to session
   * @param {string} id - Session ID
   * @param {string} userId - User UUID to assign
   * @returns {Promise<Object>}
   */
  assign: (id, userId) => api.post(`/sessions/${id}/assign`, { user_id: userId }),

  /**
   * Remove CRT assignment from session
   * @param {string} id - Session ID
   * @returns {Promise<Object>}
   */
  unassign: (id) => api.post(`/sessions/${id}/unassign`),

  /**
   * Close a session
   * @param {string} id - Session ID
   * @returns {Promise<Object>}
   */
  close: (id) => api.post(`/sessions/${id}/close`),

  /**
   * Get session history for a Discord user
   * @param {string} discordId - Discord user ID
   * @returns {Promise<Array>}
   */
  getUserHistory: (discordId) => api.get(`/sessions/user/${discordId}`),
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
// Notes API (convenience wrappers)
// =============================================================================

export const notesApi = {
  /**
   * Get notes for a session
   * @param {string} sessionId - Session ID
   * @returns {Promise<Array>}
   */
  list: (sessionId) => api.get(`/sessions/${sessionId}/notes`),

  /**
   * Create a note for a session
   * @param {string} sessionId - Session ID
   * @param {Object} data - Note data {content: string}
   * @returns {Promise<Object>}
   */
  create: (sessionId, data) => api.post(`/sessions/${sessionId}/notes`, data),

  /**
   * Update a note
   * @param {string} sessionId - Session ID
   * @param {string} noteId - Note UUID
   * @param {Object} data - Updated note data
   * @returns {Promise<Object>}
   */
  update: (sessionId, noteId, data) => 
    api.put(`/sessions/${sessionId}/notes/${noteId}`, data),

  /**
   * Lock a note (prevent further edits)
   * @param {string} sessionId - Session ID
   * @param {string} noteId - Note UUID
   * @returns {Promise<Object>}
   */
  lock: (sessionId, noteId) => 
    api.post(`/sessions/${sessionId}/notes/${noteId}/lock`),
}

// =============================================================================
// Default Export
// =============================================================================

export default api
