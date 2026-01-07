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
Dashboard Page - Main dashboard view with metrics overview
============================================================================
FILE VERSION: v5.0-3-3.7-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <!-- Active Sessions Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Sessions</span>
          <div class="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30">
            <MessageSquareWarning class="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ activeSessions.length }}</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">sessions</span>
        </div>
        <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
          {{ activeSessions.length === 0 ? 'No active crisis sessions' : 'Require CRT attention' }}
        </p>
      </div>

      <!-- Critical Sessions Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Critical</span>
          <div class="p-2 rounded-lg bg-red-100 dark:bg-red-900/30">
            <AlertTriangle class="w-5 h-5 text-red-600 dark:text-red-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ criticalCount }}</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">critical</span>
        </div>
        <p class="mt-2 text-xs" :class="criticalCount === 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
          {{ criticalCount === 0 ? 'All clear' : 'Immediate attention needed' }}
        </p>
      </div>

      <!-- Weekly Total Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">This Week</span>
          <div class="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30">
            <TrendingUp class="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.total_sessions }}</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">total</span>
        </div>
        <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
          {{ stats.total_sessions === 0 ? 'No sessions this period' : `Over ${stats.period_days} days` }}
        </p>
      </div>

      <!-- CRT Online Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">CRT Online</span>
          <div class="p-2 rounded-lg bg-green-100 dark:bg-green-900/30">
            <Users class="w-5 h-5 text-green-600 dark:text-green-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">1</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">members</span>
        </div>
        <p class="mt-2 text-xs text-green-600 dark:text-green-400">
          You are online
        </p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Active Sessions List (2/3 width) -->
      <div class="lg:col-span-2 card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Active Sessions</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Real-time crisis session monitoring</p>
        </div>
        <div class="p-6">
          <!-- Loading State -->
          <div v-if="loading" class="flex items-center justify-center py-12">
            <RefreshCw class="w-8 h-8 text-purple-500 animate-spin" />
          </div>

          <!-- Empty State -->
          <div v-else-if="activeSessions.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
            <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
              <Shield class="w-8 h-8 text-gray-400 dark:text-gray-500" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">No Active Sessions</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
              When Ash-Bot detects a crisis, active sessions will appear here for CRT response.
            </p>
          </div>

          <!-- Sessions List -->
          <div v-else class="space-y-4">
            <div 
              v-for="session in activeSessions" 
              :key="session.id"
              class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-purple-500 dark:hover:border-purple-500 transition-colors cursor-pointer"
              @click="$router.push(`/sessions/${session.id}`)"
            >
              <div class="flex items-center justify-between">
                <div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ session.discord_user_id }}</span>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    Started {{ formatTime(session.started_at) }}
                  </p>
                </div>
                <span 
                  class="px-2 py-1 rounded-full text-xs font-medium"
                  :class="severityClass(session.severity)"
                >
                  {{ session.severity }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Stats (1/3 width) -->
      <div class="card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">System Status</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Service health overview</p>
        </div>
        <div class="p-6 space-y-4">
          <!-- Ash-Bot Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" :class="health.redis ? 'bg-green-500' : 'bg-red-500'"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Ash-Bot</span>
            </div>
            <span class="text-xs" :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
              {{ health.redis ? 'Online' : 'Offline' }}
            </span>
          </div>
          
          <!-- Ash-NLP Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" :class="health.redis ? 'bg-green-500' : 'bg-yellow-500'"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Ash-NLP</span>
            </div>
            <span class="text-xs" :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'">
              {{ health.redis ? 'Online' : 'Unknown' }}
            </span>
          </div>
          
          <!-- Redis Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" :class="health.redis ? 'bg-green-500' : 'bg-red-500'"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Redis</span>
            </div>
            <span class="text-xs" :class="health.redis ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
              {{ health.redis ? 'Connected' : 'Disconnected' }}
            </span>
          </div>
          
          <!-- Database Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" :class="health.database ? 'bg-green-500' : 'bg-red-500'"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Database</span>
            </div>
            <span class="text-xs" :class="health.database ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
              {{ health.database ? 'Connected' : 'Disconnected' }}
            </span>
          </div>

          <!-- Divider -->
          <hr class="border-gray-200 dark:border-gray-700" />

          <!-- Last Sync -->
          <div class="text-center">
            <p class="text-xs text-gray-500 dark:text-gray-400">Last updated</p>
            <p class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ lastUpdated }}</p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { MainLayout } from '@/components/layout'
import { healthApi, sessionsApi } from '@/services/api'
import { 
  MessageSquareWarning, 
  AlertTriangle, 
  TrendingUp, 
  Users,
  Shield,
  RefreshCw
} from 'lucide-vue-next'

// =============================================================================
// State
// =============================================================================

const loading = ref(true)
const activeSessions = ref([])
const stats = ref({
  period_days: 7,
  total_sessions: 0,
  by_severity: {},
  by_status: {},
  average_crisis_score: null
})
const health = ref({
  database: false,
  redis: false,
  sync_service: false
})
const lastUpdated = ref('Loading...')

let refreshInterval = null

// =============================================================================
// Computed
// =============================================================================

const criticalCount = computed(() => {
  return activeSessions.value.filter(s => s.severity === 'critical').length
})

// =============================================================================
// Methods
// =============================================================================

const fetchData = async () => {
  try {
    // Fetch active sessions
    const sessionsResponse = await sessionsApi.getActive()
    activeSessions.value = sessionsResponse.data || []

    // Fetch stats (7 days)
    const statsResponse = await sessionsApi.getStats(7)
    stats.value = statsResponse.data

    // Fetch health
    const healthResponse = await healthApi.getHealthDetailed()
    if (healthResponse.data?.components) {
      health.value = {
        database: healthResponse.data.components.database?.connected ?? false,
        redis: healthResponse.data.components.redis?.connected ?? false,
        sync_service: healthResponse.data.components.sync_service?.running ?? false
      }
    }

    lastUpdated.value = 'Just now'
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    lastUpdated.value = 'Error fetching data'
  } finally {
    loading.value = false
  }
}

const formatTime = (timestamp) => {
  if (!timestamp) return 'Unknown'
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return 'Just now'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`
  return date.toLocaleDateString()
}

const severityClass = (severity) => {
  const classes = {
    critical: 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300',
    high: 'bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300',
    medium: 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300',
    low: 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300',
  }
  return classes[severity] || 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  fetchData()
  // Refresh every 30 seconds
  refreshInterval = setInterval(() => {
    fetchData()
    // Update "last updated" text while waiting
    let seconds = 0
    const updateInterval = setInterval(() => {
      seconds++
      if (seconds < 30) {
        lastUpdated.value = `${seconds}s ago`
      }
    }, 1000)
    setTimeout(() => clearInterval(updateInterval), 30000)
  }, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>
