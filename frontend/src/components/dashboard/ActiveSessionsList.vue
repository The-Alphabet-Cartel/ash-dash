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
ActiveSessionsList Component - Real-time list of active crisis sessions
============================================================================
FILE VERSION: v5.0-11-11.3-2
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation (ARIA)
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
  <ActiveSessionsList 
    :sessions="activeSessions" 
    :loading="isLoading"
  />

PROPS:
  - sessions: Array of ActiveSessionItem objects from API
  - loading: Show loading skeleton

FEATURES:
  - Severity indicator dots with pulse animation for critical/high
  - Real-time elapsed time display (updates every second)
  - Click row to navigate to session detail
  - Shows assigned CRT member
  - Empty state with helpful message
-->

<template>
  <div class="card">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Active Sessions
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Real-time crisis session monitoring
        </p>
      </div>
      <div v-if="sessions.length > 0" class="flex items-center gap-2">
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ sessions.length }} active
        </span>
        <RefreshCw 
          v-if="loading" 
          class="w-4 h-4 text-purple-500 animate-spin"
          aria-hidden="true"
        />
      </div>
    </div>

    <!-- Content -->
    <div class="p-6">
      <!-- Loading Skeleton -->
      <div v-if="loading && sessions.length === 0" class="animate-pulse space-y-4">
        <div v-for="i in 3" :key="i" class="flex items-center gap-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50">
          <div class="w-3 h-3 rounded-full bg-gray-200 dark:bg-gray-700"></div>
          <div class="flex-1">
            <div class="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
            <div class="h-3 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div class="h-6 w-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-else-if="sessions.length === 0" 
        class="flex flex-col items-center justify-center py-12 text-center"
      >
        <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
          <Shield class="w-8 h-8 text-gray-400 dark:text-gray-500" aria-hidden="true" />
        </div>
        <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-1">
          No Active Sessions
        </h4>
        <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
          When Ash-Bot detects a crisis, active sessions will appear here for CRT response.
        </p>
      </div>

      <!-- Sessions List -->
      <div v-else class="space-y-3" role="list" aria-label="Active crisis sessions">
        <div 
          v-for="session in sessions" 
          :key="session.session_id"
          class="session-item p-4 rounded-lg border border-gray-200 dark:border-gray-700 
                 hover:border-purple-500 dark:hover:border-purple-500 
                 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2
                 transition-all cursor-pointer group"
          role="listitem"
          tabindex="0"
          :aria-label="`View session for ${session.discord_username || 'User ' + session.discord_user_id}, severity ${session.severity}`"
          @click="navigateToSession(session.session_id)"
          @keydown.enter="navigateToSession(session.session_id)"
          @keydown.space.prevent="navigateToSession(session.session_id)"
        >
          <div class="flex items-center gap-4">
            <!-- Severity Indicator -->
            <div class="relative flex-shrink-0" aria-hidden="true">
              <span 
                class="w-3 h-3 rounded-full block"
                :class="severityDotClass(session.severity)"
              ></span>
              <!-- Pulse animation for critical/high -->
              <span 
                v-if="['critical', 'high'].includes(session.severity)"
                class="absolute inset-0 w-3 h-3 rounded-full animate-ping opacity-75"
                :class="severityPulseClass(session.severity)"
              ></span>
            </div>

            <!-- Session Info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-900 dark:text-white truncate">
                  {{ session.discord_username || `User ${session.discord_user_id}` }}
                </span>
                <span 
                  class="px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="severityBadgeClass(session.severity)"
                >
                  {{ session.severity }}
                </span>
              </div>
              <div class="flex items-center gap-3 mt-1 text-sm text-gray-500 dark:text-gray-400">
                <span class="flex items-center gap-1">
                  <Clock class="w-3.5 h-3.5" aria-hidden="true" />
                  {{ formatElapsed(session.elapsed_seconds) }}
                </span>
                <span v-if="session.crt_member_name" class="flex items-center gap-1">
                  <User class="w-3.5 h-3.5" aria-hidden="true" />
                  {{ session.crt_member_name }}
                </span>
                <span v-else class="text-yellow-600 dark:text-yellow-400">
                  Unassigned
                </span>
              </div>
            </div>

            <!-- Arrow -->
            <ChevronRight class="w-5 h-5 text-gray-400 group-hover:text-purple-500 transition-colors flex-shrink-0" aria-hidden="true" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Shield, RefreshCw, Clock, User, ChevronRight } from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /** Array of ActiveSessionItem data from API */
  sessions: {
    type: Array,
    default: () => [],
  },
  /** Loading state */
  loading: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// Router
// =============================================================================

const router = useRouter()

/** Navigate to session detail page */
const navigateToSession = (sessionId) => {
  router.push(`/sessions/${sessionId}`)
}

// =============================================================================
// Elapsed Time
// =============================================================================

// Force re-render every second for elapsed time updates
const tick = ref(0)
let tickInterval = null

onMounted(() => {
  // Update tick every second to refresh elapsed times
  tickInterval = setInterval(() => {
    tick.value++
  }, 1000)
})

onUnmounted(() => {
  if (tickInterval) {
    clearInterval(tickInterval)
  }
})

/** Format elapsed seconds into human-readable string */
const formatElapsed = (seconds) => {
  // Access tick.value to trigger reactivity
  const _ = tick.value
  
  if (seconds < 60) {
    return 'Just now'
  }
  if (seconds < 3600) {
    const mins = Math.floor(seconds / 60)
    return `${mins}m ago`
  }
  if (seconds < 86400) {
    const hours = Math.floor(seconds / 3600)
    const mins = Math.floor((seconds % 3600) / 60)
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h ago`
  }
  const days = Math.floor(seconds / 86400)
  return `${days}d ago`
}

// =============================================================================
// Severity Styling
// =============================================================================

/** Severity dot color classes */
const severityDotClass = (severity) => {
  const classes = {
    critical: 'bg-purple-600',
    high: 'bg-red-500',
    medium: 'bg-yellow-500',
    low: 'bg-green-500',
  }
  return classes[severity] || 'bg-gray-400'
}

/** Severity pulse animation color */
const severityPulseClass = (severity) => {
  const classes = {
    critical: 'bg-purple-600',
    high: 'bg-red-500',
  }
  return classes[severity] || ''
}

/** Severity badge classes */
const severityBadgeClass = (severity) => {
  const classes = {
    critical: 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300',
    high: 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300',
    medium: 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300',
    low: 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300',
  }
  return classes[severity] || 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
}
</script>

<style scoped>
/* Pulse animation for critical/high severity dots */
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}
</style>
