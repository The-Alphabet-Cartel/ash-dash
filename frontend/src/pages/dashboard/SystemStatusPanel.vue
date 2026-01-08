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
SystemStatusPanel Component - Service health status display
============================================================================
FILE VERSION: v5.0-4-4.7-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 4 - Dashboard & Metrics
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        System Status
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Service health overview
      </p>
    </div>

    <!-- Status Items -->
    <div class="p-6 space-y-4">
      <!-- Loading State -->
      <div v-if="loading" class="animate-pulse space-y-4">
        <div v-for="i in 4" :key="i" class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-2 h-2 rounded-full bg-gray-200 dark:bg-gray-700"></div>
            <div class="h-4 w-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>

      <!-- Status List -->
      <template v-else>
        <!-- Ash-Bot Status -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div 
              class="w-2 h-2 rounded-full" 
              :class="health.redis ? 'bg-green-500' : 'bg-red-500'"
            ></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Ash-Bot</span>
          </div>
          <span 
            class="text-xs"
            :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
          >
            {{ health.redis ? 'Online' : 'Offline' }}
          </span>
        </div>
        
        <!-- Ash-NLP Status -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div 
              class="w-2 h-2 rounded-full" 
              :class="health.redis ? 'bg-green-500' : 'bg-yellow-500'"
            ></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Ash-NLP</span>
          </div>
          <span 
            class="text-xs"
            :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'"
          >
            {{ health.redis ? 'Online' : 'Unknown' }}
          </span>
        </div>
        
        <!-- Redis Status -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div 
              class="w-2 h-2 rounded-full" 
              :class="health.redis ? 'bg-green-500' : 'bg-red-500'"
            ></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Redis</span>
          </div>
          <span 
            class="text-xs"
            :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
          >
            {{ health.redis ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
        
        <!-- Database Status -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div 
              class="w-2 h-2 rounded-full" 
              :class="health.database ? 'bg-green-500' : 'bg-red-500'"
            ></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">Database</span>
          </div>
          <span 
            class="text-xs"
            :class="health.database ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
          >
            {{ health.database ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
      </template>

      <!-- Divider -->
      <hr class="border-gray-200 dark:border-gray-700" />

      <!-- Last Sync Info -->
      <div class="text-center">
        <p class="text-xs text-gray-500 dark:text-gray-400">Sync Service</p>
        <p 
          class="text-sm font-medium"
          :class="health.sync_service ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'"
        >
          {{ health.sync_service ? 'Running' : 'Stopped' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { healthApi } from '@/services/api'

// =============================================================================
// State
// =============================================================================

const loading = ref(true)
const health = ref({
  database: false,
  redis: false,
  sync_service: false,
})

let pollInterval = null

// =============================================================================
// Data Fetching
// =============================================================================

const fetchHealth = async () => {
  try {
    const response = await healthApi.getHealthDetailed()
    if (response.data?.components) {
      health.value = {
        database: response.data.components.database?.connected ?? false,
        redis: response.data.components.redis?.connected ?? false,
        sync_service: response.data.components.sync_service?.running ?? false,
      }
    }
  } catch (error) {
    console.error('Failed to fetch health status:', error)
  } finally {
    loading.value = false
  }
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  fetchHealth()
  // Poll health every 30 seconds
  pollInterval = setInterval(fetchHealth, 30000)
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})
</script>
