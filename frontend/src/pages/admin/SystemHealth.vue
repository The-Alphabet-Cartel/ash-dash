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
System Health Page - Monitor Ash ecosystem services via centralized Ecosystem Health API
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-15
PHASE: Phase 2 - Dashboard Integration (Ecosystem Health API)
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
          Ecosystem Health
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Monitor all Ash ecosystem components
        </p>
      </div>
      
      <button
        @click="fetchEcosystemHealth"
        :disabled="isLoading"
        class="btn-secondary flex items-center gap-2"
      >
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': isLoading }" />
        Refresh
      </button>
    </div>

    <!-- Ecosystem Status Banner -->
    <div 
      class="mb-6 p-4 rounded-lg"
      :class="overallStatusClass"
    >
      <div class="flex items-center justify-between flex-wrap gap-4">
        <div class="flex items-center gap-3">
          <component :is="overallStatusIcon" class="w-6 h-6" />
          <div>
            <span class="font-semibold">
              Ecosystem: {{ overallStatusLabel }}
            </span>
            <p class="text-sm opacity-80">
              {{ overallStatusDescription }}
            </p>
          </div>
        </div>
        
        <!-- Summary Pills -->
        <div v-if="ecosystemHealth" class="flex flex-wrap gap-2">
          <span 
            v-if="ecosystemHealth.summary?.healthy" 
            class="px-2 py-1 rounded-full bg-green-500/20 text-green-600 dark:text-green-400 text-xs font-medium"
          >
            {{ ecosystemHealth.summary.healthy }} Healthy
          </span>
          <span 
            v-if="ecosystemHealth.summary?.degraded" 
            class="px-2 py-1 rounded-full bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 text-xs font-medium"
          >
            {{ ecosystemHealth.summary.degraded }} Degraded
          </span>
          <span 
            v-if="ecosystemHealth.summary?.unhealthy" 
            class="px-2 py-1 rounded-full bg-red-500/20 text-red-600 dark:text-red-400 text-xs font-medium"
          >
            {{ ecosystemHealth.summary.unhealthy }} Unhealthy
          </span>
          <span 
            v-if="ecosystemHealth.summary?.unreachable" 
            class="px-2 py-1 rounded-full bg-red-500/20 text-red-600 dark:text-red-400 text-xs font-medium"
          >
            {{ ecosystemHealth.summary.unreachable }} Unreachable
          </span>
          <span 
            v-if="ecosystemHealth.summary?.disabled" 
            class="px-2 py-1 rounded-full bg-gray-500/20 text-gray-600 dark:text-gray-400 text-xs font-medium"
          >
            {{ ecosystemHealth.summary.disabled }} Disabled
          </span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !ecosystemHealth" class="flex justify-center py-12">
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
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
        The Ash (Core) Ecosystem Health API may be unavailable.
      </p>
      <button 
        @click="fetchEcosystemHealth" 
        class="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
      >
        Try again
      </button>
    </div>

    <!-- Component Cards Grid -->
    <div v-else>
      <h4 class="text-md font-semibold text-gray-900 dark:text-white mb-4">
        Component Status
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ServiceCard
          v-for="component in components"
          :key="component.id"
          :name="component.name"
          :status="component.status"
          :icon="component.icon"
          :details="component.details"
        />
      </div>
    </div>

    <!-- Inter-Component Connectivity -->
    <div v-if="ecosystemHealth && Object.keys(ecosystemHealth.connections || {}).length > 0" class="mt-8">
      <h4 class="text-md font-semibold text-gray-900 dark:text-white mb-4">
        Inter-Component Connectivity
      </h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="(conn, name) in ecosystemHealth.connections" 
          :key="name"
          class="card p-4"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <ArrowRightLeft class="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ name }}</span>
            </div>
            <span 
              class="px-2 py-0.5 text-xs font-medium rounded-full"
              :class="getConnectionStatusClass(conn.status)"
            >
              {{ conn.status }}
            </span>
          </div>
          <div v-if="conn.latency_ms" class="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Latency: {{ conn.latency_ms }}ms
          </div>
          <div v-if="conn.error" class="text-xs text-red-500 dark:text-red-400 mt-2">
            {{ conn.error }}
          </div>
        </div>
      </div>
    </div>

    <!-- System Info -->
    <div v-if="ecosystemHealth" class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Ecosystem Version Card -->
      <div class="card p-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
            <Info class="w-4 h-4 text-purple-600 dark:text-purple-400" />
          </div>
          <span class="font-medium text-gray-900 dark:text-white">Ecosystem</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">
          v5.0
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Ash Crisis Detection
        </p>
      </div>
      
      <!-- Check Duration Card -->
      <div class="card p-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
            <Zap class="w-4 h-4 text-blue-600 dark:text-blue-400" />
          </div>
          <span class="font-medium text-gray-900 dark:text-white">Check Duration</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ ecosystemHealth.meta?.check_duration_ms?.toFixed(0) || '—' }}ms
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Full ecosystem check
        </p>
      </div>
      
      <!-- Last Updated Card -->
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
 * Ecosystem Health Page
 * 
 * Monitors the entire Ash ecosystem via the centralized Ecosystem Health API:
 * - Ash-Bot (Discord bot)
 * - Ash-NLP (Crisis detection NLP server)
 * - Ash-Dash (This dashboard)
 * - Ash-Vault (Archive & backup infrastructure)
 * - Ash (Core) (Ecosystem Health API itself)
 * - Ash-Thrash (Testing suite - when enabled)
 * 
 * Also displays inter-component connectivity status.
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
  HelpCircle,
  CircleDot,
  Bot,
  Brain,
  LayoutDashboard,
  Shield,
  Network,
  TestTube2,
  Server,
  Info,
  Clock,
  Zap,
  ArrowRightLeft,
} from 'lucide-vue-next'
import { ecosystemApi } from '@/services/api'
import { ServiceCard } from '@/components/admin'
import { format } from 'date-fns'

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
    description: 'Discord Crisis Detection Bot',
  },
  ash_nlp: {
    name: 'Ash-NLP',
    icon: Brain,
    description: 'NLP Classification Server',
  },
  ash_dash: {
    name: 'Ash-Dash',
    icon: LayoutDashboard,
    description: 'CRT Dashboard',
  },
  ash_vault: {
    name: 'Ash-Vault',
    icon: Shield,
    description: 'Archive & Backup Infrastructure',
  },
  ash: {
    name: 'Ash (Core)',
    icon: Network,
    description: 'Ecosystem Health API',
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
 * Transform ecosystem components into display cards
 */
const components = computed(() => {
  if (!ecosystemHealth.value?.components) return []
  
  return Object.entries(ecosystemHealth.value.components).map(([key, data]) => {
    const config = componentConfig[key] || { name: key, icon: Server, description: 'Unknown Component' }
    
    return {
      id: key,
      name: config.name,
      icon: config.icon,
      status: data.status || 'unknown',
      details: {
        ...data,
        description: config.description,
      },
    }
  })
})

/**
 * Overall ecosystem status styling
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
      return HelpCircle
  }
})

const overallStatusLabel = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return 'Operational'
    case 'degraded':
      return 'Degraded'
    case 'unhealthy':
      return 'Unhealthy'
    case 'unreachable':
      return 'Unreachable'
    default:
      return 'Unknown'
  }
})

const overallStatusDescription = computed(() => {
  const status = ecosystemHealth.value?.status
  
  switch (status) {
    case 'healthy':
      return 'All ecosystem components are running normally.'
    case 'degraded':
      return 'Some components are experiencing issues.'
    case 'unhealthy':
      return 'Critical components are unavailable.'
    case 'unreachable':
      return 'Unable to reach ecosystem components.'
    default:
      return 'Unable to determine ecosystem status.'
  }
})

/**
 * Get CSS classes for connection status badge
 */
function getConnectionStatusClass(status) {
  switch (status) {
    case 'healthy':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    case 'degraded':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    case 'unhealthy':
    case 'unreachable':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    case 'disabled':
      return 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
    default:
      return 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
  }
}

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
    lastUpdated.value = format(new Date(), 'HH:mm:ss')
  } catch (err) {
    console.error('Failed to fetch ecosystem health:', err)
    
    // Provide helpful error message based on error type
    if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to Ash (Core) API. The service may be down.'
    } else if (err.response?.status === 503) {
      error.value = 'Ecosystem health check failed. Some components may be unavailable.'
      // Still use the response data if available (503 includes health data)
      if (err.response?.data) {
        ecosystemHealth.value = err.response.data
        lastUpdated.value = format(new Date(), 'HH:mm:ss')
        error.value = null // Clear error since we got data
      }
    } else {
      error.value = err.response?.data?.detail || 'Failed to fetch ecosystem health'
    }
    
    // Set error state but keep stale data if available
    if (!ecosystemHealth.value) {
      ecosystemHealth.value = {
        status: 'unknown',
        components: {},
        connections: {},
        summary: {},
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
