<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
UserHistoryPanel - Display user's session history and patterns
============================================================================
FILE VERSION: v5.0-5-5.6-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card p-6">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
      <Clock class="w-5 h-5 text-purple-500" />
      User History
    </h3>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div class="h-16 bg-gray-200 dark:bg-gray-700 rounded" />
      <div class="h-12 bg-gray-200 dark:bg-gray-700 rounded" />
      <div class="h-12 bg-gray-200 dark:bg-gray-700 rounded" />
    </div>

    <!-- No History -->
    <div v-else-if="!history || history.total_sessions === 0" class="text-center py-6 text-gray-500 dark:text-gray-400">
      <History class="w-10 h-10 mx-auto mb-2 text-gray-300 dark:text-gray-600" />
      <p class="text-sm">No previous sessions</p>
    </div>

    <!-- Content -->
    <div v-else class="space-y-4">
      <!-- Summary Card -->
      <div class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-900 dark:text-white">
            {{ history.total_sessions }} Prior Session{{ history.total_sessions !== 1 ? 's' : '' }}
          </span>
          <span v-if="trendBadge" :class="['px-2 py-0.5 rounded text-xs font-medium', trendBadge.class]">
            {{ trendBadge.label }}
          </span>
        </div>
        
        <!-- Pattern Details -->
        <div class="space-y-1 text-sm text-gray-500 dark:text-gray-400">
          <p v-if="history.pattern_analysis.last_session_days_ago !== null">
            Last session: {{ formatDaysAgo(history.pattern_analysis.last_session_days_ago) }}
          </p>
          <p v-if="history.pattern_analysis.common_time_of_day">
            Pattern: {{ history.pattern_analysis.common_time_of_day }}
          </p>
          <p v-if="history.pattern_analysis.average_frequency_days">
            Avg frequency: Every {{ history.pattern_analysis.average_frequency_days }} days
          </p>
        </div>
      </div>

      <!-- Recent Sessions List -->
      <div class="space-y-2">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Recent Sessions</p>
        
        <div 
          v-for="session in displayedSessions" 
          :key="session.id"
          @click="$emit('view-session', session.id)"
          class="p-2 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors"
        >
          <div class="flex items-center justify-between">
            <SeverityBadge :severity="session.severity" size="sm" :show-dot="false" />
            <span class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatDate(session.started_at) }}
            </span>
          </div>
          <div class="flex items-center justify-between mt-1">
            <StatusBadge :status="session.status" size="sm" :show-icon="false" />
            <span class="text-xs text-gray-500 dark:text-gray-400">
              {{ session.duration_display || 'Ongoing' }}
            </span>
          </div>
        </div>

        <!-- View All Button -->
        <button 
          v-if="history.total_sessions > 3"
          @click="$emit('view-all-history', history.discord_user_id)"
          class="w-full py-2 text-sm font-medium text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 transition-colors"
        >
          View Full History →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Clock, History } from 'lucide-vue-next'
import { SeverityBadge, StatusBadge } from '@/components/sessions'

const props = defineProps({
  history: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  maxDisplayed: {
    type: Number,
    default: 3
  }
})

defineEmits(['view-session', 'view-all-history'])

const displayedSessions = computed(() => {
  if (!props.history?.sessions) return []
  return props.history.sessions.slice(0, props.maxDisplayed)
})

const trendBadge = computed(() => {
  const trend = props.history?.pattern_analysis?.severity_trend
  if (!trend) return null
  
  switch (trend) {
    case 'escalating':
      return { label: '↑ Escalating', class: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' }
    case 'improving':
      return { label: '↓ Improving', class: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' }
    case 'stable':
      return { label: '→ Stable', class: 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300' }
    default:
      return null
  }
})

function formatDaysAgo(days) {
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} week${Math.floor(days / 7) > 1 ? 's' : ''} ago`
  return `${Math.floor(days / 30)} month${Math.floor(days / 30) > 1 ? 's' : ''} ago`
}

function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}
</script>
