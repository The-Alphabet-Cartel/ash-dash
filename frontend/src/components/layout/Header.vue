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
Header Component - Top header bar with page title and actions
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <header class="sticky top-0 z-30 h-16 flex items-center justify-between px-6 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 transition-colors">
    
    <!-- Left: Page Title -->
    <div class="flex items-center gap-4">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        {{ pageTitle }}
      </h1>
      <!-- Breadcrumb (optional, for detail pages) -->
      <nav v-if="breadcrumbs.length > 0" class="hidden sm:flex items-center gap-2 text-sm">
        <ChevronRight class="w-4 h-4 text-gray-400" />
        <span 
          v-for="(crumb, index) in breadcrumbs" 
          :key="index"
          class="text-gray-500 dark:text-gray-400"
        >
          {{ crumb }}
        </span>
      </nav>
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center gap-3">
      <!-- Refresh Button -->
      <button
        @click="$emit('refresh')"
        class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors"
        title="Refresh data"
      >
        <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': isRefreshing }" />
      </button>

      <!-- Notifications (placeholder for future) -->
      <button
        class="relative p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors"
        title="Notifications"
      >
        <Bell class="w-5 h-5" />
        <!-- Notification badge -->
        <span 
          v-if="notificationCount > 0"
          class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"
        ></span>
      </button>

      <!-- Connection Status -->
      <div 
        class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium"
        :class="connectionStatusClass"
      >
        <span class="w-2 h-2 rounded-full" :class="connectionDotClass"></span>
        {{ connectionStatus }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronRight, RefreshCw, Bell } from 'lucide-vue-next'

// Props
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

// Emits
defineEmits(['refresh'])

const route = useRoute()

// Page title from route meta
const pageTitle = computed(() => route.meta?.title || 'Dashboard')

// Breadcrumbs (for future use with nested routes)
const breadcrumbs = computed(() => {
  // Could be expanded for session detail pages, etc.
  return []
})

// Connection status
const connectionStatus = computed(() => props.isConnected ? 'Connected' : 'Disconnected')

const connectionStatusClass = computed(() => 
  props.isConnected 
    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
)

const connectionDotClass = computed(() =>
  props.isConnected 
    ? 'bg-green-500 animate-pulse' 
    : 'bg-red-500'
)
</script>
