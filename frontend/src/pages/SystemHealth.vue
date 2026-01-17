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
System Health Page (Simplified) - CRT-Accessible Ecosystem Status Overview
----------------------------------------------------------------------------
FILE VERSION: v5.0-3-3.1-2
LAST MODIFIED: 2026-01-17
PHASE: Phase 3 - CRT-Accessible System Health
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

PURPOSE:
    Simplified system health view accessible to all CRT members (member+).
    Shows operational/down status without detailed metrics like latency,
    versions, or inter-component connectivity.
    
    For detailed system health information, admins can access /admin/health.
============================================================================
-->

<template>
  <MainLayout>
    <div class="system-health-simple">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          System Health
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Ash ecosystem status overview
        </p>
      </div>
      
      <button
        @click="fetchEcosystemHealth"
        :disabled="isLoading"
        class="btn-secondary flex items-center gap-2"
        aria-label="Refresh status"
      >
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': isLoading }" aria-hidden="true" />
        Refresh
      </button>
    </div>

    <!-- Overall Status Banner -->
    <div 
      class="mb-6 p-6 rounded-lg"
      :class="overallStatusClass"
      role="status"
      :aria-label="`Ecosystem status: ${overallStatusLabel}`"
    >
      <div class="flex items-center gap-4">
        <div 
          class="w-12 h-12 rounded-full flex items-center justify-center"
          :class="overallIconBgClass"
        >
          <component :is="overallStatusIcon" class="w-7 h-7" aria-hidden="true" />
        </div>
        <div>
          <h2 class="text-xl font-bold">
            {{ overallStatusLabel }}
          </h2>
          <p class="text-sm opacity-80">
            {{ overallStatusDescription }}
          </p>
        </div>
      </div>
      
      <!-- Last Updated -->
      <p v-if="lastUpdated !== '—'" class="mt-4 text-xs opacity-60">
        Last checked: {{ lastUpdated }} · Auto-refreshes every 30 seconds
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !ecosystemHealth" class="flex flex-col items-center justify-center py-16">
      <Loader2 class="w-10 h-10 animate-spin text-purple-500 mb-4" aria-hidden="true" />
      <p class="text-gray-500 dark:text-gray-400">Checking ecosystem health...</p>
    </div>

    <!-- Error State -->
    <div 
      v-else-if="error && !ecosystemHealth" 
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6"
      role="alert"
    >
      <div class="flex items-center gap-3 text-red-600 dark:text-red-400">
        <AlertCircle class="w-6 h-6 flex-shrink-0" aria-hidden="true" />
        <div>
          <p class="font-semibold">Unable to check system health</p>
          <p class="text-sm opacity-80">{{ error }}</p>
        </div>
      </div>
      <button 
        @click="fetchEcosystemHealth" 
        class="mt-4 text-sm text-red-600 dark:text-red-400 hover:underline focus:underline"
      >
        Try again
      </button>
    </div>

    <!-- Component Status Grid -->
    <div v-else>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Component Status
      </h3>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="component in components"
          :key="component.id"
          class="card p-4 border-l-4 transition-colors"
          :class="component.isUp ? 'border-green-500' : 'border-red-500'"
        >
          <div class="flex items-center justify-between">
            <!-- Component Info -->
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-lg flex items-center justify-center"
                :class="component.isUp 
                  ? 'bg-green-100 dark:bg-green-900/30' 
                  : 'bg-red-100 dark:bg-red-900/30'"
              >
                <component 
                  :is="component.icon" 
                  class="w-5 h-5"
                  :class="component.isUp 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'"
                  aria-hidden="true"
                />
              </div>
              <div>
                <h4 class="font-semibold text-gray-900 dark:text-white">
                  {{ component.name }}
                </h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ component.description }}
                </p>
              </div>
            </div>
            
            <!-- Status Indicator -->
            <div class="flex items-center gap-2">
              <span 
                class="w-3 h-3 rounded-full"
                :class="component.isUp 
                  ? 'bg-green-500 animate-pulse' 
                  : 'bg-red-500'"
                :aria-label="component.isUp ? 'Operational' : 'Down'"
              />
              <component 
                :is="component.isUp ? CheckCircle : XCircle" 
                class="w-5 h-5"
                :class="component.isUp ? 'text-green-500' : 'text-red-500'"
                aria-hidden="true"
              />
            </div>
          </div>
          
          <!-- Simple Status Label -->
          <div class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
            <span 
              class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
              :class="component.isUp 
                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'"
            >
              {{ component.isUp ? 'Operational' : component.statusLabel }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Admin Link -->
      <div 
        v-if="authStore.isAdmin" 
        class="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
      >
        <p class="text-sm text-gray-600 dark:text-gray-400">
          <router-link 
            to="/admin/health" 
            class="text-purple-600 dark:text-purple-400 hover:underline font-medium"
          >
            View detailed system health →
          </router-link>
          <span class="ml-2">
            (includes latency, versions, and inter-component connectivity)
          </span>
        </p>
      </div>
    </div>
    </div>
  </MainLayout>
</template>

<script setup>
/**
 * System Health Page (Simplified)
 * 
 * CRT-accessible overview of Ash ecosystem health status.
 * Shows simple operational/down indicators for each component.
 * 
 * Components monitored:
 * - Ash-Bot (Discord bot)
 * - Ash-NLP (Crisis detection NLP server)
 * - Ash-Dash (This dashboard)
 * - Ash-Vault (Archive & backup infrastructure)
 * - Ash (Core) (Ecosystem Health API)
 * - Ash-Thrash (Testing suite - when enabled)
 * 
 * Auto-refreshes every 30 seconds.
 * 
 * Authorization: All CRT members (member+)
 */

import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  RefreshCw, 
  Loader2, 
  AlertCircle, 
  CheckCircle,
  XCircle,
  Bot,
  Brain,
  LayoutDashboard,
  Shield,
  Network,
  TestTube2,
  Server,
} from 'lucide-vue-next'
import { ecosystemApi } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { MainLayout } from '@/components/layout'
import { format } from 'date-fns'

// =============================================================================
// Stores
// =============================================================================

const authStore = useAuthStore()

// =============================================================================
// State
// =============================================================================

const ecosystemHealth = ref(null)
const isLoading = ref(true)
const error = ref(null)
const lastUpdated = ref('—')

let refreshInterval = null

// =============================================================================
// Component Configuration
// =============================================================================

/**
 * Map ecosystem component keys to display configuration.
 * Keys match those returned by the /health/ecosystem endpoint.
 */
const componentConfig = {
  ash_bot: {
    name: 'Ash-Bot',
    icon: Bot,
    description: 'Discord Bot',
  },
  ash_nlp: {
    name: 'Ash-NLP',
    icon: Brain,
    description: 'Crisis Detection AI',
  },
  ash_dash: {
    name: 'Ash-Dash',
    icon: LayoutDashboard,
    description: 'This Dashboard',
  },
  ash_vault: {
    name: 'Ash-Vault',
    icon: Shield,
    description: 'Archive & Backup',
  },
  ash: {
    name: 'Ash (Core)',
    icon: Network,
    description: 'Health Monitor',
  },
  ash_thrash: {
    name: 'Ash-Thrash',
    icon: TestTube2,
    description: 'Testing Suite',
  },
}

// =============================================================================
// Computed Properties
// =============================================================================

/**
 * Transform ecosystem components into simplified display cards
 */
const components = computed(() => {
  if (!ecosystemHealth.value?.components) return []
  
  return Object.entries(ecosystemHealth.value.components).map(([key, data]) => {
    const config = componentConfig[key] || { 
      name: key, 
      icon: Server, 
      description: 'System Component' 
    }
    
    // Simplified status: up (healthy) or down (everything else)
    const isUp = data.status === 'healthy'
    
    // Get appropriate status label for non-healthy states
    let statusLabel = 'Down'
    if (data.status === 'degraded') statusLabel = 'Degraded'
    else if (data.status === 'unreachable') statusLabel = 'Unreachable'
    else if (data.status === 'disabled') statusLabel = 'Disabled'
    else if (data.status === 'unknown') statusLabel = 'Unknown'
    
    return {
      id: key,
      name: config.name,
      icon: config.icon,
      description: config.description,
      isUp,
      statusLabel,
    }
  })
})

/**
 * Overall ecosystem status - simplified to Operational/Issues/Down
 */
const overallStatusClass = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    case 'degraded':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    case 'unhealthy':
    case 'unreachable':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
  }
})

const overallIconBgClass = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return 'bg-green-200 dark:bg-green-800/50'
    case 'degraded':
      return 'bg-yellow-200 dark:bg-yellow-800/50'
    case 'unhealthy':
    case 'unreachable':
      return 'bg-red-200 dark:bg-red-800/50'
    default:
      return 'bg-gray-200 dark:bg-gray-700'
  }
})

const overallStatusIcon = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return CheckCircle
    case 'degraded':
      return AlertCircle
    case 'unhealthy':
    case 'unreachable':
      return XCircle
    default:
      return AlertCircle
  }
})

const overallStatusLabel = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return 'All Systems Operational'
    case 'degraded':
      return 'Some Systems Degraded'
    case 'unhealthy':
      return 'System Issues Detected'
    case 'unreachable':
      return 'Systems Unreachable'
    default:
      return 'Status Unknown'
  }
})

const overallStatusDescription = computed(() => {
  const status = ecosystemHealth.value?.status
  const summary = ecosystemHealth.value?.summary
  
  switch (status) {
    case 'healthy':
      return 'All Ash ecosystem components are running normally.'
    case 'degraded':
      const degradedCount = summary?.degraded || 0
      return `${degradedCount} component${degradedCount !== 1 ? 's are' : ' is'} experiencing issues.`
    case 'unhealthy':
      const unhealthyCount = (summary?.unhealthy || 0) + (summary?.unreachable || 0)
      return `${unhealthyCount} component${unhealthyCount !== 1 ? 's are' : ' is'} currently unavailable.`
    case 'unreachable':
      return 'Unable to reach ecosystem components.'
    default:
      return 'Unable to determine ecosystem status.'
  }
})

// =============================================================================
// API Methods
// =============================================================================

/**
 * Fetch ecosystem health status from Ash (Core) API
 */
async function fetchEcosystemHealth() {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await ecosystemApi.getHealth()
    ecosystemHealth.value = response.data
    lastUpdated.value = format(new Date(), 'h:mm:ss a')
  } catch (err) {
    console.error('Failed to fetch ecosystem health:', err)
    
    // Provide helpful error message
    if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to the health monitoring service.'
    } else if (err.response?.status === 503) {
      // 503 still includes health data
      if (err.response?.data) {
        ecosystemHealth.value = err.response.data
        lastUpdated.value = format(new Date(), 'h:mm:ss a')
        error.value = null
      }
    } else {
      error.value = 'Failed to check system health. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  fetchEcosystemHealth()
  
  // Auto-refresh every 30 seconds
  refreshInterval = setInterval(fetchEcosystemHealth, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>
