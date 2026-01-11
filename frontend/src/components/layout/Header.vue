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
Header Component - Top header bar with page title, actions, and sidebar toggle
============================================================================
FILE VERSION: v5.0-11-11.1-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <header 
    class="sticky top-0 z-30 h-16 flex items-center justify-between px-6 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 transition-colors"
    role="banner"
  >
    
    <!-- Left: Mobile Menu Toggle + Page Title -->
    <div class="flex items-center gap-4">
      <!-- Mobile Sidebar Toggle (visible on small screens or when sidebar collapsed) -->
      <button
        @click="toggleSidebar"
        class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors lg:hidden"
        :title="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :aria-expanded="!isSidebarCollapsed"
        aria-controls="sidebar"
      >
        <Menu class="w-5 h-5" aria-hidden="true" />
      </button>
      
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        {{ pageTitle }}
      </h1>
      
      <!-- Breadcrumb (optional, for detail pages) -->
      <nav 
        v-if="breadcrumbs.length > 0" 
        class="hidden sm:flex items-center gap-2 text-sm"
        aria-label="Breadcrumb"
      >
        <ChevronRight class="w-4 h-4 text-gray-400" aria-hidden="true" />
        <span 
          v-for="(crumb, index) in breadcrumbs" 
          :key="index"
          class="text-gray-500 dark:text-gray-400"
          :aria-current="index === breadcrumbs.length - 1 ? 'page' : undefined"
        >
          {{ crumb }}
        </span>
      </nav>
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center gap-3" role="group" aria-label="Header actions">
      <!-- Refresh Button -->
      <button
        @click="$emit('refresh')"
        class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
        title="Refresh data"
        aria-label="Refresh data"
        :disabled="isRefreshing"
      >
        <RefreshCw 
          class="w-5 h-5" 
          :class="{ 'animate-spin': isRefreshing }" 
          aria-hidden="true" 
        />
      </button>

      <!-- Notifications (placeholder for future) -->
      <button
        class="relative p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
        title="Notifications"
        aria-label="Notifications"
        :aria-describedby="notificationCount > 0 ? 'notification-count' : undefined"
      >
        <Bell class="w-5 h-5" aria-hidden="true" />
        <!-- Notification badge -->
        <span 
          v-if="notificationCount > 0"
          id="notification-count"
          class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"
          role="status"
          :aria-label="`${notificationCount} unread notifications`"
        ></span>
      </button>

      <!-- Connection Status -->
      <div 
        class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium"
        :class="connectionStatusClass"
        role="status"
        :aria-label="`Connection status: ${connectionStatus}`"
      >
        <span 
          class="w-2 h-2 rounded-full" 
          :class="connectionDotClass"
          aria-hidden="true"
        ></span>
        <span>{{ connectionStatus }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
/**
 * Header Component
 * 
 * Top navigation bar with:
 * - Mobile sidebar toggle (for responsive design)
 * - Dynamic page title from route meta
 * - Breadcrumb navigation (future)
 * - Refresh action
 * - Notification indicator
 * - Connection status
 * 
 * Accessibility:
 * - ARIA labels on all interactive elements
 * - Status indicators for connection and notifications
 * - Keyboard navigation support
 */

import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { ChevronRight, RefreshCw, Bell, Menu } from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  isRefreshing: {
    type: Boolean,
    default: false
  },
  isConnected: {
    type: Boolean,
    default: true
  },
  notificationCount: {
    type: Number,
    default: 0
  }
})

// =============================================================================
// Emits
// =============================================================================

defineEmits(['refresh'])

// =============================================================================
// Stores
// =============================================================================

const uiStore = useUiStore()
const route = useRoute()

// =============================================================================
// Computed
// =============================================================================

/**
 * Sidebar collapsed state
 */
const isSidebarCollapsed = computed(() => uiStore.sidebarCollapsed)

/**
 * Page title from route meta
 */
const pageTitle = computed(() => route.meta?.title || 'Dashboard')

/**
 * Breadcrumbs (for future use with nested routes)
 */
const breadcrumbs = computed(() => {
  // Could be expanded for session detail pages, etc.
  return []
})

/**
 * Connection status text
 */
const connectionStatus = computed(() => props.isConnected ? 'Connected' : 'Disconnected')

/**
 * Connection status badge class
 */
const connectionStatusClass = computed(() => 
  props.isConnected 
    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
)

/**
 * Connection status dot class
 */
const connectionDotClass = computed(() =>
  props.isConnected 
    ? 'bg-green-500 animate-pulse' 
    : 'bg-red-500'
)

// =============================================================================
// Methods
// =============================================================================

/**
 * Toggle sidebar state
 */
function toggleSidebar() {
  uiStore.toggleSidebar()
}
</script>
