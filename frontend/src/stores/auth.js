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
 * Authentication Store - OIDC Session-Based Authentication
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-10-10.4-1
 * LAST MODIFIED: 2026-01-10
 * PHASE: Phase 10 - Authentication & Authorization
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 *
 * AUTHENTICATION FLOW:
 *   1. App loads -> checkAuth() called
 *   2. If no session -> redirect to /auth/login
 *   3. User authenticates with PocketID
 *   4. Callback creates session, redirects back
 *   5. App loads user data from /api/auth/me
 *
 * SESSION MANAGEMENT:
 *   - Sessions stored in Redis (DB 1)
 *   - Cookie: ash_session_id (HttpOnly, Secure, SameSite=Lax)
 *   - Automatic token refresh in backend middleware
 *   - Logout clears session and redirects to PocketID logout
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/services/api'

/**
 * Role hierarchy for permission comparison.
 * Higher index = more permissions.
 */
const ROLE_HIERARCHY = ['member', 'lead', 'admin']

export const useAuthStore = defineStore('auth', () => {
  // ==========================================================================
  // State
  // ==========================================================================
  
  /** Current authenticated user data */
  const user = ref(null)
  
  /** Whether auth state is being loaded */
  const isLoading = ref(true)
  
  /** Last authentication error */
  const error = ref(null)
  
  /** Whether initial auth check has completed */
  const initialized = ref(false)
  
  // ==========================================================================
  // Computed Properties
  // ==========================================================================
  
  /** User is authenticated with valid session */
  const isAuthenticated = computed(() => !!user.value)
  
  /** User is a CRT member (has any role) */
  const isCrtMember = computed(() => user.value?.role !== null && user.value?.role !== undefined)
  
  /** User is Lead or Admin */
  const isLead = computed(() => ['lead', 'admin'].includes(user.value?.role))
  
  /** User is Admin */
  const isAdmin = computed(() => user.value?.role === 'admin')
  
  /** Current user's role (member/lead/admin or null) */
  const userRole = computed(() => user.value?.role || null)
  
  /** Current user's display name */
  const userName = computed(() => user.value?.name || user.value?.email || 'Unknown')
  
  /** Current user's email */
  const userEmail = computed(() => user.value?.email || '')
  
  /** Current user's database ID */
  const userId = computed(() => user.value?.id || null)
  
  /** Current user's PocketID */
  const userPocketId = computed(() => user.value?.pocket_id || null)
  
  /** Current user's groups */
  const userGroups = computed(() => user.value?.groups || [])
  
  // ==========================================================================
  // Methods
  // ==========================================================================
  
  /**
   * Check if current user has at least the required role.
   * 
   * @param {string} requiredRole - Required role (member, lead, admin)
   * @returns {boolean} True if user meets or exceeds required role
   */
  const hasPermission = (requiredRole) => {
    if (!user.value?.role) return false
    
    const userIndex = ROLE_HIERARCHY.indexOf(user.value.role)
    const requiredIndex = ROLE_HIERARCHY.indexOf(requiredRole)
    
    // User role must be at least as high as required role
    return userIndex >= requiredIndex
  }
  
  /**
   * Check authentication status without triggering redirect.
   * Used on app initialization to determine if user is logged in.
   * 
   * @returns {Promise<boolean>} True if authenticated
   */
  const checkAuth = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.getStatus()
      
      if (response.data.authenticated && response.data.user) {
        user.value = response.data.user
        initialized.value = true
        return true
      } else {
        user.value = null
        initialized.value = true
        return false
      }
    } catch (err) {
      console.error('Auth check failed:', err)
      user.value = null
      initialized.value = true
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Fetch current user from API.
   * Will trigger 401 redirect if not authenticated.
   */
  const fetchCurrentUser = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('Failed to fetch user:', err)
      error.value = err.response?.data?.detail || 'Authentication failed'
      user.value = null
      
      // Note: 401 redirect is handled by axios interceptor in api.js
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Redirect to login page.
   * Preserves current path for redirect after login.
   * 
   * @param {string} redirect - Optional custom redirect path
   */
  const login = (redirect = null) => {
    authApi.login(redirect)
  }
  
  /**
   * Log out the current user.
   * Redirects to /auth/logout which clears session and goes to PocketID logout.
   */
  const logout = () => {
    // Clear local state
    user.value = null
    initialized.value = false
    
    // Redirect to logout endpoint (handles session cleanup + PocketID logout)
    authApi.logout()
  }
  
  /**
   * Clear the current error state.
   */
  const clearError = () => {
    error.value = null
  }
  
  /**
   * Initialize auth state on app load.
   * Checks if user is authenticated and loads user data.
   */
  const initialize = async () => {
    if (initialized.value) {
      return isAuthenticated.value
    }
    
    const authenticated = await checkAuth()
    return authenticated
  }
  
  // ==========================================================================
  // Return Store
  // ==========================================================================
  
  return {
    // State
    user,
    isLoading,
    error,
    initialized,
    
    // Computed
    isAuthenticated,
    isCrtMember,
    isLead,
    isAdmin,
    userRole,
    userName,
    userEmail,
    userId,
    userPocketId,
    userGroups,
    
    // Methods
    hasPermission,
    checkAuth,
    fetchCurrentUser,
    login,
    logout,
    clearError,
    initialize,
  }
})
