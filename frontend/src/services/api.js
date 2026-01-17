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
 * FILE VERSION: v5.0-2-2.6-1
 * LAST MODIFIED: 2026-01-17
 * PHASE: Phase 2 - Dashboard Integration (Ecosystem Health API)
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
  withCredentials: true, // Include cookies for OIDC session auth
})

// =============================================================================
// Ecosystem API Client (Proxied through Ash-Dash backend)
// =============================================================================

/**
 * Axios instance for Ash (Core) Ecosystem Health API.
 * 
 * The ecosystem API runs on a separate service (port 30887). Instead of calling
 * it directly from the browser (which can't resolve Docker hostnames), we proxy
 * through the Ash-Dash backend at /api/ecosystem/*.
 * 
 * Proxy Pattern:
 *   Browser → /api/ecosystem/* (Ash-Dash) → http://ash:30887/* (Ash Core)
 * 
 * This approach:
 *   - Uses Docker internal networking (ash:30887)
 *   - No VITE_ environment variables needed
 *   - No external URL configuration required
 *   - Works seamlessly in any deployment environment
 */
const ecosystemApiClient = axios.create({
  baseURL: '/api/ecosystem',
  timeout: 15000, // Longer timeout for ecosystem-wide checks
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for OIDC session auth
})

// =============================================================================
// Auth Helper - Redirect to login
// =============================================================================

/**
 * Redirect to OIDC login flow.
 * Preserves the current path so user returns to where they were.
 */
const redirectToLogin = () => {
  // Get current path for redirect after login
  const currentPath = window.location.pathname + window.location.search
  
  // Don't redirect if already on auth pages
  if (currentPath.startsWith('/auth/') || currentPath.startsWith('/unauthorized')) {
    return
  }
  
  // Redirect to login with return path
  const loginUrl = `/auth/login?redirect=${encodeURIComponent(currentPath)}`
  window.location.href = loginUrl
}

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
          // Unauthorized - session expired or missing
          // Redirect to OIDC login flow
          console.warn('Unauthorized - redirecting to login')
          redirectToLogin()
          break
        case 403:
          console.warn('Forbidden - insufficient permissions')
          // Could redirect to /unauthorized page here
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
// Ecosystem Health API (Ash Core - Aggregated Health)
// =============================================================================

/**
 * API for Ash (Core) Ecosystem Health service.
 * 
 * Provides centralized health monitoring for all Ash ecosystem components:
 * - Ash-Bot (Discord bot)
 * - Ash-NLP (Crisis detection NLP)
 * - Ash-Dash (This dashboard)
 * - Ash-Vault (Archive infrastructure)
 * - Ash-Thrash (Testing suite)
 * 
 * Also validates inter-component connectivity.
 */
export const ecosystemApi = {
  /**
   * Get full ecosystem health report
   * 
   * Proxied: /api/ecosystem/health → http://ash:30887/health/ecosystem
   * 
   * @returns {Promise<{
   *   ecosystem: string,
   *   status: 'healthy'|'degraded'|'unhealthy'|'unreachable',
   *   timestamp: string,
   *   summary: {healthy: number, degraded: number, unhealthy: number, unreachable: number, disabled: number},
   *   components: Object<string, {status, endpoint, response_time_ms?, version?, error?}>,
   *   connections: Object<string, {status, latency_ms?, error?}>,
   *   meta: {check_duration_ms, timeout_ms, aggregator_version}
   * }>}
   */
  getHealth: () => ecosystemApiClient.get('/health'),

  /**
   * Simple liveness check for Ash (Core) API
   * 
   * Proxied: /api/ecosystem/liveness → http://ash:30887/health
   * 
   * @returns {Promise<{status, service, timestamp}>}
   */
  getLiveness: () => ecosystemApiClient.get('/liveness'),

  /**
   * Readiness check for Ash (Core) API
   * 
   * Proxied: /api/ecosystem/readiness → http://ash:30887/health/ready
   * 
   * @returns {Promise<{status, ready, service, timestamp}>}
   */
  getReadiness: () => ecosystemApiClient.get('/readiness'),

  /**
   * Get Ash (Core) service info
   * 
   * Proxied: /api/ecosystem/info → http://ash:30887/
   * 
   * @returns {Promise<{service, description, version, endpoints}>}
   */
  getInfo: () => ecosystemApiClient.get('/info'),
}

// =============================================================================
// Health API (Ash-Dash Internal - Note: Health endpoints are at root, not under /api)
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
  downloadPDF: (slug) => api.get(`/wiki/pdf/${slug}`, { responseType: 'blob' }),

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
// Archives API (Phase 9)
// =============================================================================

export const archivesApi = {
  /**
   * Archive a session
   * @param {string} sessionId - Session ID to archive
   * @param {Object} data - Archive options
   * @param {string} data.retention_tier - 'standard' or 'permanent'
   * @returns {Promise<ArchiveCreateResponse>}
   */
  archiveSession: (sessionId, data = {}) => 
    api.post(`/archives/session/${sessionId}`, data),

  /**
   * List archives with filtering
   * @param {Object} params - Query parameters
   * @param {number} params.discord_user_id - Filter by Discord user ID
   * @param {string} params.severity - Filter by severity
   * @param {string} params.retention_tier - Filter by retention tier
   * @param {number} params.skip - Records to skip
   * @param {number} params.limit - Max records (default: 50)
   * @returns {Promise<{archives, total, skip, limit}>}
   */
  list: (params = {}) => api.get('/archives', { params }),

  /**
   * Get archive storage statistics
   * @returns {Promise<ArchiveStatistics>}
   */
  getStatistics: () => api.get('/archives/statistics'),

  /**
   * Get archives expiring soon
   * @param {number} days - Days until expiration (default: 30)
   * @returns {Promise<Array<ExpiringArchive>>}
   */
  getExpiring: (days = 30) => api.get('/archives/expiring', { params: { days } }),

  /**
   * Get archive metadata
   * @param {string} archiveId - Archive UUID
   * @returns {Promise<ArchiveMetadata>}
   */
  get: (archiveId) => api.get(`/archives/${archiveId}`),

  /**
   * Download and decrypt archive
   * @param {string} archiveId - Archive UUID
   * @returns {Promise<ArchivePackage>}
   */
  download: (archiveId) => api.get(`/archives/${archiveId}/download`),

  /**
   * Update retention tier
   * @param {string} archiveId - Archive UUID
   * @param {string} retentionTier - New tier ('standard' or 'permanent')
   * @returns {Promise<ArchiveMetadata>}
   */
  updateRetention: (archiveId, retentionTier) => 
    api.put(`/archives/${archiveId}/retention`, { retention_tier: retentionTier }),

  /**
   * Extend retention by days
   * @param {string} archiveId - Archive UUID
   * @param {number} days - Days to extend
   * @returns {Promise<ArchiveMetadata>}
   */
  extendRetention: (archiveId, days) => 
    api.post(`/archives/${archiveId}/extend`, { days }),

  /**
   * Delete an archive (admin only)
   * @param {string} archiveId - Archive UUID
   * @returns {Promise<void>}
   */
  delete: (archiveId) => api.delete(`/archives/${archiveId}`),

  /**
   * Check if session is archived
   * @param {string} sessionId - Session ID
   * @returns {Promise<{session_id, is_archived, archive?}>}
   */
  checkSession: (sessionId) => api.get(`/archives/session/${sessionId}/check`),
}

// =============================================================================
// Auth API (Phase 10)
// =============================================================================

export const authApi = {
  /**
   * Get current authenticated user
   * @returns {Promise<{id, pocket_id, email, name, role, groups, is_admin, is_lead}>}
   */
  getCurrentUser: () => api.get('/auth/me'),

  /**
   * Check authentication status without triggering redirect
   * @returns {Promise<{authenticated, user?}>}
   */
  getStatus: () => api.get('/auth/status'),

  /**
   * Redirect to logout endpoint
   * This clears the session and redirects to PocketID logout
   */
  logout: () => {
    // Direct navigation to logout endpoint (not AJAX)
    window.location.href = '/auth/logout'
  },

  /**
   * Redirect to login endpoint
   * @param {string} redirect - Path to redirect to after login (default: current path)
   */
  login: (redirect = null) => {
    const path = redirect || window.location.pathname + window.location.search
    window.location.href = `/auth/login?redirect=${encodeURIComponent(path)}`
  },
}

// =============================================================================
// Admin API (Phase 10)
// =============================================================================

export const adminApi = {
  /**
   * Get all CRT team members
   * @returns {Promise<{users, total}>}
   */
  getUsers: () => api.get('/admin/users'),

  /**
   * Get audit logs with filtering and pagination
   * @param {Object} params - Query parameters
   * @param {string} params.action - Filter by action type
   * @param {string} params.entity_type - Filter by entity type
   * @param {string} params.user_id - Filter by user ID
   * @param {number} params.page - Page number (default: 1)
   * @param {number} params.page_size - Items per page (default: 50)
   * @returns {Promise<{logs, total, page, page_size, total_pages}>}
   */
  getAuditLogs: (params = {}) => api.get('/admin/audit-logs', { params }),

  /**
   * Get cleanup status for archives
   * @returns {Promise<CleanupStatusResponse>}
   */
  getCleanupStatus: () => api.get('/admin/archives/cleanup/status'),

  /**
   * Execute archive cleanup
   * @param {boolean} dryRun - If true, only report what would be deleted
   * @returns {Promise<CleanupExecuteResponse>}
   */
  executeCleanup: (dryRun = true) => 
    api.post('/admin/archives/cleanup/execute', null, { params: { dry_run: dryRun } }),

  /**
   * Get archives expiring soon
   * @param {number} days - Days until expiration (default: 30)
   * @returns {Promise<Array<ExpiringArchive>>}
   */
  getExpiringArchives: (days = 30) => 
    api.get('/admin/archives/expiring', { params: { days } }),
}

// =============================================================================
// Default Export
// =============================================================================

export default api
