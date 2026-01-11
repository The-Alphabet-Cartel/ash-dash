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
CrisisTrendsChart Component - Stacked bar chart of daily crisis sessions
============================================================================
FILE VERSION: v5.0-4-4.4-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 4 - Dashboard & Metrics
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
  <CrisisTrendsChart 
    :data="crisisTrends" 
    :days="30"
    :loading="isLoading"
  />

PROPS:
  - data: Array of CrisisTrendPoint objects from API
  - days: Number of days shown (for title display)
  - loading: Show loading skeleton
-->

<template>
  <div class="card">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        Crisis Trends
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Last {{ days }} days by severity
      </p>
    </div>

    <!-- Chart Container -->
    <div class="p-6">
      <!-- Loading Skeleton -->
      <div v-if="loading" class="animate-pulse">
        <div class="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>

      <!-- Empty State -->
      <div 
        v-else-if="!data || data.length === 0" 
        class="h-64 flex items-center justify-center"
      >
        <div class="text-center">
          <BarChart3 class="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p class="text-gray-500 dark:text-gray-400">No trend data available</p>
        </div>
      </div>

      <!-- Chart -->
      <div v-else class="h-64">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>

    <!-- Legend -->
    <div v-if="!loading && data && data.length > 0" class="px-6 pb-6">
      <div class="flex flex-wrap gap-4 justify-center">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-purple-600"></span>
          <span class="text-xs text-gray-600 dark:text-gray-400">Critical</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-red-500"></span>
          <span class="text-xs text-gray-600 dark:text-gray-400">High</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-yellow-500"></span>
          <span class="text-xs text-gray-600 dark:text-gray-400">Medium</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-sm bg-green-500"></span>
          <span class="text-xs text-gray-600 dark:text-gray-400">Low</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { Chart, registerables } from 'chart.js'
import { BarChart3 } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'

// Register Chart.js components
Chart.register(...registerables)

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /** Array of CrisisTrendPoint data from API */
  data: {
    type: Array,
    default: () => [],
  },
  /** Number of days (for display) */
  days: {
    type: Number,
    default: 30,
  },
  /** Loading state */
  loading: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// State
// =============================================================================

const chartCanvas = ref(null)
let chartInstance = null

const themeStore = useThemeStore()

// =============================================================================
// Chart Configuration
// =============================================================================

/** Check if dark mode is active */
const isDarkMode = computed(() => themeStore.isDark)

/** Get theme-aware colors */
const getChartColors = () => {
  const isDark = isDarkMode.value
  return {
    gridColor: isDark ? 'rgba(75, 85, 99, 0.3)' : 'rgba(209, 213, 219, 0.5)',
    textColor: isDark ? '#9CA3AF' : '#6B7280',
  }
}

/** Chart severity colors (matching TailwindCSS) */
const SEVERITY_COLORS = {
  critical: 'rgb(147, 51, 234)',   // purple-600
  high: 'rgb(239, 68, 68)',        // red-500
  medium: 'rgb(245, 158, 11)',     // yellow-500
  low: 'rgb(34, 197, 94)',         // green-500
}

/** Format date labels for chart */
const formatDateLabel = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

/** Build chart configuration */
const buildChartConfig = () => {
  const colors = getChartColors()
  
  // Only show every Nth label to avoid crowding
  const labelInterval = props.data.length > 14 ? Math.ceil(props.data.length / 10) : 1
  
  return {
    type: 'bar',
    data: {
      labels: props.data.map(d => formatDateLabel(d.date)),
      datasets: [
        {
          label: 'Critical',
          data: props.data.map(d => d.critical),
          backgroundColor: SEVERITY_COLORS.critical,
          borderRadius: 2,
        },
        {
          label: 'High',
          data: props.data.map(d => d.high),
          backgroundColor: SEVERITY_COLORS.high,
          borderRadius: 2,
        },
        {
          label: 'Medium',
          data: props.data.map(d => d.medium),
          backgroundColor: SEVERITY_COLORS.medium,
          borderRadius: 2,
        },
        {
          label: 'Low',
          data: props.data.map(d => d.low),
          backgroundColor: SEVERITY_COLORS.low,
          borderRadius: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: false, // Using custom legend below chart
        },
        tooltip: {
          backgroundColor: isDarkMode.value ? '#1F2937' : '#FFFFFF',
          titleColor: isDarkMode.value ? '#F3F4F6' : '#111827',
          bodyColor: isDarkMode.value ? '#D1D5DB' : '#4B5563',
          borderColor: isDarkMode.value ? '#374151' : '#E5E7EB',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          callbacks: {
            title: (items) => {
              if (items.length > 0) {
                const index = items[0].dataIndex
                return props.data[index]?.date || ''
              }
              return ''
            },
            footer: (items) => {
              const total = items.reduce((sum, item) => sum + (item.raw || 0), 0)
              return `Total: ${total}`
            },
          },
        },
      },
      scales: {
        x: {
          stacked: true,
          grid: {
            display: false,
          },
          ticks: {
            color: colors.textColor,
            maxRotation: 45,
            minRotation: 0,
            callback: function(value, index) {
              // Show fewer labels when data is dense
              if (index % labelInterval === 0) {
                return this.getLabelForValue(value)
              }
              return ''
            },
          },
        },
        y: {
          stacked: true,
          beginAtZero: true,
          grid: {
            color: colors.gridColor,
          },
          ticks: {
            color: colors.textColor,
            stepSize: 1,
            precision: 0,
          },
        },
      },
    },
  }
}

// =============================================================================
// Chart Lifecycle
// =============================================================================

/** Create or update the chart */
const updateChart = () => {
  if (!chartCanvas.value) return
  
  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
  
  // Don't create if no data
  if (!props.data || props.data.length === 0) return
  
  // Create new chart
  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, buildChartConfig())
}

// Watch for data changes
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// Watch for theme changes
watch(isDarkMode, () => {
  updateChart()
})

// Create chart on mount
onMounted(() => {
  if (props.data && props.data.length > 0) {
    updateChart()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
})
</script>
