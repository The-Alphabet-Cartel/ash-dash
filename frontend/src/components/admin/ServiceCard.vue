<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
ServiceCard Component - Status card for system health services
----------------------------------------------------------------------------
FILE VERSION: v5.0-11-11.11-2
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div 
    class="card p-4 border-l-4 transition-colors"
    :class="borderClass"
  >
    <!-- Header -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3">
        <div 
          class="w-10 h-10 rounded-lg flex items-center justify-center"
          :class="iconBgClass"
        >
          <component :is="icon" class="w-5 h-5" :class="iconClass" />
        </div>
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white">
            {{ name }}
          </h3>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ statusLabel }}
          </p>
        </div>
      </div>
      
      <!-- Status Indicator -->
      <div class="flex items-center gap-1.5">
        <span 
          class="w-2.5 h-2.5 rounded-full animate-pulse"
          :class="dotClass"
        />
        <component 
          :is="statusIcon" 
          class="w-5 h-5" 
          :class="statusIconClass" 
        />
      </div>
    </div>
    
    <!-- Details (if provided) -->
    <div v-if="hasDetails" class="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
      <dl class="grid grid-cols-2 gap-2 text-sm">
        <template v-for="(value, key) in displayDetails" :key="key">
          <dt class="text-gray-500 dark:text-gray-400">{{ formatKey(key) }}</dt>
          <dd 
            class="text-gray-900 dark:text-white font-medium text-right truncate"
            :title="getRawValue(key, value)"
          >
            {{ formatValue(key, value) }}
          </dd>
        </template>
      </dl>
    </div>
  </div>
</template>

<script setup>
/**
 * ServiceCard Component
 * 
 * Displays service health status with:
 * - Service name and icon
 * - Status indicator (healthy/degraded/unhealthy)
 * - Optional details like latency, version, etc.
 */

import { computed } from 'vue'
import { CheckCircle, AlertCircle, XCircle, Server } from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Service display name
   */
  name: {
    type: String,
    required: true,
  },
  /**
   * Service status: 'healthy', 'degraded', 'unhealthy', 'unknown'
   */
  status: {
    type: String,
    default: 'unknown',
  },
  /**
   * Service icon component
   */
  icon: {
    type: [Object, Function],
    default: () => Server,
  },
  /**
   * Additional service details object
   */
  details: {
    type: Object,
    default: () => ({}),
  },
})

// =============================================================================
// Status Configuration
// =============================================================================

const statusConfig = {
  healthy: {
    label: 'Operational',
    icon: CheckCircle,
    border: 'border-green-500',
    dot: 'bg-green-500',
    iconBg: 'bg-green-100 dark:bg-green-900/30',
    iconColor: 'text-green-600 dark:text-green-400',
    statusIcon: 'text-green-500',
  },
  degraded: {
    label: 'Degraded',
    icon: AlertCircle,
    border: 'border-yellow-500',
    dot: 'bg-yellow-500',
    iconBg: 'bg-yellow-100 dark:bg-yellow-900/30',
    iconColor: 'text-yellow-600 dark:text-yellow-400',
    statusIcon: 'text-yellow-500',
  },
  unhealthy: {
    label: 'Unhealthy',
    icon: XCircle,
    border: 'border-red-500',
    dot: 'bg-red-500',
    iconBg: 'bg-red-100 dark:bg-red-900/30',
    iconColor: 'text-red-600 dark:text-red-400',
    statusIcon: 'text-red-500',
  },
  unknown: {
    label: 'Unknown',
    icon: AlertCircle,
    border: 'border-gray-400',
    dot: 'bg-gray-400',
    iconBg: 'bg-gray-100 dark:bg-gray-800',
    iconColor: 'text-gray-600 dark:text-gray-400',
    statusIcon: 'text-gray-400',
  },
}

// =============================================================================
// Computed Properties
// =============================================================================

const config = computed(() => {
  return statusConfig[props.status] || statusConfig.unknown
})

const statusLabel = computed(() => config.value.label)
const statusIcon = computed(() => config.value.icon)
const borderClass = computed(() => config.value.border)
const dotClass = computed(() => config.value.dot)
const iconBgClass = computed(() => config.value.iconBg)
const iconClass = computed(() => config.value.iconColor)
const statusIconClass = computed(() => config.value.statusIcon)

/**
 * Filter details to show only relevant, non-status fields
 */
const displayDetails = computed(() => {
  if (!props.details) return {}
  
  // Fields to exclude from display
  const excludeFields = ['status', 'error', 'message']
  
  return Object.fromEntries(
    Object.entries(props.details)
      .filter(([key]) => !excludeFields.includes(key))
      .slice(0, 4) // Limit to 4 detail items
  )
})

const hasDetails = computed(() => {
  return Object.keys(displayDetails.value).length > 0
})

// =============================================================================
// Helpers
// =============================================================================

/**
 * Format detail key for display
 */
function formatKey(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

/**
 * Get raw value for tooltip display
 */
function getRawValue(key, value) {
  if (value === null || value === undefined) return ''
  if (Array.isArray(value)) return value.join(', ')
  return String(value)
}

/**
 * Format detail value for display
 */
function formatValue(key, value) {
  // Handle latency values (convert to ms)
  if (key.includes('latency') && typeof value === 'number') {
    return `${value.toFixed(0)}ms`
  }
  
  // Handle boolean values
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No'
  }
  
  // Handle null/undefined
  if (value === null || value === undefined) {
    return '-'
  }
  
  // Handle arrays (like secrets_available)
  if (Array.isArray(value)) {
    if (value.length === 0) return 'None'
    if (value.length <= 2) return value.join(', ')
    return `${value.length} items`
  }
  
  // Truncate long strings
  const strValue = String(value)
  if (strValue.length > 25) {
    return strValue.substring(0, 22) + '...'
  }
  
  return strValue
}
</script>
