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
 * Vue Router Configuration - Page routing and navigation guards
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-7-7.8-2
 * LAST MODIFIED: 2026-01-09
 * PHASE: Phase 7 - Documentation Wiki
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { createRouter, createWebHistory } from 'vue-router'

// Route definitions
const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/pages/Dashboard.vue'),
    meta: { 
      title: 'Dashboard', 
      requiresAuth: true 
    }
  },
  {
    path: '/sessions',
    name: 'sessions',
    component: () => import('@/pages/Sessions.vue'),
    meta: { 
      title: 'Sessions', 
      requiresAuth: true 
    }
  },
  {
    path: '/sessions/:id',
    name: 'session-detail',
    component: () => import('@/pages/SessionDetail.vue'),
    meta: { 
      title: 'Session Detail', 
      requiresAuth: true 
    }
  },
  {
    path: '/wiki',
    name: 'documentation',
    component: () => import('@/pages/Documentation.vue'),
    meta: { 
      title: 'Documentation', 
      requiresAuth: true 
    }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/pages/Admin.vue'),
    meta: { 
      title: 'Administration', 
      requiresAuth: true, 
      requiresAdmin: true 
    }
  },
]

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard for page titles
router.beforeEach((to, from, next) => {
  // Set document title
  document.title = `${to.meta.title || 'Page'} | Ash-Dash`
  
  // TODO: Add authentication checks in Phase 4
  // For now, allow all navigation
  next()
})

export default router
