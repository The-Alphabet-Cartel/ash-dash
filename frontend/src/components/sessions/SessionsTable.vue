<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
SessionsTable - Table component for displaying session list
============================================================================
FILE VERSION: v5.0-11-11.3-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="overflow-hidden rounded-xl bg-white dark:bg-gray-800 shadow-sm">
    <!-- Table Header -->
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Sessions
          <span v-if="total > 0" class="ml-2 text-sm font-normal text-gray-500 dark:text-gray-400">
            ({{ total.toLocaleString() }} total)
          </span>
        </h3>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="divide-y divide-gray-200 dark:divide-gray-700">
      <div v-for="i in 5" :key="i" class="px-6 py-4 animate-pulse">
        <div class="flex items-center gap-4">
          <div class="w-20 h-6 bg-gray-200 dark:bg-gray-700 rounded-full" />
          <div class="flex-1">
            <div class="w-32 h-4 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
            <div class="w-48 h-3 bg-gray-200 dark:bg-gray-700 rounded" />
          </div>
          <div class="w-16 h-6 bg-gray-200 dark:bg-gray-700 rounded-full" />
          <div class="w-20 h-4 bg-gray-200 dark:bg-gray-700 rounded" />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="sessions.length === 0" class="px-6 py-16 text-center">
      <div class="mx-auto w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mb-4">
        <Inbox class="w-8 h-8 text-gray-400 dark:text-gray-500" aria-hidden="true" />
      </div>
      <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-1">No Sessions Found</h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm mx-auto">
        {{ emptyMessage }}
      </p>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full" aria-label="Sessions list">
        <thead class="bg-gray-50 dark:bg-gray-900/50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Severity
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              User
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Status
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Duration
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Started
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Assigned To
            </th>
            <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="session in sessions" 
            :key="session.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-purple-500"
            tabindex="0"
            role="button"
            :aria-label="`View session for ${session.discord_username || 'Unknown User'}`"
            @click="$emit('row-click', session)"
            @keydown.enter="$emit('row-click', session)"
            @keydown.space.prevent="$emit('row-click', session)"
          >
            <!-- Severity -->
            <td class="px-6 py-4 whitespace-nowrap">
              <SeverityBadge 
                :severity="session.severity" 
                :pulse="session.status === 'active'"
                size="sm"
              />
            </td>

            <!-- User Info -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex flex-col">
                <span class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ session.discord_username || 'Unknown User' }}
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-400 font-mono">
                  {{ session.discord_user_id }}
                </span>
              </div>
            </td>

            <!-- Status -->
            <td class="px-6 py-4 whitespace-nowrap">
              <StatusBadge :status="session.status" size="sm" />
            </td>

            <!-- Duration -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="text-sm text-gray-700 dark:text-gray-300">
                {{ session.duration_display || '—' }}
              </span>
            </td>

            <!-- Started -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex flex-col">
                <span class="text-sm text-gray-700 dark:text-gray-300">
                  {{ formatDate(session.started_at) }}
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-400">
                  {{ formatTime(session.started_at) }}
                </span>
              </div>
            </td>

            <!-- Assigned To -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span v-if="session.crt_member_name" class="text-sm text-gray-700 dark:text-gray-300">
                {{ session.crt_member_name }}
              </span>
              <span v-else class="text-sm text-gray-400 dark:text-gray-500 italic">
                Unassigned
              </span>
            </td>

            <!-- Actions -->
            <td class="px-6 py-4 whitespace-nowrap text-right">
              <button
                @click.stop="$emit('row-click', session)"
                class="inline-flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors"
              >
                View
                <ChevronRight class="w-4 h-4" aria-hidden="true" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { Inbox, ChevronRight } from 'lucide-vue-next'
import SeverityBadge from './SeverityBadge.vue'
import StatusBadge from './StatusBadge.vue'

defineProps({
  sessions: {
    type: Array,
    required: true,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyMessage: {
    type: String,
    default: 'No sessions match your current filters. Try adjusting your search criteria.'
  }
})

defineEmits(['row-click'])

/**
 * Format date to readable string
 */
function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

/**
 * Format time to readable string
 */
function formatTime(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>
