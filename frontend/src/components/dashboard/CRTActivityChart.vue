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
CRTActivityChart Component - Horizontal bar chart of CRT member activity
============================================================================
FILE VERSION: v5.0-4-4.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 4 - Dashboard & Metrics
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
  <CRTActivityChart 
    :data="crtActivity" 
    :days="7"
    :loading="isLoading"
  />

PROPS:
  - data: Array of CRTActivityItem objects from API
  - days: Number of days shown (for title display)
  - loading: Show loading skeleton
-->

<template>
  <div class="card">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        CRT Activity
      </h3>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Sessions handled (last {{ days }} days)
      </p>
    </div>

    <!-- Chart Container -->
    <div class="p-6">
      <!-- Loading Skeleton -->
      <div v-if="loading" class="animate-pulse space-y-4">
        <div v-for="i in 5" :key="i" class="flex items-center gap-4">
          <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
          <div class="flex-1 h-6 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-else-if="!data || data.length === 0" 
        class="h-48 flex items-center justify-center"
      >
        <div class="text-center">
          <Users class="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p class="text-gray-500 dark:text-gray-400">No CRT activity data</p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
            Activity will appear when sessions are assigned
          </p>
        </div>
      </div>

      <!-- Chart -->
      <div v-else :style="{ height: chartHeight }">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { Users } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'

// Register Chart.js components
Chart.register(...registerables)

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /** Array of CRTActivityItem data from API */
  data: {
    type: Array,
    default: () => [],
  },
  /** Number of days (for display) */
  days: {
    type: Number,
    default: 7,
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
// Computed
// =============================================================================

/** Check if dark mode is active */
const isDarkMode = computed(() => themeStore.isDark)

/** Calculate chart height based on number of members */
const chartHeight = computed(() => {
  const barHeight = 40 // pixels per bar
  const padding = 60 // top/bottom padding
  const minHeight = 150
  const height = Math.max(minHeight, (props.data.length * barHeight) + padding)
  return `${height}px`
})

// =============================================================================
// Chart Configuration
// =============================================================================

/** Get theme-aware colors */
const getChartColors = () => {
  const isDark = isDarkMode.value
  return {
    gridColor: isDark ? 'rgba(75, 85, 99, 0.3)' : 'rgba(209, 213, 219, 0.5)',
    textColor: isDark ? '#9CA3AF' : '#6B7280',
    barColor: isDark ? 'rgba(147, 51, 234, 0.8)' : 'rgba(147, 51, 234, 0.7)',
    barHoverColor: 'rgba(147, 51, 234, 1)',
  }
}

/** Build chart configuration */
const buildChartConfig = () => {
  const colors = getChartColors()
  
  // Sort data by session count descending
  const sortedData = [...props.data].sort((a, b) => b.session_count - a.session_count)
  
  return {
    type: 'bar',
    data: {
      labels: sortedData.map(d => d.display_name),
      datasets: [
        {
          label: 'Sessions Handled',
          data: sortedData.map(d => d.session_count),
          backgroundColor: colors.barColor,
          hoverBackgroundColor: colors.barHoverColor,
          borderRadius: 4,
          borderSkipped: false,
        },
      ],
    },
    options: {
      indexAxis: 'y', // Horizontal bars
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: isDarkMode.value ? '#1F2937' : '#FFFFFF',
          titleColor: isDarkMode.value ? '#F3F4F6' : '#111827',
          bodyColor: isDarkMode.value ? '#D1D5DB' : '#4B5563',
          borderColor: isDarkMode.value ? '#374151' : '#E5E7EB',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: (context) => {
              const index = context.dataIndex
              const item = sortedData[index]
              const sessions = item.session_count
              const avgTime = item.avg_response_minutes
              
              let label = `${sessions} session${sessions !== 1 ? 's' : ''}`
              if (avgTime !== null && avgTime !== undefined) {
                label += ` • Avg: ${avgTime.toFixed(1)} min`
              }
              return label
            },
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: {
            color: colors.gridColor,
          },
          ticks: {
            color: colors.textColor,
            stepSize: 1,
            precision: 0,
          },
          title: {
            display: true,
            text: 'Sessions',
            color: colors.textColor,
            font: {
              size: 12,
            },
          },
        },
        y: {
          grid: {
            display: false,
          },
          ticks: {
            color: colors.textColor,
            font: {
              size: 12,
            },
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
