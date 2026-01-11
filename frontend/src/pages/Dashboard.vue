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
Dashboard Page - Main dashboard view with metrics, charts, and active sessions
============================================================================
FILE VERSION: v5.0-11-11.2-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

FEATURES:
  - Four metric cards with key statistics
  - Crisis trends chart (30 days)
  - CRT activity chart (7 days)
  - Active sessions list with real-time updates
  - Dual polling: 10s for sessions, 30s for metrics/charts
  - Auto-refresh indicator with last updated timestamp
  - Manual refresh button
-->

<template>
  <MainLayout>
    <!-- Header with Refresh Controls -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Crisis Response Team Overview
        </p>
      </div>
      <div class="flex items-center gap-4">
        <!-- Last Updated -->
        <div class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2">
          <span v-if="dashboard.isPolling" class="flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Live
          </span>
          <span>Updated {{ dashboard.lastUpdatedFormatted }}</span>
        </div>
        
        <!-- Refresh Button -->
        <button
          @click="handleRefresh"
          :disabled="dashboard.isLoading"
          class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg
                 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300
                 hover:bg-gray-200 dark:hover:bg-gray-700 
                 disabled:opacity-50 disabled:cursor-not-allowed
                 transition-colors"
        >
          <RefreshCw 
            class="w-4 h-4" 
            :class="{ 'animate-spin': dashboard.isLoading }" 
          />
          Refresh
        </button>
      </div>
    </div>

    <!-- Error Banner -->
    <ErrorMessage
      v-if="dashboard.hasError"
      class="mb-6"
      title="Unable to load dashboard data"
      :message="dashboard.error || 'Please check your connection and try again.'"
      :details="dashboard.errorDetails"
      @retry="handleRefresh"
    />

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <!-- Active Sessions Card -->
      <MetricCard
        label="Active Sessions"
        :value="dashboard.metrics?.active_sessions ?? 0"
        :sub-value="activeSessionsSubtext"
        :sub-value-type="dashboard.activeSessionCount > 0 ? 'warning' : 'neutral'"
        :icon="MessageSquareWarning"
        icon-color="purple"
        :loading="dashboard.isLoadingMetrics && !dashboard.metrics"
      />

      <!-- Critical + High Card -->
      <MetricCard
        label="Critical / High"
        :value="dashboard.metrics?.active_critical_high ?? 0"
        :sub-value="criticalHighSubtext"
        :sub-value-type="criticalHighSubtextType"
        :icon="AlertTriangle"
        icon-color="red"
        :loading="dashboard.isLoadingMetrics && !dashboard.metrics"
      />

      <!-- Weekly Total Card -->
      <MetricCard
        label="This Week"
        :value="dashboard.metrics?.week_total ?? 0"
        value-suffix="sessions"
        :sub-value="weekChangeSubtext"
        :sub-value-type="weekChangeType"
        :icon="TrendingUp"
        icon-color="blue"
        :loading="dashboard.isLoadingMetrics && !dashboard.metrics"
      />

      <!-- CRT Online Card -->
      <MetricCard
        label="CRT Online"
        :value="crtOnlineText"
        :sub-value="crtSubtext"
        sub-value-type="neutral"
        :icon="Users"
        icon-color="green"
        :loading="dashboard.isLoadingMetrics && !dashboard.metrics"
      />
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: Active Sessions (2/3 width on large screens) -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Active Sessions List -->
        <ActiveSessionsList
          :sessions="dashboard.activeSessions"
          :loading="dashboard.isLoadingSessions && dashboard.activeSessions.length === 0"
        />

        <!-- Crisis Trends Chart -->
        <CrisisTrendsChart
          :data="dashboard.crisisTrends"
          :days="30"
          :loading="dashboard.isLoadingTrends && dashboard.crisisTrends.length === 0"
        />
      </div>

      <!-- Right Column: CRT Activity + System Status (1/3 width) -->
      <div class="space-y-6">
        <!-- CRT Activity Chart -->
        <CRTActivityChart
          :data="dashboard.crtActivity"
          :days="7"
          :loading="dashboard.isLoadingActivity && dashboard.crtActivity.length === 0"
        />

        <!-- System Status Panel -->
        <SystemStatusPanel />
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { MainLayout } from '@/components/layout'
import { ErrorMessage } from '@/components/common'
import { 
  MetricCard, 
  CrisisTrendsChart, 
  CRTActivityChart, 
  ActiveSessionsList 
} from '@/components/dashboard'
import SystemStatusPanel from './dashboard/SystemStatusPanel.vue'
import { useDashboardStore } from '@/stores/dashboard'
import { 
  MessageSquareWarning, 
  AlertTriangle, 
  TrendingUp, 
  Users,
  RefreshCw,
} from 'lucide-vue-next'

// =============================================================================
// Store
// =============================================================================

const dashboard = useDashboardStore()

// =============================================================================
// Computed - Metric Card Subtexts
// =============================================================================

/** Active sessions subtext */
const activeSessionsSubtext = computed(() => {
  const count = dashboard.activeSessionCount
  if (count === 0) return 'No active crisis sessions'
  return count === 1 ? 'Requires CRT attention' : 'Require CRT attention'
})

/** Critical/High sessions subtext */
const criticalHighSubtext = computed(() => {
  const count = dashboard.metrics?.active_critical_high ?? 0
  if (count === 0) return 'All clear'
  return 'Immediate attention needed'
})

/** Critical/High subtext type */
const criticalHighSubtextType = computed(() => {
  const count = dashboard.metrics?.active_critical_high ?? 0
  return count === 0 ? 'positive' : 'negative'
})

/** Week change subtext */
const weekChangeSubtext = computed(() => {
  const change = dashboard.metrics?.week_change ?? 0
  if (change === 0) return 'Same as last week'
  const sign = change > 0 ? '+' : ''
  return `${sign}${change} from last week`
})

/** Week change type */
const weekChangeType = computed(() => {
  const change = dashboard.metrics?.week_change ?? 0
  // More sessions = concerning, fewer = good
  if (change > 0) return 'warning'
  if (change < 0) return 'positive'
  return 'neutral'
})

/** CRT online text */
const crtOnlineText = computed(() => {
  const active = dashboard.metrics?.crt_active ?? 0
  const total = dashboard.metrics?.crt_total ?? 0
  return `${active} / ${total}`
})

/** CRT subtext */
const crtSubtext = computed(() => {
  const active = dashboard.metrics?.crt_active ?? 0
  if (active === 0) return 'No CRT members with active sessions'
  return active === 1 ? 'Member handling session' : 'Members handling sessions'
})

// =============================================================================
// Actions
// =============================================================================

/** Manual refresh handler */
const handleRefresh = () => {
  dashboard.fetchAll()
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  // Start polling when dashboard is mounted
  dashboard.startPolling()
})

onUnmounted(() => {
  // Stop polling when navigating away
  dashboard.stopPolling()
})
</script>
