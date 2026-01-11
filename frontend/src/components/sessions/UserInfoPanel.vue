<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
UserInfoPanel - Display Discord user information for a session
============================================================================
FILE VERSION: v5.0-5-5.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card p-6">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
      <User class="w-5 h-5 text-purple-500" />
      User Information
    </h3>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3" />
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
    </div>

    <!-- Content -->
    <div v-else class="space-y-4">
      <!-- Discord Username -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Username</span>
        <span class="text-sm font-medium text-gray-900 dark:text-white">
          {{ session.discord_username || 'Unknown' }}
        </span>
      </div>

      <!-- Discord User ID -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Discord ID</span>
        <span class="text-sm font-mono text-gray-700 dark:text-gray-300">
          {{ session.discord_user_id }}
        </span>
      </div>

      <!-- Session ID -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Session ID</span>
        <span class="text-sm font-mono text-gray-700 dark:text-gray-300 truncate max-w-[200px]" :title="session.id">
          {{ session.id }}
        </span>
      </div>

      <hr class="border-gray-200 dark:border-gray-700" />

      <!-- Status -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Status</span>
        <StatusBadge :status="session.status" size="sm" />
      </div>

      <!-- Severity -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Severity</span>
        <SeverityBadge :severity="session.severity" size="sm" />
      </div>

      <hr class="border-gray-200 dark:border-gray-700" />

      <!-- Started At -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Started</span>
        <span class="text-sm text-gray-700 dark:text-gray-300">
          {{ formatDateTime(session.started_at) }}
        </span>
      </div>

      <!-- Ended At (if closed) -->
      <div v-if="session.ended_at" class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Ended</span>
        <span class="text-sm text-gray-700 dark:text-gray-300">
          {{ formatDateTime(session.ended_at) }}
        </span>
      </div>

      <!-- Duration -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Duration</span>
        <span class="text-sm text-gray-700 dark:text-gray-300">
          {{ session.duration_display || 'Ongoing' }}
        </span>
      </div>

      <hr class="border-gray-200 dark:border-gray-700" />

      <!-- CRT Assignment -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Assigned To</span>
        <span v-if="session.crt_member_name" class="text-sm font-medium text-gray-900 dark:text-white">
          {{ session.crt_member_name }}
        </span>
        <span v-else class="text-sm text-gray-400 dark:text-gray-500 italic">
          Unassigned
        </span>
      </div>

      <!-- Message Count -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500 dark:text-gray-400">Messages</span>
        <span class="text-sm text-gray-700 dark:text-gray-300">
          {{ session.message_count || 0 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { User } from 'lucide-vue-next'
import { SeverityBadge, StatusBadge } from '@/components/sessions'

defineProps({
  session: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

function formatDateTime(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>
