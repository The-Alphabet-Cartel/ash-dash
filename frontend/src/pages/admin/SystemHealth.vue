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
System Health Page - Monitor Ash ecosystem services
----------------------------------------------------------------------------
FILE VERSION: v5.0-11-11.11-2
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="system-health">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          System Health
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Monitor Ash ecosystem services
        </p>
      </div>
      
      <button
        @click="fetchHealth"
        :disabled="isLoading"
        class="btn-secondary flex items-center gap-2"
      >
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': isLoading }" />
        Refresh
      </button>
    </div>

    <!-- Overall Status Banner -->
    <div 
      class="mb-6 p-4 rounded-lg flex items-center gap-3"
      :class="overallStatusClass"
    >
      <component :is="overallStatusIcon" class="w-6 h-6" />
      <div>
        <span class="font-semibold">
          System Status: {{ overallStatusLabel }}
        </span>
        <p class="text-sm opacity-80">
          {{ overallStatusDescription }}
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !health" class="flex justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-purple-500" />
    </div>

    <!-- Error State -->
    <div 
      v-else-if="error" 
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
    >
      <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
        <AlertCircle class="w-5 h-5" />
        <p>{{ error }}</p>
      </div>
      <button 
        @click="fetchHealth" 
        class="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
      >
        Try again
      </button>
    </div>

    <!-- Service Cards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <ServiceCard
        v-for="service in services"
        :key="service.name"
        :name="service.name"
        :status="service.status"
        :icon="service.icon"
        :details="service.details"
      />
    </div>

    <!-- System Info -->
    <div v-if="health" class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Version Card -->
      <div class="card p-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
            <Info class="w-4 h-4 text-purple-600 dark:text-purple-400" />
          </div>
          <span class="font-medium text-gray-900 dark:text-white">Version</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ health.service?.version || 'Unknown' }}
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Ash-Dash
        </p>
      </div>
      
      <!-- Environment Card -->
      <div class="card p-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
            <Server class="w-4 h-4 text-blue-600 dark:text-blue-400" />
          </div>
          <span class="font-medium text-gray-900 dark:text-white">Environment</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white capitalize">
          {{ health.service?.environment || 'Unknown' }}
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Deployment mode
        </p>
      </div>
      
      <!-- Uptime Card -->
      <div class="card p-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
            <Clock class="w-4 h-4 text-green-600 dark:text-green-400" />
          </div>
          <span class="font-medium text-gray-900 dark:text-white">Last Check</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ lastUpdated }}
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Auto-refreshes every 30s
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * System Health Page
 * 
 * Monitors Ash ecosystem services:
 * - PostgreSQL database
 * - Redis (Ash-Bot integration)
 * - MinIO (Archive storage)
 * - Ash-NLP service
 * 
 * Auto-refreshes every 30 seconds.
 * 
 * Authorization: Admin only (enforced by route guard)
 */

import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  RefreshCw, 
  Loader2, 
  AlertCircle, 
  CheckCircle,
  XCircle,
  Database,
  Server,
  HardDrive,
  Cloud,
  Info,
  Clock,
} from 'lucide-vue-next'
import { healthApi } from '@/services/api'
import { ServiceCard } from '@/components/admin'
import { format } from 'date-fns'

// =============================================================================
// State
// =============================================================================

const health = ref(null)
const isLoading = ref(true)
const error = ref(null)
const lastUpdated = ref('—')

let refreshInterval = null

// =============================================================================
// Service Configuration
// =============================================================================

/**
 * Map backend service keys to display config
 */
const serviceConfig = {
  database: {
    name: 'PostgreSQL',
    icon: Database,
  },
  redis: {
    name: 'Redis (Ash-Bot)',
    icon: Server,
  },
  minio: {
    name: 'MinIO (Archives)',
    icon: HardDrive,
  },
  ash_nlp: {
    name: 'Ash-NLP',
    icon: Cloud,
  },
  sync_service: {
    name: 'Sync Service',
    icon: RefreshCw,
  },
}

// =============================================================================
// Computed Properties
// =============================================================================

/**
 * Transform health data into service cards
 */
const services = computed(() => {
  if (!health.value?.components) return []
  
  return Object.entries(health.value.components).map(([key, data]) => {
    const config = serviceConfig[key] || { name: key, icon: Server }
    
    return {
      name: config.name,
      icon: config.icon,
      status: data.status || 'unknown',
      details: data,
    }
  })
})

/**
 * Overall system status styling
 */
const overallStatusClass = computed(() => {
  const status = health.value?.status
  
  switch (status) {
    case 'healthy':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    case 'degraded':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    case 'unhealthy':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
  }
})

const overallStatusIcon = computed(() => {
  const status = health.value?.status
  
  switch (status) {
    case 'healthy':
      return CheckCircle
    case 'degraded':
      return AlertCircle
    case 'unhealthy':
      return XCircle
    default:
      return AlertCircle
  }
})

const overallStatusLabel = computed(() => {
  const status = health.value?.status
  
  switch (status) {
    case 'healthy':
      return 'Operational'
    case 'degraded':
      return 'Degraded'
    case 'unhealthy':
      return 'Unhealthy'
    default:
      return 'Unknown'
  }
})

const overallStatusDescription = computed(() => {
  const status = health.value?.status
  
  switch (status) {
    case 'healthy':
      return 'All services are running normally.'
    case 'degraded':
      return 'Some services are experiencing issues.'
    case 'unhealthy':
      return 'Critical services are unavailable.'
    default:
      return 'Unable to determine system status.'
  }
})

// =============================================================================
// API Methods
// =============================================================================

/**
 * Fetch detailed health status from API
 */
async function fetchHealth() {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await healthApi.getHealthDetailed()
    health.value = response.data
    lastUpdated.value = format(new Date(), 'HH:mm:ss')
  } catch (err) {
    console.error('Failed to fetch health:', err)
    error.value = err.response?.data?.detail || 'Failed to fetch system health'
    
    // Set error state but keep stale data if available
    if (!health.value) {
      health.value = {
        status: 'unknown',
        components: {},
      }
    }
  } finally {
    isLoading.value = false
  }
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  fetchHealth()
  
  // Auto-refresh every 30 seconds
  refreshInterval = setInterval(fetchHealth, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>
