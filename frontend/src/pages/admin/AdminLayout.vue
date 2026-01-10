<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
Admin Layout - Container for admin pages with tab navigation
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.3-4
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Page Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Administration
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Team management, audit logs, and system monitoring
      </p>
    </div>

    <!-- Admin Navigation Tabs -->
    <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
      <nav class="flex space-x-1" aria-label="Admin Navigation">
        <router-link
          v-for="tab in visibleTabs"
          :key="tab.to"
          :to="tab.to"
          class="flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors"
          :class="[
            isActiveTab(tab.to)
              ? 'border-purple-500 text-purple-600 dark:text-purple-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
          ]"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
        </router-link>
      </nav>
    </div>

    <!-- Page Content (Child Routes) -->
    <router-view />
  </MainLayout>
</template>

<script setup>
/**
 * Admin Layout Component
 * 
 * Provides consistent layout for all admin pages with:
 * - Page header with title and description
 * - Tab navigation filtered by user role
 * - Router view for child pages
 * 
 * Tab visibility is controlled by minRole - tabs are only shown
 * if the current user has sufficient permissions.
 */

import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { MainLayout } from '@/components/layout'
import { Users, FileText, Activity } from 'lucide-vue-next'

// =============================================================================
// Composables
// =============================================================================

const route = useRoute()
const authStore = useAuthStore()

// =============================================================================
// Tab Configuration
// =============================================================================

/**
 * Admin navigation tabs.
 * Each tab has a minimum role requirement for visibility.
 */
const tabs = [
  { 
    to: '/admin/users', 
    label: 'CRT Roster', 
    icon: Users, 
    minRole: 'lead',
  },
  { 
    to: '/admin/audit', 
    label: 'Audit Logs', 
    icon: FileText, 
    minRole: 'lead',
  },
  { 
    to: '/admin/health', 
    label: 'System Health', 
    icon: Activity, 
    minRole: 'admin',
  },
]

// =============================================================================
// Computed Properties
// =============================================================================

/**
 * Filter tabs based on user's role.
 * Only shows tabs the user has permission to access.
 */
const visibleTabs = computed(() => {
  return tabs.filter(tab => authStore.hasPermission(tab.minRole))
})

/**
 * Check if a tab is currently active.
 * @param {string} path - Tab path to check
 * @returns {boolean} True if tab is active
 */
const isActiveTab = (path) => {
  return route.path === path
}
</script>
