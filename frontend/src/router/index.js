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
 * Vue Router Configuration - OIDC Authentication and Route Guards
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-3-3.2-1
 * LAST MODIFIED: 2026-01-17
 * PHASE: Phase 3 - CRT-Accessible System Health
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 * 
 * AUTHENTICATION FLOW:
 *     1. User visits protected route
 *     2. Router guard checks auth status via /api/auth/status
 *     3. If not authenticated -> redirect to /auth/login
 *     4. User authenticates with PocketID
 *     5. Callback redirects back to original path
 * 
 * ROUTE PROTECTION:
 *     - requiresAuth: Route requires authenticated user (CRT member)
 *     - minRole: Minimum role required ('member', 'lead', 'admin')
 * 
 * ROLE HIERARCHY:
 *     member < lead < admin
 *     (Higher roles inherit all lower role permissions)
 * ============================================================================
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// =============================================================================
// Route Definitions
// =============================================================================

const routes = [
  // -------------------------------------------------------------------------
  // Main Application Routes
  // -------------------------------------------------------------------------
  {
    path: '/',
    name: 'dashboard',
    component: () => import(/* webpackChunkName: "main" */ '@/pages/Dashboard.vue'),
    meta: { 
      title: 'Dashboard', 
      requiresAuth: true,
    },
  },
  {
    path: '/sessions',
    name: 'sessions',
    component: () => import(/* webpackChunkName: "main" */ '@/pages/Sessions.vue'),
    meta: { 
      title: 'Sessions', 
      requiresAuth: true,
    },
  },
  {
    path: '/sessions/:id',
    name: 'session-detail',
    component: () => import(/* webpackChunkName: "detail" */ '@/pages/SessionDetail.vue'),
    meta: { 
      title: 'Session Detail', 
      requiresAuth: true,
    },
  },
  {
    path: '/archives',
    name: 'archives',
    component: () => import(/* webpackChunkName: "main" */ '@/pages/Archives.vue'),
    meta: { 
      title: 'Archives', 
      requiresAuth: true,
    },
  },
  {
    path: '/archives/:id',
    name: 'archive-detail',
    component: () => import(/* webpackChunkName: "detail" */ '@/pages/ArchiveDetail.vue'),
    meta: { 
      title: 'Archive Detail', 
      requiresAuth: true,
    },
  },
  {
    path: '/wiki',
    name: 'documentation',
    component: () => import(/* webpackChunkName: "wiki" */ '@/pages/Documentation.vue'),
    meta: { 
      title: 'Documentation', 
      requiresAuth: true,
    },
  },
  {
    path: '/system-health',
    name: 'system-health',
    component: () => import(/* webpackChunkName: "main" */ '@/pages/SystemHealth.vue'),
    meta: { 
      title: 'System Health', 
      requiresAuth: true,
    },
  },
  
  // -------------------------------------------------------------------------
  // Admin Routes (Role-Protected)
  // -------------------------------------------------------------------------
  {
    path: '/admin',
    component: () => import(/* webpackChunkName: "admin" */ '@/pages/admin/AdminLayout.vue'),
    meta: { 
      title: 'Administration',
      requiresAuth: true, 
      minRole: 'lead',
    },
    children: [
      {
        path: '',
        name: 'admin',
        redirect: '/admin/users',
      },
      {
        path: 'users',
        name: 'admin-users',
        component: () => import(/* webpackChunkName: "admin" */ '@/pages/admin/Users.vue'),
        meta: { 
          title: 'CRT Roster', 
          minRole: 'lead',
        },
      },
      {
        path: 'audit',
        name: 'admin-audit',
        component: () => import(/* webpackChunkName: "admin" */ '@/pages/admin/AuditLogs.vue'),
        meta: { 
          title: 'Audit Logs', 
          minRole: 'lead',
        },
      },
      {
        path: 'health',
        name: 'admin-health',
        component: () => import(/* webpackChunkName: "admin" */ '@/pages/admin/SystemHealth.vue'),
        meta: { 
          title: 'System Health', 
          minRole: 'admin',
        },
      },
    ],
  },
  
  // -------------------------------------------------------------------------
  // Auth / Error Routes (No auth required)
  // -------------------------------------------------------------------------
  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import(/* webpackChunkName: "error" */ '@/pages/Unauthorized.vue'),
    meta: { 
      title: 'Unauthorized',
      requiresAuth: false,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import(/* webpackChunkName: "error" */ '@/pages/NotFound.vue'),
    meta: { 
      title: 'Not Found',
      requiresAuth: false,
    },
  },
]

// =============================================================================
// Router Instance
// =============================================================================

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// =============================================================================
// Navigation Guards
// =============================================================================

/**
 * Global navigation guard for OIDC authentication and authorization.
 * 
 * Flow:
 * 1. Initialize auth store (checks session via /api/auth/status)
 * 2. If route requires auth and user not authenticated -> redirect to OIDC login
 * 3. If route has minRole and user lacks permission -> show unauthorized
 * 
 * Note: 401 responses from API calls are also caught by axios interceptor
 * which will redirect to login as a fallback.
 */
router.beforeEach(async (to, from, next) => {
  // Set document title
  const baseTitle = 'Ash-Dash'
  document.title = to.meta.title ? `${to.meta.title} | ${baseTitle}` : baseTitle
  
  // Skip auth check for non-protected routes
  if (!to.meta.requiresAuth) {
    return next()
  }
  
  // Get auth store (lazy initialization)
  const authStore = useAuthStore()
  
  // Initialize auth state if needed (calls /api/auth/status)
  if (!authStore.initialized) {
    await authStore.initialize()
  }
  
  // Check authentication requirement
  if (!authStore.isAuthenticated) {
    // Not authenticated - redirect to OIDC login
    // The login endpoint will redirect back to this path after auth
    console.log('Authentication required, redirecting to login')
    authStore.login(to.fullPath)
    return // Don't call next(), we're doing a full page redirect
  }
  
  // Check CRT membership
  if (!authStore.isCrtMember) {
    // Authenticated but not a CRT member
    console.warn('User authenticated but not a CRT member')
    return next({ 
      name: 'unauthorized',
      query: { error: 'CRT membership required' },
    })
  }
  
  // Check role requirement (if specified)
  const minRole = to.meta.minRole
  if (minRole && !authStore.hasPermission(minRole)) {
    // Insufficient permissions - redirect to dashboard
    console.warn(`Insufficient permissions for ${to.path}. Required: ${minRole}, Has: ${authStore.userRole}`)
    return next({ 
      name: 'dashboard',
      // Could add query param to show toast notification
    })
  }
  
  // All checks passed
  next()
})

// =============================================================================
// Export
// =============================================================================

export default router
